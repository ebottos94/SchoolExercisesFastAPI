from pydantic import BaseSettings


class Settings(BaseSettings):
    server_port: int = 8000
    path_db: str = "sqlite:///./app.db"
    max_num_class: int = 5



settings = Settings()