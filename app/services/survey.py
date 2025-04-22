from bson import ObjectId
from fastapi import HTTPException
from app.api.schemas.survey import SurveyCreate
from app.core.database import db


class SurveyService:
    async def create(survey_create: SurveyCreate):
        collection = db["surveys"]
        data = survey_create.dict()
        data["questions"] = []
        result = await collection.insert_one(data)
        return {"inserted_id": str(result.inserted_id)}

    async def get(survey_id: str):
        collection = db["surveys"]
        survey = await collection.find_one({"_id": ObjectId(survey_id)})
        if not survey:
            raise HTTPException(status_code=404, detail="Item not found")
        survey["id"] = str(survey.pop("_id"))
        return survey

    async def get_many():
        collection = db["surveys"]
        surveys = []
        async for item in collection.find():
            item["id"] = str(item.pop("_id"))
            surveys.append(item)
        return surveys
