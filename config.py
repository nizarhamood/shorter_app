# shortener_app/config.py

from functools import lru_cache

'''
The BasicSettings class is used as a template for defining settings for a particular application or module. This class typically contains fields for storing configuration information, such as API keys, database connection strings, and other important settings. The fields are defined using Python type annotations, and pydantic provides validation for these fields at runtime to ensure that only valid values are accepted.
'''

from pydantic import BaseSettings


# pydantic will automatically assume the below default values if corresponding environment variables are not found
class Settings(BaseSettings):
    # Environment variables
    env_name: str = "Local"
    base_url: str = "http://localhost:8000"
    db_url: str = "sqlite:///./shortener.db"
    
    # This class allows for the loading of environment variables from the .env file
    class Config:
        env_file = ".env"
    
# The decorator is responsible for caching data (Least Recently Used Strategy)
@lru_cache 
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.env_name}")
    return settings

