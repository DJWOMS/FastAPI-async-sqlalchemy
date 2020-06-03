from typing import List
from fastapi import FastAPI, HTTPException
from database import database, engine, metadata

import crud
import schemas


metadata.create_all(bind=engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


@app.get("/users/", response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100):
    return await crud.get_users(skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(user_id: int, item: schemas.ItemCreate):
    return await crud.create_user_item(item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
async def read_items(skip: int = 0, limit: int = 100):
    return await crud.get_items(skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=schemas.ItemUser)
async def read_item(item_id: int):
    return await crud.get_item_user(pk=item_id)
