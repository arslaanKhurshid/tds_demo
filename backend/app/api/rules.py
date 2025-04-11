# backend/app/api/rules.py
from fastapi import APIRouter, HTTPException
from app.models.rule import Rule
from app.services.memory_storage_service import MemoryStorageService
from app.services.groq_service import GroqService

router = APIRouter()
storage_service = MemoryStorageService()
groq_service = GroqService()

@router.post("/generate")
async def generate_rule():
    logs = await storage_service.get_logs()
    log_samples = [log.dict() for log in logs[:5]]  # Use up to 5 logs
    rule = await groq_service.generate_rule(log_samples)
    await storage_service.store_rule(rule)
    return {"message": "Rule generated", "rule_id": rule.id}

@router.get("/")
async def get_rules():
    return await storage_service.get_rules()