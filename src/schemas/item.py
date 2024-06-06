from typing import List, Optional

from pydantic import BaseModel

from .user import User


# Shared properties
class ItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    user_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Item(ItemInDBBase):
    user: User


# Additional properties stored in DB
class ItemInDB(ItemInDBBase):
    pass


# List of items to return via API
class ItemRows(BaseModel):
    data: List[Item]
    total: int
