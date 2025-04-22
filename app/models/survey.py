from typing import List
from pydantic import BaseModel

from app.models.question import Question


class Survey(BaseModel):
    title: str
    description: str | None = None
    questions: List[Question]
