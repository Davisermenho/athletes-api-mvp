"""Pydantic models for Athlete payloads.

These models mirror the canonical athlete header defined in the project.
Enums are provided for position fields to ensure a stable contract.
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import date, datetime


class MainAttackPosition(str, Enum):
    armadora_central = "armadora_central"
    lateral_esquerda = "lateral_esquerda"
    lateral_direita = "lateral_direita"
    ponta_esquerda = "ponta_esquerda"
    ponta_direita = "ponta_direita"
    pivo = "pivo"


class SecondaryAttackPosition(str, Enum):
    central = "central"
    lateral_esquerda = "lateral_esquerda"
    lateral_direita = "lateral_direita"
    ponta_esquerda = "ponta_esquerda"
    ponta_direita = "ponta_direita"
    pivo = "pivo"


class MainDefensivePosition(str, Enum):
    _1_defensora = "1_defensora"
    _2_defensora = "2_defensora"
    defensora_base = "defensora_base"
    goleira = "goleira"
    defensora_avancada = "defensora_avancada"


class SecondaryDefensivePosition(str, Enum):
    _1_defensora = "1_defensora"
    _2_defensora = "2_defensora"
    defensora_base = "defensora_base"
    goleira = "goleira"
    defensora_avancada = "defensora_avancada"


class AthleteBase(BaseModel):
    athlete_id: str = Field(..., description="Business identifier for the athlete (unique).")
    row_uuid: Optional[UUID] = Field(None, description="Row UUID (gen_random_uuid()).")
    full_name: str = Field(..., description="Full name of the athlete.")
    nickname: Optional[str] = None
    birth_date: Optional[date] = None
    age_display: Optional[str] = None
    category: Optional[str] = None
    main_attack_position: Optional[MainAttackPosition] = Field(None)
    secondary_attack_position: Optional[SecondaryAttackPosition] = Field(None)
    main_defensive_position: Optional[MainDefensivePosition] = Field(None)
    secondary_defensive_position: Optional[SecondaryDefensivePosition] = Field(None)
    jersey_number: Optional[int] = Field(None, ge=0)
    date_joined: Optional[date] = None
    date_left: Optional[date] = None
    active_flag: Optional[bool] = Field(True)
    height_cm: Optional[int] = Field(None, ge=0)
    weight_kg: Optional[float] = Field(None, ge=0)
    medical_notes: Optional[str] = None
    social_notes: Optional[str] = None
    physical_notes: Optional[str] = None
    mental_notes: Optional[str] = None
    external_reference: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_sync_at: Optional[datetime] = None


class AthleteCreate(AthleteBase):
    """Model used when creating/upserting an athlete from client input.

    Required fields: `athlete_id`, `full_name`.
    """
    athlete_id: str
    full_name: str


class AthleteRead(AthleteBase):
    id: int = Field(..., description="Internal DB id")

    # Support pydantic v1 (`Config.orm_mode`) and v2 (`model_config`) so this
    # model works in either environment. The project may use pydantic v2; keep
    # both for compatibility during migration.
    class Config:
        orm_mode = True

    model_config = {"from_attributes": True}
