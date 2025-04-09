from pydantic import BaseModel
#from sqlalchemy import Column, Integer, String, DateTime

from infrastructure.databases.SQL.pg_alchemy import SqlDB

Base = SqlDB().get_base()

class OrderDB(Base):
    pass

class OrderSchema(BaseModel):
    __tablename__ = 'orders' # VOU MUDAR DPS
    pass
