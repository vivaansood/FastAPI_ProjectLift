from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create the FastAPI app instance 
app = FastAPI()


# Gives us data validation, better docs, and IDE autocomplete for free
class Item(BaseModel):
    text: str = None
    is_done: bool = False

# In-memory list to store our items. resets every time the server reloads
items = []


# Root route. handles GET requests to "/"
@app.get("/")
def root():
    return {"Hello": "World"}


# POST route to create a new item
# Now takes an Item object instead of a plain string query parameter
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items


# GET route to list items
# response_model tells FastAPI this returns a list of Item objects
# limit is a query parameter with a default value of 10
@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]


# GET route to fetch a single item by its index 
# response_model=Item tells FastAPI the response should conform to the Item structure
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    # Check that the requested index exists in our items list
    if item_id < len(items):
        return items[item_id]
    else:
        # Raise a proper error instead of letting it crash with a generic error
        raise HTTPException(status_code=404, detail="Item not found")