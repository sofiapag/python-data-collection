from fastapi import FastAPI, HTTPException, status
from sqlmodel import select, Session

import db_internal
from models import User, Feature, CollectionMethod, UserInputTable

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


@app.get("/features", response_model=list[Feature])
async def get_features():
    with Session(db_internal.engine) as session:
        statement = select(Feature)
        results = session.execute(statement)
        results = list(i[0] for i in results.all())
    if len(results) == 0:
        return []
    return results

@app.post("/features", status_code=status.HTTP_201_CREATED, response_model=Feature)
async def create_feature(feature: Feature):
    if (
        (feature.collectionMethod == CollectionMethod.SELECTOR) and
        (not feature.possibleValues)
    ):
        raise HTTPException(status_code=422, detail="selector features must have possible values")
    if (
        (feature.collectionMethod == CollectionMethod.SLIDER) and
        ((not feature.minValue) or (not feature.maxValue))
    ):
        raise HTTPException(status_code=422, detail="slider features must have min and max values")

    with Session(db_internal.engine) as session:
        session.add(feature)
        session.commit()
        session.refresh(feature)
        return feature

@app.delete("/features/{feature_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_feature(feature_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(Feature, feature_id)
        if not row:
            raise HTTPException(status_code=404, detail="feature_id not found")
        session.delete(row)
        session.commit()
        return

@app.get("/userInputTables", response_model=list[UserInputTable])
async def get_user_input_tables():
    with Session(db_internal.engine) as session:
        statement = select(UserInputTable)
        results = session.execute(statement)
        results = list(i[0] for i in results.all())

    if len(results) == 0:
        return []
    return results

@app.post("/userInputTables", status_code=status.HTTP_201_CREATED, response_model=UserInputTable)
async def create_user_input_table(userInputTable: UserInputTable):
    with Session(db_internal.engine) as session:
        session.add(userInputTable)
        session.commit()
        session.refresh(userInputTable)
        return userInputTable

@app.delete("/userInputTables/{userInputTable_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_input_table(userInputTable_id: int):
    with Session(db_internal.engine) as session:
        row = session.get(UserInputTable, userInputTable_id)
        if not row:
            raise HTTPException(status_code=404, detail="userInputTable_id not found")
        session.delete(row)
        session.commit()
        return
