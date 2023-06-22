from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import datetime
import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=schemas.Users)
def read_objects(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    return {"users": users}


@app.get("/user/{id}", response_model=schemas.BaseUser)
def get_user(id: UUID, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, id=id)
    if not user:
        raise HTTPException(status_code=400, detail="user not found")
    return {**user.__dict__}


@app.get("/numbers", response_model=schemas.Numbers)
def read_numbers(db: Session = Depends(get_db)):
    numbers = crud.get_numbers(db=db)
    return {"numbers": numbers}


@app.get("/tarifs_mobile", response_model=schemas.TarifsMobile)
def read_tarifs_mobile(db: Session = Depends(get_db)):
    tarifs = crud.get_tarifs_mobile(db=db)
    return {"tarifs": tarifs}


@app.post("/imports/users", response_model=schemas.UsersInput)
def create_user(items: schemas.UsersInput, db: Session = Depends(get_db)):
    for item in items.users:
        db_object = crud.get_user(db=db, id=item.id)
        if db_object:
            raise HTTPException(status_code=400, detail="user(s) already registered")
    for item in items.users:
        crud.create_user(db=db, object=item)
    return {**items.__dict__}


@app.post("/imports/numbers")
def create_numbers(items: schemas.Numbers, db: Session = Depends(get_db)):
    for item in items.numbers:
        if crud.get_number(db=db, number=item.number):
            raise HTTPException(status_code=400, detail="number(s) already registered")
    for item in items.numbers:
        crud.create_number(db=db, object=item)
    return {"success"}


@app.post("/imports/options_mobile")
def create_option_mobile(items: schemas.Options_mobile, db: Session = Depends(get_db)):
    for item in items.options:
        if crud.get_option(db=db, name=item.name):
            raise HTTPException(status_code=400, detail="option(s) already registered")
    for item in items.options:
        crud.create_option_mobile(db=db, object=item)
    return {"success"}


@app.post("/imports/numbers_options")
def create_numbers_options(items: schemas.Numbers_options, db: Session = Depends(get_db)):
    for item in items.numbers_with_options:
        if not crud.get_number(db=db, number=item.number):
            raise HTTPException(status_code=400, detail="number not found")
        for id in item.id_options:
            if not crud.get_option_by_id(db=db, id=id):
                raise HTTPException(status_code=400, detail="option not found")
            if crud.get_numbers_options(db=db, number=item.number, id=id):
                raise HTTPException(status_code=400, detail="option with number already registred")
    for item in items.numbers_with_options:
        for id in item.id_options:
            crud.create_numbers_options(db=db, number=item.number, option_id=id)
    return {"success"}


@app.delete("/user/{id}")
def delete_user(id: UUID, date: datetime.date, db: Session = Depends(get_db)):
    db_object = crud.get_user(db=db, id=id)
    if not db_object:
        raise HTTPException(status_code=404, detail="Item not found")
    crud.delete_user(db=db, id=id)
    return "Successful deletion"


@app.get("/stat/age", response_model=schemas.SuperStats)
def stat_age(db: Session = Depends(get_db)):
    list_age = [(18, 27), (28, 37), (38, 47), (48, 57), (58, 67), (68, 1000)]
    answer = []
    for age in list_age:
        count_numbers_age = crud.count_number_age(db=db, agemin=age[0], agemax=age[1])
        count_numbers_age_group = crud.stat(db=db, agemin=age[0], agemax=age[1])
        for item in count_numbers_age_group:
            item["percent"] /= count_numbers_age
            item["percent"] *= 100
            item["percent"] = round(item["percent"], 1)
        age_str = f"{age[0]}-{age[1]}"
        if age[1] == 1000:
            age_str = f"{age[0]} and more"
        answer.append({"age": age_str,
                       "stats_for_this_age": count_numbers_age_group})
    return {"stats": answer}
