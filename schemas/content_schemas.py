from pydantic import BaseModel, Field


class BlogSection(BaseModel):
    heading: str = Field(description="Heading of the blog section")
    content: str = Field(description="Content of the blog section")


class BlogOutput(BaseModel):
    title: str = Field(description="Title of the blog")
    introduction: str = Field(description="Introduction of the blog")
    sections: list[BlogSection] = Field(
        description="Main sections of the blog"
    )
    conclusion: str = Field(description="Conclusion of the blog")

    seo_title: str = Field(
        description="SEO optimized title for search engines"
    )

    meta_description: str = Field(
        description="SEO meta description summarizing the blog"
    )

    keywords: list[str] = Field(
        description="Relevant SEO keywords for the blog"
    )

class SocialMediaOutput(BaseModel):

    hook: str = Field(
        description="Attention-grabbing opening line for the social media post"
    )

    content: str = Field(
        description="Main body of the social media post"
    )

    call_to_action: str = Field(
        description="Call to action encouraging the audience to engage or take action"
    )

    hashtags: list[str] = Field(
        description="Relevant hashtags for the social media post"
    )

class EmailOutput(BaseModel):

    subject: str = Field(
        description="Subject line of the generated email"
    )

    email_body: str = Field(
        description="Main body of the email including greeting and message"
    )

    closing: str = Field(
        description="Professional closing statement and sign-off"
    )