from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

items = []
current_id = 1

class Item(BaseModel):
    name: str
    description: str | None = None

class ItemResponse(Item):
    id: int

#commented
@app.post("/items", response_model=ItemResponse)
def create_item(item: Item):
    global current_id
    new_item = {
        "id": current_id,
        "name": item.name,
        "description": item.description
    }
    items.append(new_item)
    current_id += 1
    return new_item

@app.get("/items", response_model=List[ItemResponse])
def get_items():
    return items

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    for item in items:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, updated_item: Item):
    for item in items:
        if item["id"] == item_id:
            item["name"] = updated_item.name
            item["description"] = updated_item.description
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(index)
            return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
