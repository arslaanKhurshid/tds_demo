# backend/app/models/log.py
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any

class Log(BaseModel):
    id: str
    timestamp: datetime
    source_ip: str
    event_type: str
    details: Dict[str, Any]