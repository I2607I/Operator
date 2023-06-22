from typing import List
from pydantic import BaseModel
import datetime
from uuid import UUID


class BaseUser(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str
    age: int
    region: str
    city: str
    street: str
    index: str


class UserPlusNumbers(BaseUser):
    numbers: List[str]
    pay: int

    class Config:
        orm_mode = True


class Users(BaseModel):
    users: List[UserPlusNumbers]

    class Config:
        orm_mode = True


class UsersInput(BaseModel):
    users: List[BaseUser]
    date: datetime.date


class Number(BaseModel):
    number: str
    tarif_id: int
    user_id: UUID

    class Config:
        orm_mode = True


class Numbers(BaseModel):
    numbers: List[Number]

    class Config:
        orm_mode = True


class Option_mobile(BaseModel):
    name: str
    desc: str
    cost: int


class Options_mobile(BaseModel):
    options: List[Option_mobile]


class Number_options(BaseModel):
    number: str
    id_options: List[int]


class Numbers_options(BaseModel):
    numbers_with_options: List[Number_options]


class Contract(BaseModel):
    id: int
    contract: str
    tarif_id: int
    date: datetime.datetime
    user_id: UUID

    class Config:
        orm_mode = True


class Contracts(BaseModel):
    contracts: List[Contract]

    class Config:
        orm_mode = True


class TarifMobile(BaseModel):
    id: int
    name: str
    desc: str = None
    GB: int
    SMS: int
    Time_our: int
    Time_their: int
    Cost: int
    number_of_numbers: int

    class Config:
        orm_mode = True


class TarifsMobile(BaseModel):
    tarifs: List[TarifMobile]

    class Config:
        orm_mode = True


class Stat(BaseModel):
    name_tarif: str
    percent: float


class Stats(BaseModel):
    age: str
    stats_for_this_age: List[Stat]


class SuperStats(BaseModel):
    stats: List[Stats]
