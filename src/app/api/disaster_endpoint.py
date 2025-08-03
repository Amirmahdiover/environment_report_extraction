from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from extractor import extract_json
import json
app = FastAPI()

class ReportInput(BaseModel):
    report_text: str

@app.post("/extract/")
async def extract_report(report: ReportInput):
    try:
        result = extract_json(report.report_text)
        json_result = json.loads(result)
        return {"success": True, "result": json_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
