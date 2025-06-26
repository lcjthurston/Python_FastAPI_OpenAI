# main.py

from typing import Optional, List
from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
# Import StaticFiles
from fastapi.staticfiles import StaticFiles

# Define Pydantic models for data validation and schema generation
class Item(BaseModel):
    """
    Represents an item available in the store.
    """
    id: Optional[int] = Field(None, description="Unique identifier for the item")
    name: str = Field(..., example="Laptop Pro", description="Name of the item")
    description: Optional[str] = Field(None, example="Powerful laptop for professionals", description="Detailed description of the item")
    price: float = Field(..., gt=0, example=1200.00, description="Price of the item (must be greater than 0)")
    tax: Optional[float] = Field(None, ge=0, le=1.0, example=0.08, description="Tax rate applicable to the item (between 0 and 1)")

class User(BaseModel):
    """
    Represents a user of the application.
    """
    id: Optional[int] = Field(None, description="Unique identifier for the user")
    username: str = Field(..., example="johndoe", description="Unique username for the user")
    email: Optional[str] = Field(None, example="john.doe@example.com", description="User's email address")
    full_name: Optional[str] = Field(None, example="John Doe", description="Full name of the user")

# Initialize the FastAPI application
app = FastAPI(
    title="E-commerce API",
    description="This is a simple e-commerce API built with FastAPI, demonstrating automatic OpenAPI schema generation.",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Local Development Server"}
    ]
)

# In-memory "database" for demonstration purposes
items_db = {}
users_db = {}
next_item_id = 1
next_user_id = 1

# --- ADD THIS SECTION FOR STATIC FILES ---
# Mount the "static" directory to serve static files.
# By mounting it at "/", if a request for "/favicon.ico" comes,
# FastAPI will look for "static/favicon.ico".
app.mount("/", StaticFiles(directory="static"), name="static")
# ----------------------------------------


@app.get("/")
async def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the E-commerce API! Visit /docs for interactive documentation."}

@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item: Item):
    """
    Create a new item in the store.

    - **name**: Name of the item.
    - **description**: Optional detailed description.
    - **price**: Price of the item (must be positive).
    - **tax**: Optional tax rate (between 0 and 1).
    """
    global next_item_id
    item.id = next_item_id
    items_db[item.id] = item
    next_item_id += 1
    return item

@app.get("/items/", response_model=List[Item], tags=["Items"])
async def get_items(
    skip: int = Query(0, description="Number of items to skip"),
    limit: int = Query(10, description="Maximum number of items to return (max 100)", le=100),
):
    """
    Retrieve a list of all available items with optional pagination.
    """
    response_items = list(items_db.values())[skip : skip + limit]
    return response_items

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def read_item(
    item_id: int = Path(..., title="The ID of the item to get", description="The ID of the item you want to retrieve", ge=1)
):
    """
    Retrieve details of a specific item by its ID.
    """
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(
    item: Item, # Corrected order
    item_id: int = Path(..., title="The ID of the item to update", ge=1)
):
    """
    Update an existing item by its ID.
    The request body expects an updated Item object with its details.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    item.id = item_id # Ensure the ID in the payload matches the path ID
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(
    item_id: int = Path(..., title="The ID of the item to delete", ge=1)
):
    """
    Delete an item by its ID.
    """
    if item_id not in items_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted successfully"}

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: User):
    """
    Create a new user.
    """
    global next_user_id
    user.id = next_user_id
    users_db[user.id] = user
    next_user_id += 1
    return user

@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def read_user(user_id: int = Path(..., title="The ID of the user to get", ge=1)):
    """
    Retrieve details of a specific user by their ID.
    """
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
