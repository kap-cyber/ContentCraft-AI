import streamlit as st

from screens.blog_screen import render_blog_screen
from screens.social_media_screen import render_social_media_screen
from screens.email_screen import render_email_screen
from screens.home_screen import render_home_screen
from ui.components import (
    APP_NAME,
    init_theme,
    load_css,
    sidebar_brand,
    sidebar_label,
    theme_toggle,
)


st.set_page_config(
    page_title=APP_NAME,
    page_icon=":material/auto_awesome:",
    layout="wide",
    initial_sidebar_state="auto",
)

load_css(init_theme())

# Pages
blog_page = st.Page(
    render_blog_screen,
    title="Blog Generator",
    icon=":material/article:",
    url_path="blog",
)

social_page = st.Page(
    render_social_media_screen,
    title="Social Media Generator",
    icon=":material/forum:",
    url_path="social-media",
)

email_page = st.Page(
    render_email_screen,
    title="Email Generator",
    icon=":material/mail:",
    url_path="email",
)


def render_dashboard():
    render_home_screen(blog_page, social_page, email_page)


home_page = st.Page(
    render_dashboard,
    title="Dashboard",
    icon=":material/space_dashboard:",
    default=True,
)

current_page = st.navigation(
    [home_page, blog_page, social_page, email_page],
    position="hidden",
)

# Sidebar
with st.sidebar:
    sidebar_brand()

    sidebar_label("Workspace")
    st.page_link(home_page, width="stretch")

    sidebar_label("Generators")
    st.page_link(blog_page, width="stretch")
    st.page_link(social_page, width="stretch")
    st.page_link(email_page, width="stretch")

    st.divider()

    theme_toggle()

    with st.expander("About", icon=":material/info:"):
        st.html(
            f"""
            <div class="cc-about">
              <b>{APP_NAME}</b> is an AI content studio for writing blogs,
              social media posts and professional emails, with live
              streaming output and one-click blog refinement.
              <div class="cc-chip-row">
                <span class="cc-chip">Streamlit</span>
                <span class="cc-chip">LangChain</span>
                <span class="cc-chip">Groq</span>
                <span class="cc-chip">Pydantic</span>
              </div>
            </div>
            """
        )

current_page.run()
