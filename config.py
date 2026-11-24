import os
from dotenv import load_dotenv

load_dotenv()

# API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# Model configuration
MODEL_NAME = "openai/gpt-oss-20b"
TEMPERATURE = 0

# Validate configuration
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Please check your .env file.")