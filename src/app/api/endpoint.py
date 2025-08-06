# src/app/api/disaster_endpoint.py

import os
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from src.app.agents.disaster_agent import DisasterAgent

load_dotenv()

# Load config
api_key = os.getenv("OPENAI_API_KEY")

# Create one shared instance of the agent
agent = DisasterAgent(model_name="gpt-4o-mini", temperature=0.4, api_key=api_key)

# FastAPI Router (modular endpoint)
router = APIRouter()

class ReportInput(BaseModel):
    report_text: str

@router.post("/extract/")
async def extract_report(report: ReportInput):
    try:
        result = agent.process(report.report_text)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
