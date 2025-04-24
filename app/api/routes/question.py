from fastapi import APIRouter, Depends, Path

from app.api.schemas.question import QuestionCreate, QuestionUpdate
from app.services.question import QuestionService, get_question_service
from app.services.survey import SurveyService, get_survey_service

router = APIRouter()


@router.post("/")
async def create(
    question_create: QuestionCreate,
    survey_service: SurveyService = Depends(get_survey_service),
    question_service: QuestionService = Depends(get_question_service),
):
    survey = await survey_service.get(question_create.survey_id)
    return await question_service.create(question_create=question_create, survey=survey)


@router.put("/{survey_id}/{index}")
async def update(
    question_update: QuestionUpdate,
    survey_id: str,
    index: int = Path(..., ge=0),
    survey_service: SurveyService = Depends(get_survey_service),
    question_service: QuestionService = Depends(get_question_service),
):
    survey = await survey_service.get(survey_id)
    return await question_service.update(
        question_update=question_update, survey=survey, index=index
    )


@router.delete("/{survey_id}/{index}")
async def delete(
    survey_id: str,
    index: int = Path(..., ge=0),
    survey_service: SurveyService = Depends(get_survey_service),
    question_service: QuestionService = Depends(get_question_service),
):
    survey = await survey_service.get(survey_id)
    return await question_service.delete(survey=survey, index=index)
