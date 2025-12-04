from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from uuid import UUID
from datetime import date, datetime


class AthleteBase(BaseModel):
    athlete_id: str
    row_uuid: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    dob: Optional[date] = None
    country_code: Optional[str] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    metadata: Dict = Field(default_factory=dict)


class AthleteCreate(AthleteBase):
    pass


class AthleteRead(AthleteBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
