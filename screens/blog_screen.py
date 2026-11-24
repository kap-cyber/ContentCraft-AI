import streamlit as st

from generators.blog_generator import generate_blog, improve_blog
from ui.components import (
    empty_state,
    icon_svg,
    page_header,
    section_title,
    text_to_html,
)


def format_blog_preview(data):

    content = []

    # Title
    if data.get("title"):
        content.append(f"# {data['title']}")

    # Introduction
    if data.get("introduction"):
        content.append(data["introduction"])

    # Blog sections
    for section in data.get("sections", []):

        if section.get("heading"):
            content.append(f"## {section['heading']}")

        if section.get("content"):
            content.append(section["content"])

    # Conclusion
    if data.get("conclusion"):
        content.append("## Conclusion")
        content.append(data["conclusion"])

    # SEO Fields
    if data.get("seo_title"):
        content.append("### SEO Title")
        content.append(data["seo_title"])

    if data.get("meta_description"):
        content.append("### Meta Description")
        content.append(data["meta_description"])

    if data.get("keywords"):
        content.append("### SEO Keywords")
        content.append(", ".join(data["keywords"]))

    return "\n\n".join(content)


# ---------- Presentation helpers (UI only) ----------

def _format_article(data):
    """Article body as Markdown (same content as format_blog_preview, minus SEO)."""

    content = []

    if data.get("title"):
        content.append(f"# {data['title']}")

    if data.get("introduction"):
        content.append(data["introduction"])

    for section in data.get("sections", []) or []:

        if not isinstance(section, dict):
            continue

        if section.get("heading"):
            content.append(f"## {section['heading']}")

        if section.get("content"):
            content.append(section["content"])

    if data.get("conclusion"):
        content.append("## Conclusion")
        content.append(data["conclusion"])

    return "\n\n".join(content)


def _seo_html(data):

    rows = []

    if data.get("seo_title"):
        rows.append(
            '<div class="cc-seo-row"><div class="cc-seo-label">SEO Title</div>'
            f'<div class="cc-seo-value">{text_to_html(data["seo_title"])}</div></div>'
        )

    if data.get("meta_description"):
        rows.append(
            '<div class="cc-seo-row"><div class="cc-seo-label">Meta Description</div>'
            f'<div class="cc-seo-value">{text_to_html(data["meta_description"])}</div></div>'
        )

    keywords = [k for k in (data.get("keywords") or []) if k]

    if keywords:
        chips = "".join(f'<span class="cc-chip">{text_to_html(k)}</span>' for k in keywords)
        rows.append(
            '<div class="cc-seo-row"><div class="cc-seo-label">SEO Keywords</div>'
            f'<div class="cc-chip-row">{chips}</div></div>'
        )

    if not rows:
        return ""

    return (
        f'<div class="cc-seo"><div class="cc-seo-head">{icon_svg("spark", 14)} '
        f'SEO details</div>{"".join(rows)}</div>'
    )


def render_blog_preview(placeholder, data):
    """Render the (possibly partial) blog into a st.empty placeholder."""

    with placeholder.container():

        article = _format_article(data)

        if article:
            st.markdown(article)

        seo = _seo_html(data)

        if seo:
            st.html(seo)


def _word_count(data):
    return len(_format_article(data).replace("#", " ").split())


def clear_instruction():
    st.session_state.improvement_instruction = ""


def render_blog_screen():
    if "generated_blog" not in st.session_state:
        st.session_state.generated_blog = None

    if "improvement_instruction" not in st.session_state:
        st.session_state.improvement_instruction = ""

    # Clear instruction before widget is created
    if st.session_state.get("clear_instruction_flag", False):
        st.session_state.improvement_instruction = ""
        st.session_state.clear_instruction_flag = False

    page_header(
        "Blog Generator",
        "Create detailed, structured, SEO-friendly blog articles — then refine them with AI.",
        icon="blog",
        eyebrow="Generator",
    )

    st.write("")

    input_col, output_col = st.columns([5, 7], gap="large")

    # ---------- Inputs ----------
    with input_col:

        with st.container(border=True, key="card_blog_inputs"):

            section_title("Blog details", "Tell the AI what to write about.")

            # User inputs
            topic = st.text_input(
                "Blog Topic",
                placeholder="e.g., How AI is transforming healthcare",
            )

            audience = st.selectbox(
                "Target Audience",
                [
                    "Beginners",
                    "Students",
                    "Professionals",
                    "Developers",
                    "General Audience",
                ],
            )

            col_tone, col_style = st.columns(2)

            with col_tone:
                tone = st.selectbox(
                    "Tone",
                    [
                        "Professional",
                        "Friendly",
                        "Casual",
                        "Formal",
                        "Persuasive",
                    ],
                )

            with col_style:
                style = st.selectbox(
                    "Writing Style",
                    [
                        "Informative",
                        "Educational",
                        "Storytelling",
                        "Technical",
                        "Conversational",
                    ],
                )

            word_count = st.slider(
                "Target Word Count",
                min_value=300,
                max_value=1000,
                value=500,
                step=100,
                help="Approximate length of the article body.",
            )

            language = st.selectbox(
                "Language",
                ["English", "Hindi", "Hinglish"],
            )

            generate_clicked = st.button(
                "Generate Blog",
                type="primary",
                icon=":material/auto_awesome:",
                width="stretch",
            )

            input_feedback = st.container()

    # ---------- Output ----------
    with output_col:

        status_slot = st.empty()

        with st.container(border=True, key="card_blog_output"):
            blog_placeholder = st.empty()

        meta_slot = st.empty()

        improve_area = st.container()

    streamed = False

    # Generate Blog
    if generate_clicked:

        if not topic.strip():
            input_feedback.warning(
                "Please enter a blog topic.", icon=":material/warning:"
            )

        else:

            with status_slot.container():

                with st.spinner("Generating your blog..."):

                    final_blog = {}

                    for chunk in generate_blog(
                        topic=topic,
                        audience=audience,
                        tone=tone,
                        style=style,
                        word_count=word_count,
                        language=language,
                    ):

                        # Accumulate streamed chunks
                        final_blog.update(chunk)

                        render_blog_preview(blog_placeholder, final_blog)

            st.session_state.generated_blog = final_blog
            streamed = True

    if not streamed:

        if st.session_state.generated_blog:
            render_blog_preview(blog_placeholder, st.session_state.generated_blog)

        else:
            empty_state(
                blog_placeholder,
                "Your article will appear here",
                "Fill in the blog details and click Generate Blog. "
                "The article streams in live as it's written.",
                icon="doc",
            )

    # Improvement Section
    if st.session_state.generated_blog:

        with improve_area:

            with st.container(border=True, key="card_blog_improve"):

                section_title(
                    "✨ Improve Your Blog",
                    "Describe the changes and the AI will rewrite the article above.",
                )

                st.text_area(
                    "What would you like to improve?",
                    placeholder=(
                        "Make the introduction more engaging, "
                        "add practical examples, or simplify the language..."
                    ),
                    key="improvement_instruction",
                )

                col1, col2 = st.columns([3, 2])

                with col1:

                    improve_button = st.button(
                        "Improve Blog",
                        key="improve_button",
                        type="primary",
                        icon=":material/auto_fix_high:",
                        width="stretch",
                    )

                with col2:

                    st.button(
                        "Clear",
                        key="clear_button",
                        on_click=clear_instruction,
                        icon=":material/backspace:",
                        width="stretch",
                    )

                improve_feedback = st.container()

        if improve_button:

            improvement_instruction = (
                st.session_state.improvement_instruction
            )

            if not improvement_instruction.strip():

                improve_feedback.warning(
                    "Please describe what you want to improve.",
                    icon=":material/warning:",
                )

            else:
                improve_placeholder = blog_placeholder
                improve_blog_data = {}
                with improve_feedback:
                    with st.spinner("Improving your blog..."):

                        for chunk in improve_blog(
                            blog=st.session_state.generated_blog,
                            improvement_instruction=improvement_instruction,
                            word_count=word_count
                        ):

                            improve_blog_data.update(chunk)

                            render_blog_preview(improve_placeholder, improve_blog_data)
                        st.session_state.generated_blog = improve_blog_data

                st.toast("Blog improved", icon=":material/check_circle:")

    # Article meta + download (rendered last so it reflects the latest version)
    if st.session_state.generated_blog:

        with meta_slot.container():

            meta_col, download_col = st.columns(
                [3, 2], vertical_alignment="center"
            )

            with meta_col:
                st.caption(
                    f":material/description: ~{_word_count(st.session_state.generated_blog)} words"
                )

            with download_col:
                st.download_button(
                    "Download Markdown",
                    data=format_blog_preview(st.session_state.generated_blog),
                    file_name="contentcraft-blog.md",
                    mime="text/markdown",
                    icon=":material/download:",
                    on_click="ignore",
                    width="stretch",
                    key="download_blog",
                )
