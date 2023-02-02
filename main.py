from fastapi import FastAPI, HTTPException, status
from sqlmodel import select, Session

import db_internal
from models import Crop, User

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    db_internal.create_db()


@app.get("/users", response_model=list[User])
async def get_users():
    with Session(db_internal.engine) as session:
        statement = select(User)
        results = session.execute(statement)
        results = list(i[0] for i in results.all())
    if len(results) == 0:
        return []
    return results


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.delete("/crops/{crop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_crop(crop_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(Crop, crop_id)
        if not row:
            raise HTTPException(status_code=404, detail=f"crop_id {crop_id} not found")
        session.delete(row)
        session.commit()
        return


@app.post("/crops", status_code=status.HTTP_201_CREATED, response_model=Crop)
async def create_crop(crop: Crop):
    if not crop.tilled:
        crop.tillage_depth = None

    with Session(db_internal.engine) as session:
        session.add(crop)
        session.commit()
        session.refresh(crop)
        return crop
