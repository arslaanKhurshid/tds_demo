# backend/app/services/db_service.py
import asyncpg
from typing import List, Optional
from app.models.log import Log
from app.models.rule import Rule
from app.models.alert import Alert
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

class DatabaseService:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseService, cls).__new__(cls)
        return cls._instance

    async def initialize(self):
        if self._pool is None:
            try:
                self._pool = await asyncpg.create_pool(
                    user="postgres",
                    password="password",
                    database="postgres",
                    host="localhost",
                    port=5432
                )
                logger.debug("Database pool initialized")
            except Exception as e:
                logger.error(f"Failed to initialize database pool: {str(e)}")
                raise
        return self._pool

    @property
    def pool(self):
        if self._pool is None:
            raise RuntimeError("DatabaseService not initialized. Call initialize() first.")
        return self._pool

    async def store_log(self, log: Log):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO logs (id, timestamp, source_ip, event_type, details)
                VALUES ($1, $2, $3, $4, $5)
                """,
                log.id, log.timestamp, log.source_ip, log.event_type, json.dumps(log.details)
            )

    async def get_logs(self) -> List[Log]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM logs")
            # Ensure each row is correctly passed to Log model
            return [Log(**dict(row)) for row in rows]  # Convert row to dict explicitly

    async def store_rule(self, rule: Rule):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO rules (id, name, query, exclusion_list, enabled)
                VALUES ($1, $2, $3, $4, $5)
                """,
                rule.id, rule.name, rule.query, rule.exclusion_list, rule.enabled
            )

    async def get_rules(self) -> List[Rule]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM rules")
            return [Rule(**dict(row)) for row in rows]

    async def get_rule(self, rule_id: str) -> Optional[Rule]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow("SELECT * FROM rules WHERE id = $1", rule_id)
            return Rule(**dict(row)) if row else None

    async def store_alert(self, alert: Alert):
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO alerts (id, rule_id, severity, details, timestamp)
                VALUES ($1, $2, $3, $4, $5)
                """,
                alert.id, alert.rule_id, alert.severity, json.dumps(alert.details), alert.timestamp
            )

    async def get_alerts(self) -> List[Alert]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch("SELECT * FROM alerts")
            return [Alert(**dict(row)) for row in rows]