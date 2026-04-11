#This code is the user input checker, only allows specific type of data to be sent to db.

from pydantic import BaseModel, EmailStr # Used to enfore strict datatypes
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str 
    role: str 
    email: EmailStr # EmailStr checks if the value is email or not

class UserResponse(BaseModel):
    id: int 
    name: str 
    role: str 
    email: EmailStr
    created_at: datetime # Return the timestamp of the request

class FoodListingCreate(BaseModel):
    title: str 
    description: Optional[str]=None # This value is not compulsory, else None
    qty: str 
    provider_id: int

class FoodListingResponse(BaseModel):
    id: int
    title: str 
    description: Optional[str]=None
    qty: str 
    status: str 
    provider_id: int
    claimed_id: Optional[int]=None
    created_at: datetime

     
