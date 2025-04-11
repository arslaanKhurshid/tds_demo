# backend/app/api/alerts.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.memory_storage_service import MemoryStorageService
from app.services.groq_service import GroqService

router = APIRouter()
storage_service = MemoryStorageService()
groq_service = GroqService()

class DetectRequest(BaseModel):
    rule_id: str

@router.post("/detect")
async def detect_threats(request: DetectRequest):
    rule = await storage_service.get_rule(request.rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    logs = await storage_service.get_logs()
    alerts = await groq_service.detect_threats(logs, rule)
    for alert in alerts:
        await storage_service.store_alert(alert)
    return {"message": f"{len(alerts)} alerts generated"}

@router.get("/")
async def get_alerts():
    return await storage_service.get_alerts()