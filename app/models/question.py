from pydantic import BaseModel
from typing import Any


class Question(BaseModel):
    question_id: str
    title: str
    type: str
    answers: Any
