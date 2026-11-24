# ✨ ContentCraft AI

**Create smarter. Write faster.**

ContentCraft AI is an AI-powered content creation platform that helps users generate high-quality blog articles, social media posts, and professional emails using Large Language Models (LLMs).

Built with Python, Streamlit, and LangChain, the application provides an interactive interface for generating, streaming, and improving AI-generated content.

---

## 🚀 Features

### 📝 Blog Generator
- Generate structured blog articles based on topics and target audiences.
- Customize tone, writing style, language, and word count.
- Stream AI-generated content in real time.
- Generate SEO titles, meta descriptions, and keywords.
- Improve existing blogs using custom instructions.

### 📱 Social Media Post Generator
- Generate platform-specific social media content.
- Customize platform, audience, tone, and content type.
- Generate engaging hooks, post content, calls to action, and hashtags.
- Support custom instructions.

### ✉️ Email Generator
- Generate professional emails for different scenarios.
- Support job applications, follow-ups, business communication, and more.
- Customize recipient, topic, key details, tone, and instructions.
- Generate structured email content with subject, body, and closing.

### 🎨 User Interface
- Modern SaaS-style interface.
- Interactive dashboard.
- Light and Dark mode.
- Responsive layout.
- Dedicated interfaces for each content generator.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – Interactive web application
- **LangChain** – LLM orchestration and prompt management
- **Groq API** – Large Language Model inference
- **Pydantic** – Structured output validation
- **JSON Output Parsing** – Structured AI-generated content

---

## 🏗️ Project Structure

```text
ContentCraft-AI/
│
├── generators/
│   ├── blog_generator.py
│   ├── social_media_generator.py
│   └── email_generator.py
│
├── schemas/
│   └── content_schemas.py
│
├── screens/
│   ├── home_screen.py
│   ├── blog_screen.py
│   ├── social_media_screen.py
│   └── email_screen.py
│
├── ui/
│   ├── components.py
│   └── styles.css
│
├── app.py
├── config.py
├── model.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ContentCraft-AI.git
```

### 2. Navigate to the Project Directory

```bash
cd ContentCraft-AI
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Replace `your_groq_api_key` with your actual Groq API key.

### 7. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key used to access the Groq LLM service |

**Never commit your `.env` file or API keys to GitHub.**

---

## 🧠 How It Works

ContentCraft AI uses LangChain to manage the LLM interaction pipeline.

The general workflow:

1. User provides content requirements through the UI.
2. Input data is passed to the appropriate generator.
3. LangChain prompt templates construct the model prompt.
4. The LLM generates the requested content.
5. Output parsers structure the generated response.
6. Generated content is streamed to the UI.
7. Users can review and customize the generated content.

---

## 📌 Future Improvements

- Content history and saved drafts.
- Download generated content in multiple formats.
- Additional social media platforms.
- More advanced content customization.
- Improved content generation workflows.
- User authentication and personalized workspaces.

---

## 👨‍💻 Author

**Kapil Panchal**

Full-Stack Developer | AI Engineer

---

