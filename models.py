from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from database import metadata


users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, unique=True, index=True),
    Column("hashed_password", String),
    Column("is_active", Boolean, default=True)
)


items = Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, index=True),
    Column("description", String),
    Column("owner_id", Integer, ForeignKey("users.id"))
)
