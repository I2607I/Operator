from sqlalchemy import Column, ForeignKey, Integer, String, Date, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Tarifs_mobile(Base):
    __tablename__ = "tarifs_mobile"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    desc = Column(String)
    GB = Column(Integer)
    SMS = Column(Integer)
    Time_our = Column(Integer)
    Time_their = Column(Integer)
    Cost = Column(Integer)
    numbers = relationship("Numbers_mobile")


association_number_option = Table(
    "association_number_option",
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column("option_id", ForeignKey("options_mobile.id")),
    Column("number_id", ForeignKey("numbers_mobile.id")),
)


class Options_mobile(Base):
    __tablename__ = "options_mobile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    desc = Column(String)
    cost = Column(Integer)


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    age = Column(Integer)
    region = Column(String)
    city = Column(String)
    street = Column(String)
    index = Column(String)
    numbers = relationship("Numbers_mobile")
    # contracts = relationship("Contracts_home_internet")


class Numbers_mobile(Base):
    __tablename__ = "numbers_mobile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(String)
    tarif_id = Column(Integer, ForeignKey("tarifs_mobile.id"))
    date = Column(Date(), default=datetime.today().strftime('%Y-%m-%d'))
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))

    option = relationship("Options_mobile", secondary=association_number_option, backref='numbers_mobile')
