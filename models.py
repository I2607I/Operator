from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.dialects.sqlite import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

# У пользователя может быть несколько номеров
# Каждый номер имеет свой тариф и свои услуги
# Пользователь может добавлять друзей и заходить в их личный кабинет без пароля
# У пользователя может быть несколько договоров на проводной Интернет
# Один договор - один адрес
# Каждый договор имеет свой тариф 




class Tarifs_mobile(Base):
    __tablename__ = "tarifs_mobile"

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    GB = Column(Integer)
    SMS = Column(Integer)
    Time_our = Column(Integer)
    Time_their = Column(Integer)
    Cost = Column(Integer)
    numbers = relationship("Numbers_mobile")



class Tarifs_home_internet(Base):
    __tablename__ = "tarifs_home_internet"

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    speed = Column(Integer)
    TV_channels = Column(Integer)
    cost = Column(Integer)
    contracts = relationship("Contracts_home_internet")


    

class Options_mobile(Base):
    __tablename__ = "options_mobile"

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    cost = Column(Integer)

class Options_home_internet(Base):
    __tablename__ = "options_home_internet"

    id = Column(Integer, primary_key=True)
    desc = Column(String)
    cost = Column(Integer)



class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    region = Column(String)
    city =Column(String)
    street = Column(String)
    index = Column(String)
    numbers = relationship("Numbers_mobile")
    contracts = relationship("Contracts_home_internet")

    # friends = 

class Numbers_mobile(Base):
    __tablename__ = "numbers_mobile"

    id = Column(Integer, primary_key=True)
    number = Column(String)
    tarif_id = Column(Integer, ForeignKey("tarifs_mobile.id"))
    # options = 
    date = Column(DateTime(), default=datetime.now)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))


class Contracts_home_internet(Base):
    __tablename__ = "contracts_home_internet"

    id = Column(Integer, primary_key=True)
    contract = Column(String)
    tarif_id = Column(Integer, ForeignKey("tarifs_home_internet.id"))
    # options =
    date = Column(DateTime(), default=datetime.now)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
















