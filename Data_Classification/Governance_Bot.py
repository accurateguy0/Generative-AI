import os
import pandas as pd
import json
import re
from typing import TypedDict, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv
load_dotenv()

G_KEY = os.getenv("GOOGLE_API_KEY") 
console = Console()

class DataState(TypedDict):
    csv_path: str
    schema_info: str
    sample_data: str
    raw_json: str
    masked_path: str

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
    Sensitivity: "High", "Medium", or "Low".
    Do not include markdown blocks.
    """
    response = llm.invoke(prompt)
    
    content = response.content
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict) and "text" in part:
                text_parts.append(part["text"])
            else:
                text_parts.append(str(part))
        content = "".join(text_parts)
    elif isinstance(content, dict) and "text" in content:
        content = content["text"]
    
    content = str(content)
    clean_json = content.replace("```json", "").replace("```", "").strip()
    return {"raw_json": clean_json}

def data_masker(state: DataState):
    df = pd.read_csv(state['csv_path'])
    try:
        classifications = json.loads(state['raw_json'])
    except Exception:
        # Emergency fix: if JSON is still messy, try regex to find the array
        match = re.search(r'\[.*\]', state['raw_json'], re.DOTALL)
        if match:
            classifications = json.loads(match.group())
        else:
            raise ValueError("Could not parse AI JSON response")

    for item in classifications:
        col = item['column']
        level = str(item['sensitivity']).capitalize()

        if level == "High":
            df[col] = "[MASKED]"
        elif level == "Medium":
            df[col] = df[col].astype(str).apply(lambda x: x[0] + "****" if len(x) > 1 else "****")

    masked_file = "customer_data_MASKED.csv"
    df.to_csv(masked_file, index=False)
    return {"masked_path": masked_file}

workflow = StateGraph(DataState)
workflow.add_node("ingestor", metadata_ingestor)
workflow.add_node("classifier", gemini_classifier)
workflow.add_node("masker", data_masker)
workflow.set_entry_point("ingestor")
workflow.add_edge("ingestor", "classifier")
workflow.add_edge("classifier", "masker")
workflow.add_edge("masker", END)
app = workflow.compile()

if __name__ == "__main__":
    if not os.path.exists("customer_data.csv"):
        console.print("[bold red]Error: customer_data.csv not found.[/bold red]")
    else:
        with console.status("[bold green]Running Data Governance Pipeline...", spinner="runner"):
            result = app.invoke({"csv_path": "customer_data.csv"})

        data = json.loads(result["raw_json"])
        table = Table(title="🛡️  PII CLASSIFICATION DASHBOARD", title_style="bold magenta", border_style="bright_blue")
        table.add_column("Column", style="bold white")
        table.add_column("Category", style="yellow")
        table.add_column("Sensitivity", justify="center")

        for row in data:
            level = str(row['sensitivity']).capitalize()
            color = "red" if level == "High" else "yellow" if level == "Medium" else "green"
            table.add_row(row['column'], row['category'], f"[{color}]{level}[/{color}]")
        
        console.print("\n", table)
        console.print(f"\n[bold green]✅ Success! Masked file saved at:[/bold green] [bold cyan]{result['masked_path']}[/bold cyan]")
        console.print("\n[bold white]👀 Preview of Masked Data:[/bold white]")
        console.print(pd.read_csv(result['masked_path']).head())
