from fastapi import FastAPI

from app.api.routes.question import router as question_router
from app.api.routes.survey import router as survey_router

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(survey_router, prefix="/api/surveys", tags=["surveys"])
app.include_router(question_router, prefix="/api/questions", tags=["questions"])
