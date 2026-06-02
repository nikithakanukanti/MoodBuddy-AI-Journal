# MoodBuddy-AI-Journal
A cute, friendly local AI journal and mood companion built with Streamlit and Ollama.

# 🧸 MoodBuddy: Your Local AI Journal Companion

MoodBuddy is a wholesome, private digital diary that reads your daily thoughts, analyzes your emotional vibe, and responds with a validating, supportive message. 

Because it runs entirely on your local machine using an open-source Large Language Model (LLM), your personal journal entries are 100% private and never sent over the internet.

## ✨ Features
- **Cute Dashboard:** Built with a simple, modern Streamlit UI.
- **Privacy First:** Powered completely offline via Ollama.
- **Memory Lane:** Automatically saves your daily logs and lets you review past days via dropdown cards.

## 🛠️ Tech Stack
- **Language:** Python
- **Interface:** Streamlit
- **AI Core:** Ollama (`qwen2:1.5b`)

## 🚀 How to Run It Locally

1. **Install Python Packages:**
   ```bash
   pip install streamlit openai
2. **Start your AI Brain:**
Make sure Ollama is running in the background and pull the model:
   ```bash
   ollama run qwen2:1.5b
3. **Launch MoodBuddy**:
Navigate to your folder and run:
   ```bash
   python -m streamlit run app.py
