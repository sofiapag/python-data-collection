from typing import List, Optional
from enum import Enum

from sqlmodel import Field, SQLModel

# Indicates to the UI what type of input field to use to collect the data
# Can be expanded to include others
class CollectionMethod(Enum):
    SELECTOR = 'selector'
    TEXTBOX = 'textbox'
    DATE = 'date'
    NUMBER = 'number'
    SLIDER = 'slider'

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

class Feature(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    collectionMethod: CollectionMethod
    possibleValues: Optional[str]
    minValue: Optional[float]
    maxValue: Optional[float]
    defaultValue: Optional[str]
    info: Optional[str]

class UserInputTable(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    features: str
    startYear: int
    endYear: int
