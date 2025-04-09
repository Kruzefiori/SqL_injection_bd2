from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import env


class SqlDB:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SqlDB, cls).__new__(cls)
            cls._instance.initialize()
        return cls._instance

    def initialize(self):
        self.engine = create_engine(
            url=env.sql_db_uri,
            pool_pre_ping=True,
        )

        self.Base = declarative_base()
        self.Metadata = MetaData()

    def get_session(self):
        session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
            expire_on_commit=True
        )()

        return session

    def get_base(self):
        return self.Base

    def get_metadata(self):
        return self.Metadata

    def get_db(self):
        return self._instance

