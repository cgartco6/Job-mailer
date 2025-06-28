import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class Config:
    # Email settings
    EMAIL_USER = os.getenv("EMAIL_USER", "your_email@gmail.com")
    EMAIL_PASS = os.getenv("EMAIL_PASS", "your_app_password")
    
    # File paths
    BASE_CV_PATH = os.getenv("BASE_CV_PATH", "base_cv.txt")
    BASE_COVER_LETTER = os.getenv("BASE_COVER_LETTER", "cover_letter.txt")
    
    # Job search settings
    TARGET_JOBS = os.getenv("TARGET_JOBS", "Python Developer,AI Engineer").split(',')
    LOCATION = os.getenv("LOCATION", "Remote")
    
    # Retry settings
    RESUME_RETRY_LIMIT = int(os.getenv("RESUME_RETRY_LIMIT", 3))
    EMAIL_RETRY_LIMIT = int(os.getenv("EMAIL_RETRY_LIMIT", 3))
    
    # Scraping settings
    SCRAPE_DELAY = float(os.getenv("SCRAPE_DELAY", 5.0))  # seconds between requests

config = Config()
