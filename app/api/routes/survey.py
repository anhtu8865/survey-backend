from fastapi import APIRouter
from app.models.survey import Survey
from app.core.database import db

router = APIRouter()


@router.get("/surveys/")
async def get_surveys():
    # Access a collection and fetch documents
    collection = db["surveys"]  # Replace "surveys" with your collection name
    surveys = []
    async for item in collection.find():
        item["id"] = str(item.pop("_id"))
        surveys.append(item)
    return surveys


@router.post("/surveys/")
async def create_item(item: Survey):
    collection = db["surveys"]
    result = await collection.insert_one(item.dict())
    return {"inserted_id": str(result.inserted_id)}
