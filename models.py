from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class CropType(str, Enum):
    CORN: str = "corn"
    WHEAT: str = "wheat"
    BARLEY: str = "barkley"
    HOPS: str = "hops"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    crops: list["Crop"] = Relationship(back_populates="user")


class Crop(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    year: int = Field(ge=1000, le=9999)
    crop_type: CropType
    tilled: bool
    tillage_depth: Optional[float] = Field(ge=0, lt=10)
    comments: str

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="crops")
