from sqlalchemy.orm import Session
from sqlalchemy.sql import func
import models
import schemas


def get_users(db: Session):
    users = db.query(models.User).all()
    cost_options_users = db.query(func.sum(models.Options_mobile.cost).label("sumcost")).join(models.association_number_option).join(models.Numbers_mobile).join(models.User).filter(models.association_number_option.c.option_id == models.Options_mobile.id).filter(models.Numbers_mobile.id == models.association_number_option.c.number_id).filter(models.User.id == models.Numbers_mobile.user_id).group_by(models.User.id)
    for item in users:
        numbers = db.query(models.Numbers_mobile.number, models.Tarifs_mobile.Cost).filter(models.Tarifs_mobile.id == models.Numbers_mobile.tarif_id).filter(models.Numbers_mobile.user_id == item.id).all()
        cost = 0
        item.__dict__["numbers"] = []
        for num in numbers:
            item.__dict__["numbers"].append(num.number)
            cost += num.Cost
        cost_option = cost_options_users.filter(models.User.id == item.id).first()
        if cost_option is not None:
            cost += cost_option.sumcost
        item.__dict__["pay"] = cost
    return users


def get_numbers(db: Session):
    res = db.query(models.Numbers_mobile).all()
    return res


def get_user(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user


def get_tarifs_mobile(db: Session):
    tarifs = db.query(models.Tarifs_mobile).all()
    for item in tarifs:
        item.__dict__["number_of_numbers"] = 0
    tarif_id_groups = db.query(models.Numbers_mobile.tarif_id, func.count(models.Numbers_mobile.tarif_id)).join(models.Tarifs_mobile, models.Numbers_mobile.tarif_id == models.Tarifs_mobile.id).group_by(models.Numbers_mobile.tarif_id).all()
    for row in tarif_id_groups:
        tarifs[row[0] - 1].__dict__["number_of_numbers"] = row[1]
    return tarifs


def get_option(db: Session, name: str):
    option = db.query(models.Options_mobile).filter(models.Options_mobile.name == name).all()
    return option


def get_option_by_id(db: Session, id: int):
    option = db.query(models.Options_mobile).filter(models.Options_mobile.id == id).all()
    return option


def create_user(db: Session, object: schemas.UsersInput):
    user = models.User(
        id=object.id,
        first_name=object.first_name,
        last_name=object.last_name,
        middle_name=object.middle_name,
        age=object.age,
        region=object.region,
        city=object.city,
        street=object.street,
        index=object.index)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_number(db: Session, object: schemas.Numbers):
    number = models.Numbers_mobile(number=object.number,
                                   tarif_id=object.tarif_id,
                                   user_id=object.user_id
                                   )
    db.add(number)
    db.commit()
    db.refresh(number)
    return number


def create_option_mobile(db: Session, object: schemas.Options_mobile):
    option = models.Options_mobile(name=object.name,
                                   desc=object.desc,
                                   cost=object.cost
                                   )
    db.add(option)
    db.commit()
    db.refresh(option)
    return option


def create_numbers_options(db: Session, number: str, option_id: int):
    number_id = db.query(models.Numbers_mobile.id).filter(models.Numbers_mobile.number == number).first()
    number_id = number_id[0]
    number_option = models.association_number_option.insert().values(option_id=option_id, number_id=number_id)
    db.execute(number_option)
    db.commit()
    return number_option


def get_numbers_options(db: Session, number: str, id: int):
    res = db.query(models.association_number_option).join(models.Numbers_mobile).filter(models.association_number_option.c.option_id == models.Numbers_mobile.id).filter(models.association_number_option.c.option_id == id).filter(models.Numbers_mobile.number == number).first()
    return res


def delete_user(db: Session, id: int):
    object = db.query(models.User).filter(models.User.id == id)
    object.delete()
    db.commit()
    return True


def count_number_age(db: Session, agemin: int, agemax: int):
    count = db.query(func.count(models.Numbers_mobile.id)).join(models.User).filter(models.Numbers_mobile.user_id == models.User.id).filter(models.User.age <= agemax).filter(models.User.age >= agemin).all()
    return count[0][0]


def stat(db: Session, agemin: int, agemax: int):
    c = db.query(models.Tarifs_mobile.name.label("name_tarif"), func.count(models.Numbers_mobile.tarif_id).label("percent")).join(models.User).filter(models.Numbers_mobile.tarif_id == models.Tarifs_mobile.id).filter(models.Numbers_mobile.user_id == models.User.id).filter(models.User.age <= agemax).filter(models.User.age >= agemin).group_by(models.Tarifs_mobile.name).all()
    return [r._asdict() for r in c]


def get_number(db: Session, number: str):
    num = db.query(models.Numbers_mobile).filter(models.Numbers_mobile.number == number).all()
    return num
