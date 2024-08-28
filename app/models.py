from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from typing import Optional, Any

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    chat_history: Optional[Any] = Field(sa_column=Column(JSON), default=[])

class Payload(BaseModel):
    user_id: int
    user_input: str