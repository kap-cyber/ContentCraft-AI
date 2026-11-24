from langchain_core.prompts import ChatPromptTemplate
import json
from model import llm
from schemas.content_schemas import BlogOutput
from langchain_core.output_parsers import JsonOutputParser

def calculate_max_tokens(word_count: int) -> int:
    estimated_tokens = int(word_count * 3)

    # Extra tokens for JSON structure and SEO fields
    buffer_tokens = 300

    return estimated_tokens + buffer_tokens

parser = JsonOutputParser(pydantic_object=BlogOutput)
blog_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a professional blog content writer and SEO specialist.

Generate informative, engaging, and well-structured blog posts.

Ensure the blog contains:
1. An engaging title
2. Introduction
3. Multiple main sections with headings
4. Conclusion
5. SEO title
6. Meta description
7. Relevant SEO keywords

WORD COUNT REQUIREMENTS:

- Target approximately {word_count} words for the blog content only.
- Do not include the title, SEO title, meta description, or keywords
  when calculating the target word count.
- Aim to stay within approximately 10% of the requested word count.
- Distribute the content appropriately across the introduction,
  main sections, and conclusion.
- Introduction: approximately 10% of the target word count.
- Main sections: approximately 75-80%.
- Conclusion: approximately 10-15%.
- These percentages are guidelines, not rigid limits.
- Generate 4-6 main sections, depending on the topic.
- Each section must have a descriptive heading and detailed content.
- Avoid repeating information across sections.
- Do not make sections excessively short.
- Do not stop after generating the introduction.
- Complete every required field in the output schema.

SEO requirements:
- SEO title should be concise and search-friendly.
- Meta description should summarize the blog and encourage clicks.
- Keywords should be relevant to the topic.
- Avoid keyword stuffing.

Ensure the output is complete, informative, and consistent with all
user requirements.

{format_instructions}
""",
        ),
        (
            "human",
            """
Write a blog post with the following requirements:

Topic: {topic}
Target Audience: {audience}
Tone: {tone}
Writing Style: {style}
Word Count: {word_count}
Language: {language}
""",
        ),
    ]
).partial(format_instructions=parser.get_format_instructions())


# structured_llm = llm.with_structured_output(BlogOutput)
# blog_chain = blog_prompt | llm | parser

def generate_blog(
    topic: str,
    audience: str,
    tone: str,
    style: str,
    word_count: int,
    language: str,
):

    inputs = {
        "topic": topic,
        "audience": audience,
        "tone": tone,
        "style": style,
        "word_count": word_count,
        "language": language,
    }
    max_tokens = calculate_max_tokens(word_count)
    dynamic_llm = llm.bind(max_tokens=max_tokens)
    dynamic_blog_chain = blog_prompt | dynamic_llm | parser

    for chunk in dynamic_blog_chain.stream(inputs):
        yield chunk

import json

def improve_blog(
    blog: dict,
    improvement_instruction: str,
    word_count: int,
):
    improvement_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are an expert blog editor and content transformation specialist.

Your primary responsibility is to follow the user's improvement
instructions exactly.

IMPORTANT PRIORITY RULES:

1. The user's improvement instructions are your highest priority.
2. Make meaningful and noticeable changes when requested.
3. Do not simply rephrase existing content.
4. If the user requests adding new information, examples, steps,
   explanations, or sections, actually add them.
5. If the user requests removing content, remove it completely.
6. If the user requests replacing a section, completely replace
   that section with the requested content.
7. If the user requests restructuring, restructure the blog.
8. Preserve content only when the user has not requested changes
   to that content.
9. Do not ignore, weaken, or partially implement instructions.
10. Carefully verify that the final blog satisfies every part
    of the user's instruction before producing the output.

BLOG REQUIREMENTS:

- Preserve the original topic unless instructed otherwise.
- Maintain the target audience and language unless instructed otherwise.
- Maintain approximately the target word count.
- Preserve all required fields in the output schema.
- Return the COMPLETE improved blog.
- Never return only the modified sections.
- Avoid unnecessary repetition.
- Make the improvements genuinely useful and substantial.

USER INSTRUCTION:

The instruction below must be followed exactly:

{improvement_instruction}

Original Blog:

{blog}

Target Word Count: {word_count}

Return the complete improved blog in the required JSON format.

{format_instructions}
""",
            ),
        ]
    ).partial(
        format_instructions=parser.get_format_instructions()
    )

    max_tokens = calculate_max_tokens(word_count)

    dynamic_llm = llm.bind(max_tokens=max_tokens)

    improvement_chain = improvement_prompt | dynamic_llm | parser

    inputs = {
        "blog": json.dumps(blog, ensure_ascii=False, indent=2),
        "improvement_instruction": improvement_instruction,
        "word_count": word_count,
    }

    for chunk in improvement_chain.stream(inputs):
        yield chunk

