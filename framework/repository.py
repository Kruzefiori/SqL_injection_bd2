from infrastructure.databases.SQL.pg_alchemy import SqlDB
from infrastructure.databases.SQL.psycopg import PsycopgSqlDB
from dataclasses import dataclass
from typing import Generic, TypeVar, Union
from sqlalchemy import inspect
from sqlalchemy.orm import Session

T = TypeVar("T")

@dataclass
class Field(Generic[T]):
    name: str
    value: T


class GenericRepository:
    def __init__(self, model_class):
        self.db = SqlDB().get_db()
        if self.db is None:
            raise ValueError("Database not initialized")
        self.model_class = model_class

    """
    def create(self, item):
        session = self._create_a_session()
        try:
            session.add(item)
            session.commit()
            session.refresh(item)
            return item
        except Exception as e:
            session.rollback()
            raise RuntimeError(
                f"Error creating {self.model_class.__name__}: {e}"
            ) from e
        finally:
            session.close()
    """

    def delete(self, item):
        session = self._create_a_session()
        try:
            session.delete(item)
            session.commit()
            return item
        except Exception as e:
            session.rollback()
            raise RuntimeError(
                f"Error deleting {self.model_class.__name__}: {e}"
            ) from e
        finally:
            session.close()

    def delete_by_id(self, id_: Union[int, str, tuple, dict]):
        item = self.get_by_id(id_)
        if not item:
            raise ValueError(f"{self.model_class.__name__} with ID {id_} not found")
        return self.delete(item)

    def _id_name(self) -> list[str]:
        return [key.name for key in inspect(self.model_class).primary_key]

    def get_all(self, page: int = 1, page_size: int = 10):
        session = self._create_a_session()
        offset = (page - 1) * page_size
        try:
            return session.query(self.model_class).offset(offset).limit(page_size).all()
        except Exception as e:
            session.rollback()
            raise RuntimeError(
                f"Error fetching all {self.model_class.__name__}: {e}"
            ) from e
        finally:
            session.close()

    def get_by_field(self, field: Field):
        return self.get_by_fields([field])

    def get_by_fields(self, fields: list[Field]):
        session = self._create_a_session()
        try:
            query = session.query(self.model_class)
            for field in fields:
                column = getattr(self.model_class, field.name[0], None)
                if column is None:
                    raise AttributeError(
                        f"Model {self.model_class.__name__} has no field named '{field.name}'"
                    )
                query = query.filter(column == field.value)
            return query.first()
        except Exception as e:
            session.rollback()
            field_details = ", ".join(f"{f.name}={f.value}" for f in fields)
            raise RuntimeError(
                f"Error fetching {self.model_class.__name__} by fields [{field_details}]: {e}"
            ) from e
        finally:
            session.close()

    def get_by_id(self, id_: Union[int, str, tuple, dict]):
        pk_names = self._id_name()

        if isinstance(id_, dict):
            fields = [Field(name=k, value=v) for k, v in id_.items()]
        elif isinstance(id_, tuple):
            if len(pk_names) != len(id_):
                raise ValueError(
                    f"Expected {len(pk_names)} values for composite key, got {len(id_)}"
                )
            fields = [
                Field(name=pk_names[i], value=id_[i]) for i in range(len(pk_names))
            ]
        else:
            fields = [Field(name=pk_names[0], value=id_)]

        return self.get_by_fields(fields)

    def update(self, item):
        session = self._create_a_session()
        try:
            session.merge(item)
            session.commit()
            return item
        except Exception as e:
            session.rollback()
            raise RuntimeError(
                f"Error updating {self.model_class.__name__}: {e}"
            ) from e
        finally:
            session.close()

    def _create_a_session(self) -> Session:
        if self.db is None:
            raise ValueError("Database not initialized")
        session = self.db.get_session()
        if session is None:
            raise ValueError("An error occurred while connecting to the database")
        return session

###===========================================================================================
###===========================================================================================
###===========================================================================================
### PSYCOPG
###===========================================================================================
###===========================================================================================
###===========================================================================================

class GenericRepositoryInjection:
    # Write this class the same as the class above but providing a framework to perform queries
    # using psycopg instead of sqlalchemy

    def __init__(self, model_class):
        self.db = PsycopgSqlDB().get_db()
        if self.db is None:
            raise ValueError("Database not initialized")
        self.model_class = model_class
        self.connection = self.db.get_connection()
        self.cursor = self.db.get_cursor()
        

    def refresh_cursor (self):
        if self.cursor is None or self.connection is None:
            self.db.get_connection()
            self.db.get_cursor()

    """
    def create(self, item):
        self.refresh_cursor()
        try:
            columns = ", ".join(item.keys())
            values = ", ".join([f"%({key})s" for key in item.keys()])
            query = f"INSERT INTO {self.model_class.__tablename__} ({columns}) VALUES ({values}) RETURNING *"
            self.cursor.execute(query, item)
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            raise RuntimeError(
                f"Error creating {self.model_class.__name__}: {e}"
            ) from e
    """

    def delete(self, item):
        self.refresh_cursor()
        try:
            query = f"DELETE FROM {self.model_class.__tablename__} WHERE id = %s"
            self.cursor.execute(query, (item.id,))
            self.connection.commit()
            return item
        except Exception as e:
            raise RuntimeError(
                f"Error deleting {self.model_class.__name__}: {e}"
            ) from e

    def delete_by_id(self, id_):
        item = self.get_by_id(id_)
        if not item:
            raise ValueError(f"{self.model_class.__name__} with ID {id_} not found")
        return self.delete(item)

    def _id_name(self) -> list[str]:
        return [key.name for key in inspect(self.model_class).primary_key]

    def get_all(self, page: int = 1, page_size: int = 10):
        self.refresh_cursor()
        offset = (page - 1) * page_size
        try:
            query = f"SELECT * FROM {self.model_class.__tablename__} LIMIT %s OFFSET %s"
            self.cursor.execute(query, (page_size, offset))
            results = self.cursor.fetchall()
            if results:
                column_names = [desc[0] for desc in self.cursor.description]
                return [dict(zip(column_names, row)) for row in results]
            return []
        except Exception as e:
            raise RuntimeError(
                f"Error fetching all {self.model_class.__name__}: {e}"
            ) from e

    def get_by_field(self, field: Field):
        return self.get_by_fields([field])

    def get_by_fields(self, fields: list[Field]):
        self.refresh_cursor()
        try:
            # Construção da query Where com os placeholders de values (%s)
            where_clause = " AND ".join([f"{field.name[0]} = %s" for field in fields])
            query = f"SELECT * FROM {self.model_class.__tablename__} WHERE {where_clause}"
            
            # Extrair o valor do campo para ser substituído no placeholder
            values = [field.value for field in fields]
            
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            if result:
                # Mapeia os resultados para um dicionário
                column_names = [desc[0] for desc in self.cursor.description]
                return dict(zip(column_names, result))
            return None
        except Exception as e:
            field_details = ", ".join(f"{f.name}={f.value}" for f in fields)
            raise RuntimeError(
                f"Error fetching {self.model_class.__name__} by fields [{field_details}]: {e}"
            ) from e

    def get_by_id(self, id_):
        pk_names = self._id_name()

        if isinstance(id_, dict):
            fields = [Field(name=k, value=v) for k, v in id_.items()]
        elif isinstance(id_, tuple):
            if len(pk_names) != len(id_):
                raise ValueError(
                    f"Expected {len(pk_names)} values for composite key, got {len(id_)}"
                )
            fields = [
                Field(name=pk_names[i], value=id_[i]) for i in range(len(pk_names))
            ]
        else:
            fields = [Field(name=pk_names[0], value=id_)]

        return self.get_by_fields(fields)

    def update(self, item):
        self.refresh_cursor()
        try:
            columns = ", ".join([f"{key} = %s" for key in item.keys()])
            query = f"UPDATE {self.model_class.__tablename__} SET {columns} WHERE id = %s RETURNING *"
            values = list(item.values())
            values.append(item.id)
            self.cursor.execute(query, values)
            self.connection.commit()
            result = self.cursor.fetchone()
            if result:
                # Mapeia os resultados para um dicionário
                column_names = [desc[0] for desc in self.cursor.description]
                return dict(zip(column_names, result))
            return None
        except Exception as e:
            raise RuntimeError(
                f"Error updating {self.model_class.__name__}: {e}"
            ) from e

    def _create_a_session(self):
        if self.db is None:
            raise ValueError("Database not initialized")
        self.refresh_cursor()
        session = self.db.get_cursor()
        if session is None:
            raise ValueError("An error occurred while connecting to the database")
        return session
