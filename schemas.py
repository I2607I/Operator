from typing import List, Union
from pydantic import BaseModel, Field
import datetime
from uuid import UUID

class BaseUser(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    middle_name: str
    region: str
    city: str
    street: str
    index: str
    # numbers: Union[List[str], None] = []

class UserPlusNumbers(BaseUser):
    numbers: List[str]

    class Config:
        orm_mode = True

class Users(BaseModel):
    users: List[UserPlusNumbers]

    class Config:
        orm_mode = True
    
class UsersInput(BaseModel):
    users: List[BaseUser]
    date : datetime.date





class Number(BaseModel):
    id: int
    number: str
    tarif_id: int
    date: datetime.datetime
    user_id: UUID

    class Config:
        orm_mode = True

class Numbers(BaseModel):
    numbers: List[Number]

    class Config:
        orm_mode = True

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