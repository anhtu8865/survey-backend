from enum import Enum
from typing import Any, List

from pydantic import BaseModel


class QuestionType(str, Enum):
    TEXT = "text"
    SINGLE = "single"
    MULTIPLE = "multiple"


class Question(BaseModel):
    question_id: str
    title: str
    type: QuestionType
    options: List[str]
