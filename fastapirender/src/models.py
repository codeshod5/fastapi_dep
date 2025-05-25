from sqlmodel import SQLModel,Field
from typing import List 
from datetime import datetime
from pydantic import BaseModel,EmailStr
# from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String

class RouteAnArea(SQLModel,table=True):
    r_id:int|None=Field(primary_key=True)
    
    route_id:int
    area:str
    
class Driver(SQLModel,table=True):
    driver_id:int = Field(primary_key=True)
    driver_name:str
    driver_no:int
class Busesinfo(SQLModel,table=True):
    bus_id:int=Field(primary_key=True)
    bus_no:str =Field(unique=True)
   
    timming:datetime|None=None

# class BusAndRoute(SQLModel,table=True):
#     id:int= Field(primary_key=True)
#     bus_id:int = Field(foreign_key="busesinfo.bus_id")
#     route_id:int = Field(unique=True)
#     driver_id:int=Field(foreign_key="driver.driver_id")
#     timming:str|None=None

class BusAndRoute2(SQLModel,table=True):
    id:int|None = Field(primary_key=True)
    bus_id:int
    route_id:int = Field(unique=True)
    driver_id:int
    timming:str|None=None

class Client(SQLModel,table=True):
    c_id:int=Field(primary_key=True)
    username:str 
    email:str
    password:str
    area:str
    
    timing:str