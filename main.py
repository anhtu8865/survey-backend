from fastapi import FastAPI

from database import db

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Example endpoint to test MongoDB connection
@app.get("/items/")
async def get_items():
    # Access a collection and fetch documents
    collection = db["items"]  # Replace "items" with your collection name
    items = []
    async for item in collection.find():
        item["id"] = str(item.pop("_id"))
        items.append(item)
    return items


# Example endpoint to insert a document
@app.post("/items/")
async def create_item(item: dict):
    collection = db["items"]
    result = await collection.insert_one(item)
    return {"inserted_id": str(result.inserted_id)}
