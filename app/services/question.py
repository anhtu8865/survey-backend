from bson import ObjectId
from fastapi import HTTPException
from app.api.schemas.question import QuestionCreate, QuestionUpdate
from app.models.survey import Survey
from app.core.database import db


class QuestionService:
    async def create(question_create: QuestionCreate, survey: Survey):
        collection = db["surveys"]
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
            "answers": question_create.answers,
        }
        await collection.update_one(
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

    async def update(question_update: QuestionUpdate, survey: Survey, index: int):
        collection = db["surveys"]
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
            "answers": question_update.answers,
        }
        await collection.update_one(
            {"_id": ObjectId(survey["id"])},
            {"$set": {f"questions.{index}": data_update}},
        )
        return {"message": "Question updated successfully"}

    async def delete(survey: Survey, index: int):
        collection = db["surveys"]
        if index >= len(survey["questions"]):
            raise HTTPException(status_code=400, detail="Index out of range")
        await collection.update_one(
            {"_id": ObjectId(survey["id"])},
            {"$unset": {f"questions.{index}": ""}},
        )
        await collection.update_one(
            {"_id": ObjectId(survey["id"])},
            {"$pull": {"questions": None}},
        )
        return {"message": "Question deleted successfully"}
