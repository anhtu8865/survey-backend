from pydantic import BaseModel


class Survey(BaseModel):
    title: str
    description: str | None = None
