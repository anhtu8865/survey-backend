from pydantic import BaseModel
from typing import Any


class QuestionCreate(BaseModel):
    survey_id: str
    index: int
    question_id: str
    title: str
    type: str
    answers: Any


class QuestionUpdate(BaseModel):
    question_id: str
    title: str
    type: str
    answers: Any
