import os
import pandas as pd
import json
from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

G_KEY = os.getenv("GOOGLE_API_KEY")
console = Console()

class DataState(TypedDict):
    csv_path: str
    schema_info: str
    sample_data: str
    raw_json: str

def metadata_ingestor(state: DataState):
    df = pd.read_csv(state['csv_path'])
    state['schema_info'] = df.dtypes.to_string()
    state['sample_data'] = df.head(2).to_string()
    return state

def gemini_classifier(state: DataState):
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=G_KEY)
    prompt = f"""
    Act as a Data Privacy Officer. Classify these columns: {state['schema_info']} 
    Sample: {state['sample_data']}
    Return ONLY a JSON list of objects with these keys: 
    "column", "category", "sensitivity", "reason"
    Sensitivity must be: "High", "Medium", or "Low".
    """
    response = llm.invoke(prompt)
    content = response.content

    if isinstance(content, dict) and "text" in content:
        content = content["text"]
    elif isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
            else:
                text_parts.append(str(part))
        content = "".join(text_parts)
    
    content = str(content)
    clean_json = content.replace("```json", "").replace("```", "").strip()
    return {"raw_json": clean_json}

workflow = StateGraph(DataState)
workflow.add_node("ingestor", metadata_ingestor)
workflow.add_node("classifier", gemini_classifier)
workflow.set_entry_point("ingestor")
workflow.add_edge("ingestor", "classifier")
workflow.add_edge("classifier", END)
app = workflow.compile()

if __name__ == "__main__":
    if os.path.exists("customer_data.csv"):
        with console.status("[bold green]Analyzing Data Schema...", spinner="aesthetic"):
            result = app.invoke({"csv_path": "customer_data.csv"})
        try:
            data = json.loads(result["raw_json"])
            table = Table(title="🛡️ Data Classification Report", title_style="bold magenta", border_style="bright_blue")
            table.add_column("Column")
            table.add_column("Category")
            table.add_column("Sensitivity", justify="center")
            table.add_column("Reason", width=50)
            for row in data:
                sens = row['sensitivity'].capitalize()
                color = "red" if sens == "High" else "yellow" if sens == "Medium" else "green"
                table.add_row(row['column'], row['category'], f"[{color}]{sens}[/{color}]", row['reason'])
            console.print("\n", Panel(table, expand=False, border_style="bright_magenta"))
        except Exception as e:
            console.print(f"[bold red]JSON Error:[/bold red] {e}")
            console.print(f"Content Attempted: {result['raw_json'][:100]}...")
