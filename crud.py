from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy.sql import func



def get_users(db: Session):
    res = db.query(models.User).all()
    # print(res)
    # print(res[0].__dict__)
    for item in res:
        # item.__dict__["numbers"] = "QQQ"
        n = db.query(models.Numbers_mobile).filter(models.Numbers_mobile.user_id == item.__dict__['id'])
        # print(n.__dict__)
        # print(len(n))
        # n = list(n)
        # print(n)
        # if len(n) == 1:
        #     print(n[0].__dict__['number'])
        # s = []
        # for i in n:
        #     s.append(i.__dict__['number'])
        # item.__dict__["numbers"] = s
        item.__dict__["numbers"] = [i.__dict__['number'] for i in n]
        # print(s)
            
        # print(item.__dict__['id'])
    # print(res[0].__dict__)
    return res

def get_numbers(db: Session):
    res = db.query(models.Numbers_mobile).all()
    print(res)
    return res

def get_contracts(db: Session):
    res = db.query(models.Contracts_home_internet).all()
    return res

def get_user(db: Session, id: id):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user

def get_tarifs_mobile(db: Session):
    tarifs = db.query(models.Tarifs_mobile).all()
    # print(tarifs[0].__dict__)
    for i in tarifs:
        i.__dict__["number_of_numbers"] = 0
    # a = db.query(models.Tarifs_mobile, models.Numbers_mobile, models.Tarifs_mobile.id, func.count(models.Numbers_mobile.tarif_id)).group_by(models.Numbers_mobile.tarif_id).all()
    # b = a.filter(models.Tarifs_mobile.id == 1).all()
    # b = a.group_by(models.Numbers_mobile.tarif_id).all()
    # b = db.query(models.Numbers_mobile.tarif_id, func.count(models.Numbers_mobile.tarif_id), models.Tarifs_mobile.Cost).group_by(models.Numbers_mobile.tarif_id).all()
    a = db.query(models.Numbers_mobile.tarif_id, func.count(models.Numbers_mobile.tarif_id)).join(models.Tarifs_mobile, models.Numbers_mobile.tarif_id == models.Tarifs_mobile.id).group_by(models.Numbers_mobile.tarif_id).all()
    # b = db.query(models.Numbers_mobile.tarif_id, models.Numbers_mobile.number, models.Tarifs_mobile.Cost).join(models.Tarifs_mobile, models.Numbers_mobile.tarif_id == models.Tarifs_mobile.id).all()
    # for 
    # print(a.sort(key=a[i][0]))
    print(a)
    for row in a:
        # print(item, type(item))
        print(row.tarif_id)
        tarifs[row[0] - 1].__dict__["number_of_numbers"] = row[1]
    # print('\n', b)
    # print(b[0])
    return tarifs


def create_user(db: Session, object: schemas.UsersInput):
    user = models.User(id=object.id,
                            first_name=object.first_name, 
                            last_name=object.last_name, 
                            middle_name=object.middle_name, 
                            region=object.region,
                            city=object.city,
                            street=object.street,
                            index=object.index
                            )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, id: int):
    object = db.query(models.User).filter(models.User.id == id)
    object.delete()
    db.commit()
    return True
