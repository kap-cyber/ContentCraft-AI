import streamlit as st

from generators.social_media_generator import generate_social_media_post
from ui.components import empty_state, page_header, section_title, text_to_html


# ---------- Presentation helpers (UI only) ----------

def _post_preview_html(data, platform):

    hook = data.get("hook", "")
    content = data.get("content", "")
    call_to_action = data.get("call_to_action", "")
    hashtags = [h for h in (data.get("hashtags") or []) if h]

    parts = [
        '<div class="cc-post">',
        '<div class="cc-post-head">',
        '<div class="cc-avatar">CC</div>',
        '<div><div class="cc-post-name">Your Brand</div>'
        '<div class="cc-post-meta">Draft preview</div></div>',
        f'<span class="cc-platform">{text_to_html(platform)}</span>',
        "</div>",
    ]

    if hook:
        parts.append('<div class="cc-post-section-label">Hook</div>')
        parts.append(f'<div class="cc-post-hook">{text_to_html(hook)}</div>')

    if content:
        parts.append('<div class="cc-post-section-label">Main Content</div>')
        parts.append(f'<div class="cc-post-body">{text_to_html(content)}</div>')

    if call_to_action:
        parts.append('<div class="cc-post-section-label">Call to Action</div>')
        parts.append(f'<div class="cc-post-cta">{text_to_html(call_to_action)}</div>')

    if hashtags:
        parts.append('<div class="cc-post-section-label">Hashtags</div>')
        parts.append(
            f'<div class="cc-post-tags">{text_to_html(" ".join(hashtags))}</div>'
        )

    parts.append("</div>")

    return "".join(parts)


def _full_post_text(data):

    pieces = [
        data.get("hook", ""),
        data.get("content", ""),
        data.get("call_to_action", ""),
        " ".join(data.get("hashtags", []) or []),
    ]

    return "\n\n".join(p for p in pieces if p)


def render_social_media_screen():

    page_header(
        "Social Media Generator",
        "Generate engaging social media content tailored to your platform and audience.",
        icon="social",
        eyebrow="Generator",
    )

    st.write("")

    if "generated_social_media" not in st.session_state:
        st.session_state.generated_social_media = None

    input_col, output_col = st.columns([5, 7], gap="large")

    # ---------- Inputs ----------
    with input_col:

        with st.container(border=True, key="card_social_inputs"):

            section_title("Post details", "Choose a platform and describe your post.")

            platform = st.selectbox(
                "Platform",
                ["Instagram", "LinkedIn", "X (Twitter)", "Facebook"]
            )

            topic = st.text_input(
                "Topic",
                placeholder="e.g., Artificial Intelligence"
            )

            audience = st.text_input(
                "Target Audience",
                placeholder="e.g., Students, developers, entrepreneurs"
            )

            col_type, col_tone = st.columns(2)

            with col_type:
                content_type = st.selectbox(
                    "Content Type",
                    [
                        "Educational",
                        "Promotional",
                        "Inspirational",
                        "Entertaining",
                        "Informative",
                        "Personal Branding"
                    ]
                )

            with col_tone:
                tone = st.selectbox(
                    "Tone",
                    [
                        "Professional",
                        "Casual",
                        "Friendly",
                        "Engaging",
                        "Persuasive",
                        "Humorous"
                    ]
                )

            additional_instructions = st.text_area(
                "Additional Instructions (Optional)",
                placeholder="e.g., Keep it under 150 words, add emojis, mention our product launch..."
            )

            generate_button = st.button(
                "Generate Post",
                type="primary",
                icon=":material/auto_awesome:",
                width="stretch",
            )

            input_feedback = st.container()

    # ---------- Output ----------
    with output_col:

        status_slot = st.empty()

        output_placeholder = st.empty()

    if generate_button:

        if not topic.strip():
            input_feedback.warning("Please enter a topic.", icon=":material/warning:")

        elif not audience.strip():
            input_feedback.warning(
                "Please enter your target audience.", icon=":material/warning:"
            )

        else:

            generated_data = {}

            with status_slot.container():

                with st.spinner("Generating your social media post..."):

                    for chunk in generate_social_media_post(
                        platform=platform,
                        topic=topic,
                        audience=audience,
                        content_type=content_type,
                        tone=tone,
                        additional_instructions=additional_instructions
                    ):

                        generated_data.update(chunk)

                        output_placeholder.html(
                            _post_preview_html(generated_data, platform)
                        )

            # Save generated output
            st.session_state.generated_social_media = generated_data
            st.session_state.social_preview_platform = platform

            st.rerun()

    if st.session_state.generated_social_media:

        generated_data = st.session_state.generated_social_media

        preview_platform = st.session_state.get("social_preview_platform", platform)

        with output_placeholder.container(border=True, key="card_social_output"):

            section_title("Generated Social Media Post", "Preview your post, then copy or edit individual sections.")

            preview_tab, sections_tab = st.tabs(
                [":material/visibility: Preview", ":material/edit_note: Sections"]
            )

            with preview_tab:

                st.html(_post_preview_html(generated_data, preview_platform))

                st.caption("Full post — use the copy icon to copy it.")
                st.code(_full_post_text(generated_data), language=None, wrap_lines=True)

            with sections_tab:

                # Hook
                st.text_area(
                    "Hook",
                    value=generated_data.get("hook", ""),
                    height=100
                )

                # Main Content
                st.text_area(
                    "Content",
                    value=generated_data.get("content", ""),
                    height=250
                )

                # Call To Action
                st.text_area(
                    "Call to Action",
                    value=generated_data.get("call_to_action", ""),
                    height=100
                )

                # Hashtags
                hashtags = generated_data.get("hashtags", [])

                st.text_area(
                    "Hashtags",
                    value=" ".join(hashtags),
                    height=100
                )

    else:

        with output_placeholder.container():
            empty_state(
                st,
                "Your post will appear here",
                "Choose a platform, describe your topic and audience, "
                "then click Generate Post.",
                icon="social",
            )
