# backend/app/models/alert.py
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class Alert(BaseModel):
    id: str
    rule_id: str
    severity: str
    details: Dict[str, Any]
    timestamp: datetime