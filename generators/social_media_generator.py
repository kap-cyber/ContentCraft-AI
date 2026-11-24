from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from model import llm
from schemas.content_schemas import SocialMediaOutput

parser = JsonOutputParser(pydantic_object=SocialMediaOutput)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert social media content creator.

        Your task is to generate engaging social media posts
        tailored to the selected platform and target audience.

        Follow these guidelines:

        - Write an attention-grabbing hook.
        - Create engaging and valuable content.
        - Adapt the writing style to the selected platform.
        - Match the requested tone.
        - Keep the content appropriate for the selected content type.
        - Generate a relevant call to action.
        - Generate relevant hashtags.
        - Avoid unnecessary hashtags.
        - Do not include explanations outside the requested output.
        - Follow the required output format.

        {format_instructions}
        """
    ),
    (
        "human",
        """
        Platform: {platform}

        Topic: {topic}

        Target Audience: {audience}

        Content Type: {content_type}

        Tone: {tone}

        Additional Instructions: {additional_instructions}
        """
    )
])
prompt = prompt.partial(
    format_instructions=parser.get_format_instructions()
)
social_media_chain = prompt | llm | parser

def generate_social_media_post(
    platform,
    topic,
    audience,
    content_type,
    tone,
    additional_instructions=""
):

    inputs = {
        "platform": platform,
        "topic": topic,
        "audience": audience,
        "content_type": content_type,
        "tone": tone,
        "additional_instructions": additional_instructions
    }

    for chunk in social_media_chain.stream(inputs):
        yield chunk