import streamlit as st

from ui.components import icon_svg


FEATURES = [
    {
        "key": "blog",
        "icon": "blog",
        "title": "Blog Generator",
        "description": (
            "Create detailed, structured, SEO-friendly blog articles "
            "and improve existing content."
        ),
        "cta": "Start writing",
    },
    {
        "key": "social",
        "icon": "social",
        "title": "Social Media Generator",
        "description": (
            "Create engaging, platform-optimized social media content "
            "for different audiences."
        ),
        "cta": "Create a post",
    },
    {
        "key": "email",
        "icon": "email",
        "title": "Email Generator",
        "description": (
            "Generate professional emails for job applications, business "
            "communication, follow-ups, and more."
        ),
        "cta": "Write an email",
    },
]


def render_home_screen(blog_page, social_page, email_page):

    pages = {"blog": blog_page, "social": social_page, "email": email_page}

    st.html(
        f"""
        <div class="cc-hero">
          <span class="cc-pill">{icon_svg("spark", 14)} AI-powered content studio</span>
          <h1>Create content with <span>AI.</span></h1>
          <p>Generate blogs, social media posts, and professional emails
          in seconds using AI.</p>
        </div>
        """
    )

    st.write("")

    columns = st.columns(3, gap="medium")

    for column, feature in zip(columns, FEATURES):

        with column:

            with st.container(border=True, key=f"card_feature_{feature['key']}"):

                st.html(
                    f"""
                    <div class="cc-feature-icon">{icon_svg(feature["icon"], 22)}</div>
                    <div class="cc-feature-title">{feature["title"]}</div>
                    <div class="cc-feature-desc">{feature["description"]}</div>
                    """
                )

                if st.button(
                    feature["cta"],
                    key=f"open_{feature['key']}",
                    icon=":material/arrow_forward:",
                    icon_position="right",
                    width="stretch",
                ):
                    st.switch_page(pages[feature["key"]])

    st.write("")

    with st.container(border=True, key="card_how_it_works"):

        st.html(
            """
            <div class="cc-section-title" style="margin-bottom:1rem">How it works</div>
            <div class="cc-steps">
              <div class="cc-step">
                <div class="cc-step-num">1</div>
                <div>
                  <div class="cc-step-title">Pick a generator</div>
                  <div class="cc-step-text">Blog, social media or email — choose what you need to write.</div>
                </div>
              </div>
              <div class="cc-step">
                <div class="cc-step-num">2</div>
                <div>
                  <div class="cc-step-title">Describe your content</div>
                  <div class="cc-step-text">Set the topic, audience, tone and any extra details.</div>
                </div>
              </div>
              <div class="cc-step">
                <div class="cc-step-num">3</div>
                <div>
                  <div class="cc-step-title">Generate &amp; refine</div>
                  <div class="cc-step-text">Watch it stream in live, then refine, copy or download.</div>
                </div>
              </div>
            </div>
            """
        )
