from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from app.constants import MAX_LENGTH_NAME_PROJECT, MIN_LENGTH_DESCRIPTION_PROJECT, MIN_LENGTH_NAME_PROJECT


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH_NAME_PROJECT,
        max_length=MAX_LENGTH_NAME_PROJECT
    )
    description: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH_DESCRIPTION_PROJECT
    )
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ...,
        min_length=MIN_LENGTH_NAME_PROJECT,
        max_length=MAX_LENGTH_NAME_PROJECT
    )
    description: str = Field(
        ...,
        min_length=MIN_LENGTH_DESCRIPTION_PROJECT
    )
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass
