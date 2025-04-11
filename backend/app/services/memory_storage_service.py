# backend/app/services/memory_storage_service.py
from typing import List, Optional
from app.models.log import Log
from app.models.rule import Rule
from app.models.alert import Alert
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MemoryStorageService:
    _instance = None
    _logs: List[Log] = []
    _rules: List[Rule] = []
    _alerts: List[Alert] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryStorageService, cls).__new__(cls)
            # Initialize with hardcoded logs and rules
            cls._instance._initialize_data()
        return cls._instance

    def _initialize_data(self):
        """Initialize hardcoded logs and rules."""
        # Hardcoded Logs
        self._logs = [
            Log(
                id="log-001",
                timestamp=datetime.fromisoformat("2025-04-11T10:00:00"),
                source_ip="192.168.1.100",
                event_type="login",
                details={
                    "event": "User login attempt",
                    "user": "admin",
                    "status": "success"
                }
            ),
            Log(
                id="log-002",
                timestamp=datetime.fromisoformat("2025-04-11T10:01:00"),
                source_ip="192.168.1.101",
                event_type="login",
                details={
                    "event": "User login attempt",
                    "user": "unknown",
                    "status": "failed"
                }
            ),
            Log(
                id="log-003",
                timestamp=datetime.fromisoformat("2025-04-11T10:02:00"),
                source_ip="10.0.0.50",
                event_type="error",
                details={
                    "event": "Access denied",
                    "resource": "/sensitive/data",
                    "user": "guest"
                }
            ),
            Log(
                id="log-004",
                timestamp=datetime.fromisoformat("2025-04-11T10:03:00"),
                source_ip="192.168.1.100",
                event_type="access",
                details={
                    "event": "File accessed",
                    "file": "/public/index.html",
                    "user": "admin"
                }
            )
        ]
        logger.debug("Initialized hardcoded logs")

        # Hardcoded Rules
        self._rules = [
            Rule(
                id="rule-001",
                name="Suspicious Login Rule",
                query="event_type == 'login' AND status == 'failed'",
                exclusion_list=["192.168.1.100"],
                enabled=True
            ),
            Rule(
                id="rule-002",
                name="Unauthorized Access Rule",
                query="event_type == 'error' AND resource == '/sensitive/data'",
                exclusion_list=[],
                enabled=True
            ),
            Rule(
                id="rule-003",
                name="Admin Activity Rule",
                query="user == 'admin' AND event_type != 'login'",
                exclusion_list=["10.0.0.50"],
                enabled=True
            )
        ]
        logger.debug("Initialized hardcoded rules")

    async def store_log(self, log: Log):
        logger.debug(f"Storing log: {log.id}")
        self._logs.append(log)

    async def get_logs(self) -> List[Log]:
        logger.debug("Retrieving all logs")
        return self._logs

    async def store_rule(self, rule: Rule):
        logger.debug(f"Storing rule: {rule.id}")
        self._rules.append(rule)

    async def get_rules(self) -> List[Rule]:
        logger.debug("Retrieving all rules")
        return self._rules

    async def get_rule(self, rule_id: str) -> Optional[Rule]:
        logger.debug(f"Retrieving rule: {rule_id}")
        for rule in self._rules:
            if rule.id == rule_id:
                return rule
        return None

    async def store_alert(self, alert: Alert):
        logger.debug(f"Storing alert: {alert.id}")
        self._alerts.append(alert)

    async def get_alerts(self) -> List[Alert]:
        logger.debug("Retrieving all alerts")
        return self._alerts