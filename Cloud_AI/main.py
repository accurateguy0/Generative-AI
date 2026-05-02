import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)


from Data_Classification.Governance_Bot import app as bot_app

app = FastAPI()

class ClassificationRequest(BaseModel):
    
    csv_path: str 

@app.get("/")
def home():
    return {"message": "Cloud-AI Gateway is Online UwU"}

@app.post("/run-audit")
async def run_audit(request: ClassificationRequest):
    
    full_path = os.path.join(parent_dir, request.csv_path)
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail=f"File not found at {full_path}")

    try:
        
        result = bot_app.invoke({"csv_path": full_path})
        
        return {
            "status": "Success",
            "masked_file": result.get("masked_path"),
            "summary": "AI Governance complete via Cloud_AI module"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
