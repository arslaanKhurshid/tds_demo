# backend/app/models/rule.py
from pydantic import BaseModel
from typing import List

class Rule(BaseModel):
    id: str
    name: str
    query: str
    exclusion_list: List[str]
    enabled: bool = True