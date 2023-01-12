from sqlmodel import create_engine, SQLModel

import models
from config import settings

sqlite_url = f"sqlite:///{settings.db_path}"
engine = create_engine(sqlite_url, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)
