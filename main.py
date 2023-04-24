from urllib import response
from fastapi import Depends, FastAPI, HTTPException

import crud, models, schemas
from database import SessionLocal, engine
from sqlalchemy.orm import Session

from uuid import UUID
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=schemas.Users)
def read_objects(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    # if user is None:
    #     raise HTTPException(status_code=404, detail="Item not found")

    # print(users.__dict__)
    # print(users[0].id)
    # print(users[0].city)
    # print(users[1])
    print(users)
    return {"users": users}
    # return {**users.__dict__}

    # return {"users": users}

@app.get("/user/{id}", response_model=schemas.BaseUser)
def get_user(id: UUID, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, id=id)
    if not user:
            raise HTTPException(status_code=400, detail="FILE/FOLDER already registered")
    return {**user.__dict__}

@app.get("/numbers", response_model=schemas.Numbers)
def read_numbers(db: Session = Depends(get_db)):
    numbers = crud.get_numbers(db=db)
    print(numbers[0].__dict__)
    return {"numbers": numbers}
    return {**numbers.__dict__}

@app.get("/contracts", response_model=schemas.Contracts)
def read_contracts(db: Session = Depends(get_db)):
    contracts = crud.get_contracts(db=db)
    return {"contracts": contracts}

@app.get("/tarifs_mobile", response_model=schemas.TarifsMobile)
def read_tarifs_mobile(db: Session = Depends(get_db)):
    tarifs = crud.get_tarifs_mobile(db=db)
    return {"tarifs": tarifs}


@app.post("/imports", response_model=schemas.UsersInput)
def create_user(items: schemas.UsersInput, db: Session = Depends(get_db)):
    for i in items.users:
        db_object = crud.get_user(db=db, id=i.id)
        print(db_object)
        if db_object:
            raise HTTPException(status_code=400, detail="FILE/FOLDER already registered")
    for i in items.users:
        crud.create_user(db=db, object=i)
    return {**items.__dict__}

@app.delete("/user/{id}")
def delete_user(id: UUID, date: datetime.date, db: Session = Depends(get_db)):
    db_object = crud.get_user(db=db, id=id)
    if  not db_object:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_user(db=db, id=id)
    return "Удаление прошло успешно"