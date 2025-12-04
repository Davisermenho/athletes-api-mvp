from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from uuid import UUID
from datetime import date, datetime


class AthleteBase(BaseModel):
    athlete_id: str
    row_uuid: Optional[UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    dob: Optional[date]
    country_code: Optional[str]
    category: Optional[str]
    gender: Optional[str]
    metadata: Optional[Dict] = {}


class AthleteCreate(AthleteBase):
    pass


class AthleteRead(AthleteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
