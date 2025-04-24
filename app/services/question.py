from bson import ObjectId
from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.api.schemas.question import QuestionCreate, QuestionUpdate
from app.core.database import get_db
from app.models.survey import Survey


class QuestionService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["surveys"]

    async def create(self, question_create: QuestionCreate, survey: Survey):
        if question_create.index > len(survey["questions"]):
            raise HTTPException(status_code=400, detail="Index out of range")

        for question in survey["questions"]:
            if question["question_id"] == question_create.question_id:
                raise HTTPException(
                    status_code=400, detail="Question ID already exists"
                )
        question_data = {
            "question_id": question_create.question_id,
            "title": question_create.title,
            "type": question_create.type,
            "options": question_create.options,
        }
        await self.collection.update_one(
            {"_id": ObjectId(question_create.survey_id)},
            {
                "$push": {
                    "questions": {
                        "$each": [question_data],
                        "$position": question_create.index,
                    }
                }
            },
        )
        return {"message": "Question created successfully"}

    async def update(self, question_update: QuestionUpdate, survey: Survey, index: int):
        if index >= len(survey["questions"]):
            raise HTTPException(status_code=400, detail="Index out of range")

        for idx, question in enumerate(survey["questions"]):
            if question["question_id"] == question_update.question_id and idx != index:
                raise HTTPException(
                    status_code=400, detail="Question ID already exists"
                )

        data_update = {
            "question_id": question_update.question_id,
            "title": question_update.title,
            "type": question_update.type,
            "options": question_update.options,
        }
        await self.collection.update_one(
            {"_id": ObjectId(survey["id"])},
            {"$set": {f"questions.{index}": data_update}},
        )
        return {"message": "Question updated successfully"}

    async def delete(self, survey: Survey, index: int):
        if index >= len(survey["questions"]):
            raise HTTPException(status_code=400, detail="Index out of range")
        await self.collection.update_one(
            {"_id": ObjectId(survey["id"])},
            {"$unset": {f"questions.{index}": ""}},
        )
        await self.collection.update_one(
            {"_id": ObjectId(survey["id"])},
            {"$pull": {"questions": None}},
        )
        return {"message": "Question deleted successfully"}

async def get_question_service(db=Depends(get_db)):
    return QuestionService(db)