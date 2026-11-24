from langchain_groq import ChatGroq
from config import (
    GROQ_API_KEY,
    MODEL_NAME,
    TEMPERATURE,
)

llm = ChatGroq(
    model=MODEL_NAME,
    api_key=GROQ_API_KEY,
    temperature=TEMPERATURE,
    max_retries=2,
    reasoning_format="hidden",
    reasoning_effort="low"
)