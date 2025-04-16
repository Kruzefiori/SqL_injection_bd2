from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Env:
    app_cors_origins: str = getenv("APP_CORS_ORIGINS", "*")
    app_cors_methods: str = getenv("APP_CORS_METHODS", "GET,POST")
    app_cors_headers: str = getenv("APP_CORS_HEADERS", "Content-Type")
    sql_db_uri: str = getenv(
        "SQL_DB_URI", "postgresql://unifei:unifei@localhost:8081/unifei"
    )
    sql_db_provider: str = getenv("SQL_DB_PROVIDER", "postgresql")


env = Env()
