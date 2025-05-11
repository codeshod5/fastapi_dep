# from sqlalchemy import Column, String, Integer
# from sqlalchemy.ext.declarative import declarative_base
# from pydantic import BaseModel,EmailStr
# from fastapi import FastAPI,Depends
# from app.database import get_session
# from sqlmodel import Session


# # from sqlalchemy.orm import session

# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     email = Column(String(100), unique=True)  # Only basic constraints
# class Usercheck(BaseModel):
#     email:EmailStr

# app = FastAPI()
# @app.post('writee/')
# def writee(user:User,sess:Session=Depends(get_session)):
#     sess.add(user)
#     sess.commit()
#     return "message sendt"

from sqlmodel import SQLModel,Field
from typing import List 
from datetime import datetime
from pydantic import BaseModel,EmailStr
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String

class Routes_and_Areas(SQLModel,table=True):
    r_id:int=Field(primary_key=True,index=True)
    routes_id: int =Field(index=True,unique=True)
    areas: List[str] = Field(sa_type=ARRAY(String))
    timing:datetime|None= Field(index=True)

class Buses_and_Routes(SQLModel,table=True):
    b_id:int=Field(primary_key=True,index=True)
    bus_id:int=Field(index=True)
    routes_id:int=Field(index=True,unique=True)

class Drivers(SQLModel,table=True):
    d_id:int = Field(primary_key=True,index=True)
    routes_id:int = Field(index=True,unique=True)
    bus_id:int = Field(index=True,unique=True)

class Clients(SQLModel,table=True):
    c_id:int=Field(primary_key=True,index=True)
    username:str = Field(max_length=50,index=True)
    email:str=Field(index=True)
    password:str 
    routes_id:int|None = Field(index=True)
    bus_id:int|None = Field(index=True)

class Client_check(BaseModel):
    username:str
    email:EmailStr
    password:str


