import uvicorn
from fastapi import FastAPI
from app.api.routes.survey import router as survey_router


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(survey_router, prefix="/api", tags=["surveys"])
