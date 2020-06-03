from database import database
from models import users, items
import schemas


async def get_user(user_id: int):
    user = dict(await database.fetch_one(users.select().where(users.c.id == user_id)))
    list_item = await database.fetch_all(items.select().where(items.c.owner_id == user["id"]))
    user.update({"items": [dict(result) for result in list_item]})
    return user


async def get_user_by_email(email: str):
    return await database.fetch_one(users.select().where(users.c.email == email))


async def get_users(skip: int = 0, limit: int = 100):
    results = await database.fetch_all(users.select().offset(skip).limit(limit))
    return [dict(result) for result in results]


async def create_user(user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = users.insert().values(email=user.email, hashed_password=fake_hashed_password)
    user_id = await database.execute(db_user)
    return schemas.User(**user.dict(), id=user_id)


async def get_items(skip: int = 0, limit: int = 100):
    query = items.select().offset(skip).limit(limit)
    results = await database.fetch_all(query)
    return [dict(result) for result in results]


async def get_item_user(pk: int):
    item = dict(await database.fetch_one(items.select().where(items.c.id == pk)))
    user = dict(await database.fetch_one(users.select().where(users.c.id == item["owner_id"])))
    item.update({"owner": user})
    return item


async def create_user_item(item: schemas.ItemCreate, user_id: int):
    query = items.insert().values(**item.dict(), owner_id=user_id)
    item_id = await database.execute(query)
    return schemas.Item(**item.dict(), id=item_id, owner_id=user_id)
