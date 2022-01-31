from pydantic import BaseSettings

ONE_DAY_IN_MINUTES = 60 * 24


class EnvironmentVariables(BaseSettings):
    DB_URL: str
    ACCESS_TOKEN_EXPIRY_IN_MINUTES: int = ONE_DAY_IN_MINUTES
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    SESSION_SECRET_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


environment_variables = EnvironmentVariables()
