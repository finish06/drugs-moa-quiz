from pydantic import BaseModel
from typing import List, Optional


class MOA(BaseModel):
    """Mechanism of Action model"""
    moa: str


class Drug(BaseModel):
    """Drug model with generic name, brand name, and mechanism of action"""
    id: int
    generic_name: str
    brand_name: str
    moa: List[MOA]


class MOAResponse(BaseModel):
    """Response model for MOA list"""
    id: int
    moa: str
