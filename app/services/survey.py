from bson import ObjectId
from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.schemas.survey import SurveyCreate
from app.core.database import get_db


class SurveyService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["surveys"]

    async def create(self, survey_create: SurveyCreate):
        data = survey_create.dict()
        data["questions"] = []
        result = await self.collection.insert_one(data)
        return {"inserted_id": str(result.inserted_id)}

    async def get(self, survey_id: str):
        survey = await self.collection.find_one({"_id": ObjectId(survey_id)})
        if not survey:
            raise HTTPException(status_code=404, detail="Item not found")
        survey["id"] = str(survey.pop("_id"))
        return survey

    async def get_many(self):
        surveys = []
        async for item in self.collection.find():
            item["id"] = str(item.pop("_id"))
            surveys.append(item)
        return surveys

async def get_survey_service(db=Depends(get_db)):
    return SurveyService(db)