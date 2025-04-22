from pydantic import BaseModel


class SurveyCreate(BaseModel):
    title: str
    description: str | None = None
