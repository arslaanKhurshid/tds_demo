# backend/app/services/mock_log_service.py
from app.models.log import Log
from app.services.memory_storage_service import MemoryStorageService
import uuid
from datetime import datetime
import random

async def generate_mock_log():
    storage_service = MemoryStorageService()
    log = Log(
        id=str(uuid.uuid4()),
        timestamp=datetime.utcnow(),
        source_ip=f"192.168.1.{random.randint(1, 255)}",
        event_type=random.choice(["login", "access", "error"]),
        details={
            "event": random.choice([
                "User login attempt",
                "File access denied",
                "Suspicious network activity"
            ]),
            "user": f"user{random.randint(1, 100)}"
        }
    )
    await storage_service.store_log(log)
    return log