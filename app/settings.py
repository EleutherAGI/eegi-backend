class EmailSettings:
    """ Email Settings"""
    EMAIL_RESET_TOKEN_EXPIRE_HOURS = 24
    EMAIL_ID = ""
    EMAIL_PASSWORD = ""
    SMTP_SERVER = ""
    SMTP_PORT = 465


class DBSettings:
    """ Database Configuration"""
    DATABASE = "postgres"
    POSTGRES_SERVER = "localhost"
    POSTGRES_PORT = "5432"
    POSTGRES_USER = ""
    POSTGRES_PASSWORD = ""
    POSTGRES_DB = "postgres"
    POSTGRES_ADAPTER = "psycopg2"

    SQLALCHEMY_DATABASE_URL = DATABASE + '+' + POSTGRES_ADAPTER + '://' + \
                              POSTGRES_USER + ':' + POSTGRES_PASSWORD + '@' + POSTGRES_SERVER + ':' + \
                              POSTGRES_PORT + '/' + POSTGRES_DB


class ProjectSettings:
    PROJECT_NAME = "EEGI-backend"
    PROJECT_DESCRIPTION = "an api interface for gathering human preferences"
    API_VERSION = "1.0.0"
    API_VERSION_PATH = "/api/v1"
    SERVER_HOST = "https://localhost:8088/api/v1/"
    BACKEND_CORS_ORIGINS = ["*"]
    ACCESS_TOKEN_EXPIRE_MINUTES = 300
    SESSION_TOKEN_EXPIRE_SECONDS = 43200