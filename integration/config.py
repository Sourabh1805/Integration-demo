import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


# Define a function to dynamically determine the .env file
def get_dotenv_file():
    # Try to get the ENV variable from the environment

    env = os.getenv("ENV", "dev").lower()  # Default to 'dev' if ENV is not set

    if env == "test":
        return "integration/.env.test"
    elif env == "dev":
        return "integration/.env.dev"
    else:
        raise ValueError(f"Unsupported ENV value: {env}. Expected 'dev' or 'test'.")


# Dynamically load the appropriate .env file
dotenv_file = get_dotenv_file()
load_dotenv(dotenv_file)

# Debugging: Print the loaded ENV for confirmation
# print(f"Loaded ENV: {os.getenv('ENV')} from {dotenv_file}")


# Define configuration using Pydantic's BaseSettings
class Config(BaseSettings):
    ENV: str = "dev"  # Default value if ENV is not set
    SQLALCHEMY_DATABASE_URI: str
    BIG_CHAT_API: str
    OUR_API: str

    class Config:
        env_file = dotenv_file  # Specify the dynamically determined .env file


# Singleton instance for global use
settings = Config()

# Debugging: Print the loaded settings for confirmation
# print(f"Settings: ENV={settings.ENV}, DB_URI={settings.SQLALCHEMY_DATABASE_URI}")
