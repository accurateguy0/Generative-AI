import subprocess
from langchain.tools import tool

@tool
def run_security_scan(file_path: str):
    
    result = subprocess.run(["bandit", "-r", file_path, "-f", "json"], capture_output=True, text=True)
    return result.stdout

@tool
def run_ruff_lint(file_path: str):
    
    result = subprocess.run(["ruff", "check", file_path], capture_output=True, text=True)
    return result.stdout
