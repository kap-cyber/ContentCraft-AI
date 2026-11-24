from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from config import (
    GROQ_API_KEY,
    GOOGLE_API_KEY,
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
# llm =ChatOllama(model=MODEL_NAME,think=False)
# llm = ChatGoogleGenerativeAI(
#     model=MODEL_NAME,
#     google_api_key=GOOGLE_API_KEY,
#     temperature=TEMPERATURE,
#     max_tokens=MAX_TOKENS,
#     max_retries=2,
# )

# response = llm.invoke("Explain ai")
# print(response.content)