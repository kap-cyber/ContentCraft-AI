import streamlit as st

from generators.email_generator import generate_email
from ui.components import empty_state, page_header, section_title, text_to_html


# ---------- Presentation helpers (UI only) ----------

def _email_preview_html(data, recipient):

    subject = data.get("subject", "")
    email_body = data.get("email_body", "")
    closing = data.get("closing", "")

    to_value = text_to_html(recipient) if recipient else '<span style="color:#94A3B8">Recipient</span>'

    closing_html = (
        f'<div class="cc-mail-closing">{text_to_html(closing)}</div>' if closing else ""
    )

    return (
        '<div class="cc-mail">'
        '<div class="cc-mail-bar"><span class="cc-mail-dot"></span>'
        '<span class="cc-mail-dot"></span><span class="cc-mail-dot"></span>'
        '<span style="margin-left:6px">New message</span></div>'
        f'<div class="cc-mail-row"><span class="cc-mail-key">To</span>'
        f'<span class="cc-mail-val">{to_value}</span></div>'
        f'<div class="cc-mail-row"><span class="cc-mail-key">Subject</span>'
        f'<span class="cc-mail-val cc-mail-subject">{text_to_html(subject)}</span></div>'
        f'<div class="cc-mail-body">{text_to_html(email_body)}{closing_html}</div>'
        "</div>"
    )


def _full_email_text(data):

    subject = data.get("subject", "")
    pieces = [
        f"Subject: {subject}" if subject else "",
        data.get("email_body", ""),
        data.get("closing", ""),
    ]

    return "\n\n".join(p for p in pieces if p)


def render_email_screen():

    if "generated_email" not in st.session_state:
        st.session_state.generated_email = None

    page_header(
        "Email Generator",
        "Generate professional emails tailored to your purpose, "
        "recipient, and communication style.",
        icon="email",
        eyebrow="Generator",
    )

    st.write("")

    input_col, output_col = st.columns([5, 7], gap="large")

    # ---------- Inputs ----------
    with input_col:

        with st.container(border=True, key="card_email_inputs"):

            section_title("Email details", "Describe who you're writing to and why.")

            email_type = st.selectbox(
                "Email Type",
                [
                    "Professional Email",
                    "Job Application",
                    "Follow-up Email",
                    "Cold Outreach",
                    "Business Email",
                    "Thank You Email",
                    "Apology Email",
                    "Meeting Request",
                    "Other"
                ]
            )

            col_recipient, col_tone = st.columns(2)

            with col_recipient:
                recipient = st.text_input(
                    "Recipient",
                    placeholder="e.g., Hiring Manager, Client, HR"
                )

            with col_tone:
                tone = st.selectbox(
                    "Tone",
                    [
                        "Professional",
                        "Formal",
                        "Friendly",
                        "Casual",
                        "Persuasive",
                        "Polite",
                        "Confident"
                    ]
                )

            topic = st.text_input(
                "Subject / Topic",
                placeholder="e.g., Application for AI Engineer position"
            )

            key_details = st.text_area(
                "Key Details",
                placeholder="Enter the important information that should be included in the email..."
            )

            additional_instructions = st.text_area(
                "Additional Instructions (Optional)",
                placeholder="e.g., Keep it concise, mention my projects, avoid overly formal language..."
            )

            generate_button = st.button(
                "Generate Email",
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
            input_feedback.warning("Please enter the email topic.", icon=":material/warning:")

        elif not key_details.strip():
            input_feedback.warning("Please enter the key details.", icon=":material/warning:")

        else:

            generated_data = {}

            with status_slot.container():

                with st.spinner("Generating your email..."):

                    for chunk in generate_email(
                        email_type=email_type,
                        recipient=recipient,
                        topic=topic,
                        key_details=key_details,
                        tone=tone,
                        additional_instructions=additional_instructions
                    ):

                        generated_data.update(chunk)

                        output_placeholder.html(
                            _email_preview_html(generated_data, recipient)
                        )

            st.session_state.generated_email = generated_data
            st.session_state.email_preview_recipient = recipient

            st.rerun()

    if st.session_state.generated_email:

        email_data = st.session_state.generated_email

        preview_recipient = st.session_state.get("email_preview_recipient", recipient)

        with output_placeholder.container(border=True, key="card_email_output"):

            section_title("Generated Email", "Review the draft, then copy it or edit individual parts.")

            preview_tab, edit_tab = st.tabs(
                [":material/visibility: Preview", ":material/edit_note: Edit"]
            )

            with preview_tab:

                st.html(_email_preview_html(email_data, preview_recipient))

                st.caption("Full email — use the copy icon to copy it.")
                st.code(_full_email_text(email_data), language=None, wrap_lines=True)

            with edit_tab:

                st.text_area(
                    "Subject",
                    value=email_data.get("subject", ""),
                    height=70
                )

                st.text_area(
                    "Email Body",
                    value=email_data.get("email_body", ""),
                    height=300
                )

                st.text_area(
                    "Closing",
                    value=email_data.get("closing", ""),
                    height=100
                )

    else:

        with output_placeholder.container():
            empty_state(
                st,
                "Your email will appear here",
                "Pick an email type, add the topic and key details, "
                "then click Generate Email.",
                icon="email",
            )
