from fastapi import APIRouter, Depends

from app.api.schemas.survey import SurveyCreate
from app.services.survey import SurveyService, get_survey_service

router = APIRouter()


@router.post("/")
async def create(
    survey_create: SurveyCreate,
    survey_service: SurveyService = Depends(get_survey_service),
):
    return await survey_service.create(survey_create)


@router.get("/{survey_id}")
async def get(
    survey_id: str, survey_service: SurveyService = Depends(get_survey_service)
):
    return await survey_service.get(survey_id)


@router.get("/")
async def get_many(survey_service: SurveyService = Depends(get_survey_service)):
    return await survey_service.get_many()
