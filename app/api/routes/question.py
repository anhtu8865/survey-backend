from bson import ObjectId
from fastapi import APIRouter, HTTPException, Path
from app.api.schemas.question import QuestionCreate, QuestionUpdate
from app.core.database import db
from app.services.survey import SurveyService
from app.services.question import QuestionService

router = APIRouter()


@router.post("/")
async def create(question_create: QuestionCreate):
    survey = await SurveyService.get(question_create.survey_id)
    return await QuestionService.create(question_create=question_create, survey=survey)


@router.put("/{survey_id}/{index}")
async def update(
    question_update: QuestionUpdate,
    survey_id: str,
    index: int = Path(..., ge=0),
):
    survey = await SurveyService.get(survey_id)
    return await QuestionService.update(
        question_update=question_update, survey=survey, index=index
    )


@router.delete("/{survey_id}/{index}")
async def delete(survey_id: str, index: int = Path(..., ge=0)):
    survey = await SurveyService.get(survey_id)
    return await QuestionService.delete(survey=survey, index=index)
