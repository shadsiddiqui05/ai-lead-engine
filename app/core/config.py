from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SimplifIQ Lead Engine"
    GEMINI_API_KEY: str
    TAVILY_API_KEY: str
    RESEND_API_KEY: str
    GOOGLE_SERVICE_ACCOUNT_FILE: str
    GOOGLE_SHEET_ID: str = "your_google_sheet_id_here"
    GOOGLE_DRIVE_FOLDER_ID: str = "your_google_drive_folder_id_here"
    
    class Config:
        env_file = ".env"

settings = Settings()