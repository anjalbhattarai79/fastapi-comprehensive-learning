from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    
    database_hostname: str 
    database_port: str 
    database_password: str        
    database_name: str 
    # database_url: str = "postgresql://postgres:admin@localhost/fastapi"
    
    secret_key: str 
    database_username: str 
    algorithm: str 
    access_token_expire_minutes: int 
    
    class Config:
        env_file = ".env" # This will tell pydantic to look for the .env file in the root directory of the project and load the environment variables from there.

settings = Settings()   