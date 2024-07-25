import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuration class for the application.
    
    Attributes:
        TOGETHER_API_KEY (str): The API key for the Together service.
        UPLOAD_FOLDER (str): The folder where uploaded files will be stored.
        MAX_UPLOAD_SIZE (int): The maximum allowed size for uploaded files in bytes.
        ALLOWED_EXTENSIONS (set): The set of allowed file extensions.
        RATE_LIMIT (str): The rate limit for API requests.
    """
    TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
    UPLOAD_FOLDER = "uploads"
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {'pdf'}
    RATE_LIMIT = "5/minute"