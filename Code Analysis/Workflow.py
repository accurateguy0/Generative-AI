import os
import subprocess
import requests
import base64
from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from rich.console import Console
from rich.markdown import Markdown

G_KEY = os.getenv("GOOGLE_API_KEY")
GH_TOKEN = os.getenv("GITHUB_TOKEN")

class AgentState(TypedDict):
    repo_owner: str
    repo_name: str
    files_to_check: List[str]
    files_data: List[dict] 
    reports: List[str]
    final_analysis: str

def ingestion_node(state: AgentState):
    headers = {"Authorization": f"token {GH_TOKEN}"}
    files_content = []
    for file_path in state['files_to_check']:
        url = f"https://api.github.com/repos/{state['repo_owner']}/{state['repo_name']}/contents/{file_path}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = base64.b64decode(response.json()['content']).decode('utf-8')
            files_content.append({"filename": file_path, "content": content})
    return {"files_data": files_content}

def scanner_node(state: AgentState):
    all_reports = []
    for file in state.get('files_data', []):
        with open(file['filename'], "w") as f:
            f.write(file['content'])
        bandit_res = subprocess.run(["bandit", "-r", file['filename'], "-q"], capture_output=True, text=True).stdout
        ruff_res = subprocess.run(["ruff", "check", file['filename']], capture_output=True, text=True).stdout
        all_reports.append(f"FILE: {file['filename']}\nBANDIT:\n{bandit_res}\nRUFF:\n{ruff_res}")
        if os.path.exists(file['filename']):
            os.remove(file['filename'])
    return {"reports": all_reports}

def gemini_analyzer_node(state: AgentState):
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-latest", 
        google_api_key=G_KEY
    )
    context = "\n\n".join(state.get('reports', []))
    if not context:
        return {"final_analysis": "No security logs were generated to analyze."}
    prompt = f"Analyze these security logs and provide the corrected code for vulnerabilities:\n\n{context}"
    try:
        response = llm.invoke(prompt)
        return {"final_analysis": response.content}
    except Exception as e:
        return {"final_analysis": f"Analysis failed: {str(e)}"}

workflow = StateGraph(AgentState)
workflow.add_node("ingestor", ingestion_node)
workflow.add_node("scanner", scanner_node)
workflow.add_node("analyzer", gemini_analyzer_node)
workflow.set_entry_point("ingestor")
workflow.add_edge("ingestor", "scanner")
workflow.add_edge("scanner", "analyzer")
workflow.add_edge("analyzer", END)
app = workflow.compile()

if __name__ == "__main__":
    console = Console()
    test_config = {
        "repo_owner": "accurateguy0",
        "repo_name": "Generative-AI",
        "files_to_check": ["vulnerable_test.py"],
        "files_data": [],
        "reports": [] 
    }
    try:
        with console.status("[bold green]Running Workflow...", spinner="dots"):
            result = app.invoke(test_config)
        files_found = [f['filename'] for f in result.get('files_data', [])]
        if not files_found:
            console.print("[yellow]⚠️ Warning: No files were downloaded. Check your GitHub Token and file path.[/yellow]")
        else:
            console.print(f"[green]✅ Ingested files:[/green] {files_found}")
        
        reports = result.get('reports', [])
        if not any(reports):
            console.print("[yellow]⚠️ Warning: Scanners (Bandit/Ruff) produced no output. The file might be clean.[/yellow]")
        raw_content = result.get("final_analysis", "")
        if isinstance(raw_content, list) and len(raw_content) > 0:
            final_text = raw_content[0].get('text', "")
        else:
            final_text = str(raw_content)

        if not final_text or final_text.strip() == "":
            console.print("[bold red]❌ Analysis is empty. The LLM did not return a response.[/bold red]")
        else:
            console.print("\n" + "━" * 60, style="blue")
            console.print("🛡️  [bold cyan]GITHUB SECURITY SCAN REPORT[/bold cyan]", justify="center")
            console.print("━" * 60 + "\n", style="blue")
            console.print(Markdown(final_text))
            console.print("\n" + "━" * 60, style="blue")
        
    except Exception as e:
        console.print(f"\n[bold red]❌ Critical Error:[/bold red] {e}")
