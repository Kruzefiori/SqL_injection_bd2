from infrastructure.databases.SQL.pg_alchemy import SqlDB
from infrastructure.databases.SQL.psycopg import PsycopgSqlDB

Base = SqlDB().get_base()


class ModelGeneric(Base):
    __abstract__ = True

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class ModelGenericInjection(Base):
    __abstract__ = True

    def to_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

