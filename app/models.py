from typing import List
from pydantic import BaseModel

class Query(BaseModel):
    question: str

class ChatHistory(BaseModel):
    messages: List[dict]