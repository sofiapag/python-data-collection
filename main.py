from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel
from sqlmodel import select, Session

import db_internal
from models import Crop, User

app = FastAPI()


class Message(BaseModel):
    detail: str


@app.on_event("startup")
async def startup_event():
    db_internal.create_db()


@app.get("/users", response_model=list[User])
async def get_users():
    with Session(db_internal.engine) as session:
        statement = select(User)
        results = session.execute(statement)
        results = list(i[0] for i in results.all())
    return results


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def delete_user(user_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(User, user_id)
        if not row:
            raise HTTPException(status_code=404, detail="user_id not found")
        session.delete(row)
        session.commit()
        return


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(user: User):
    with Session(db_internal.engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.delete(
    "/crops/{crop_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def delete_crop(crop_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(Crop, crop_id)
        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"crop_id {crop_id} not found",
            )
        session.delete(row)
        session.commit()
        return


@app.post(
    "/crops",
    status_code=status.HTTP_201_CREATED,
    response_model=Crop,
    responses={status.HTTP_400_BAD_REQUEST: {"model": Message}},
)
async def create_crop(crop: Crop):
    if not crop.tilled and crop.tillage_depth and crop.tillage_depth > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Field is not tilled and should not have tillage_depth",
        )

    with Session(db_internal.engine) as session:
        session.add(crop)
        session.commit()
        session.refresh(crop)
        return crop


@app.get(
    "/crops/{crop_id}",
    status_code=status.HTTP_200_OK,
    response_model=Crop,
    responses={status.HTTP_404_NOT_FOUND: {"model": Message}},
)
async def get_crop(crop_id: int):
    with Session(db_internal.engine) as session:
        statement = select(Crop).where(Crop.id == crop_id)
        result = session.execute(statement).first()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"crop_id {crop_id} not found"
        )
    return result[0]


@app.get("/crops", status_code=status.HTTP_200_OK, response_model=list[Crop])
async def get_crops(limit: int = Query(10, le=100), offset: int = 0):
    with Session(db_internal.engine) as session:
        statement = select(Crop).limit(limit).offset(offset)
        results = session.execute(statement)
        results = list(i[0] for i in results.all())
    return results
