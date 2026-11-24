from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from model import llm
from schemas.content_schemas import EmailOutput

parser = JsonOutputParser(pydantic_object=EmailOutput)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert professional email writer.

        Your task is to write clear, effective, and well-structured
        emails based on the user's requirements.

        Follow these guidelines:

        - Write an appropriate subject line.
        - Match the requested email type.
        - Adapt the language to the recipient.
        - Follow the requested tone.
        - Include all important details provided by the user.
        - Keep the email clear and well-organized.
        - Avoid unnecessary words and repetition.
        - Include an appropriate greeting in the email body.
        - Generate a suitable closing and sign-off.
        - Do not invent information that the user hasn't provided.
        - Follow the required output format.

        {format_instructions}
        """
    ),
    (
        "human",
        """
        Email Type: {email_type}

        Recipient: {recipient}

        Topic: {topic}

        Key Details: {key_details}

        Tone: {tone}

        Additional Instructions: {additional_instructions}
        """
    )
])

prompt = prompt.partial(
    format_instructions=parser.get_format_instructions()
)

email_chain = prompt | llm | parser

def generate_email(
    email_type,
    recipient,
    topic,
    key_details,
    tone,
    additional_instructions=""
):

    inputs = {
        "email_type": email_type,
        "recipient": recipient,
        "topic": topic,
        "key_details": key_details,
        "tone": tone,
        "additional_instructions": additional_instructions
    }

    for chunk in email_chain.stream(inputs):
        yield chunk