from typing import List

from pydantic import BaseModel

from app.models.question import QuestionType


class QuestionCreate(BaseModel):
    survey_id: str
    index: int
    question_id: str
    title: str
    type: QuestionType
    options: List[str]


class QuestionUpdate(BaseModel):
    question_id: str
    title: str
    type: QuestionType
    options: List[str]
