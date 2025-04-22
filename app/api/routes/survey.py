from bson import ObjectId
from fastapi import APIRouter
from app.api.schemas.survey import SurveyCreate
from app.models.survey import Survey
from app.core.database import db
from app.services.survey import SurveyService

router = APIRouter()


@router.post("/")
async def create(survey_create: SurveyCreate):
    return await SurveyService.create(survey_create)


@router.get("/{survey_id}")
async def get(survey_id: str):
    return await SurveyService.get(survey_id)


@router.get("/")
async def get_many():
    return await SurveyService.get_many()
