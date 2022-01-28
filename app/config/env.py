from pydantic import BaseSettings

ONE_DAY_IN_MINUTES = 60 * 24


class EnvironmentVariables(BaseSettings):
    DB_URL: str
    ACCESS_TOKEN_EXPIRY_IN_MINUTES: int = ONE_DAY_IN_MINUTES

    class Config:
        env_file = ".env"


environment_variables = EnvironmentVariables()
