from pydantic import BaseModel
from typing import Optional


class AskQuestion(BaseModel):
    question: str


class QnaResponse(BaseModel):
    question: str
    answer: str
    source: Optional[str] = None
