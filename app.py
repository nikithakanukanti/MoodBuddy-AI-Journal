import streamlit as st
from openai import OpenAI
import datetime
import os

# 1. Page Configuration
st.set_page_config(page_title="MoodBuddy", page_icon="🧸", layout="centered")

# 2. Connect to your free, local AI (Using the tiny model that worked for you!)
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL_NAME = "qwen2:1.5b" 

st.markdown(
    """
    <style>
    .stApp {
        background-color: #CDB4DB;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 3. App Title and Greeting
st.title("MoodBuddy🧸")
st.subheader("Your friendly AI Journal & Mood Companion")
st.write(f"Today is **{datetime.date.today().strftime('%A, %B %d')}** ✨")

st.divider()

# 4. Create two Tabs at the top of the webpage!
tab1, tab2 = st.tabs(["📝 New Entry", "📖 Past Memories"])

# --- TAB 1: WRITING A NEW DIARY ENTRY ---
with tab1:
    st.markdown("### 📝 How was your day?")
    journal_entry = st.text_area(
        "Pour your heart out here...", 
        placeholder="Type here about how your day went...",
        key="new_entry_box"
    )

    if st.button("✨ Analyze My Day ✨", type="primary"):
        if not journal_entry.strip():
            st.warning("Please write something first!")
        else:
            with st.spinner("🧸 MoodBuddy is reading carefully..."):
                prompt = f"""
                You are a wholesome, cute, and supportive AI journal assistant. 
                Read this journal entry: "{journal_entry}"
                
                Provide a reply in exactly this format:
                MOOD: (Choose ONE emoji that matches the vibe best, followed by a 1-word mood)
                REACTION: (Write a short, 2-sentence warm and encouraging reply)
                HIGHLIGHT: (Pick out the single best or most important moment)
                """
                
                try:
                    response = client.chat.completions.create(
                        model=MODEL_NAME, 
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7
                    )
                    ai_output = response.choices[0].message.content
                    
                    st.success("🧸 Analysis Complete!")
                    st.info(ai_output)
                    
                    # Save it with a special delimiter (###) so it's easy for Python to read back later
                    with open("my_diary_history.txt", "a", encoding="utf-8") as f:
                        f.write(f"###\nDATE: {datetime.date.today().strftime('%Y-%m-%d')}\nUSER: {journal_entry}\nAI: {ai_output}\n")
                    
                    st.caption("💾 Saved safely to your local history!")

                except Exception as e:
                    st.error(f"Make sure Ollama is open! Error: {e}")

# --- TAB 2: VIEWING PAST ENTRIES ---
with tab2:
    st.markdown("### 📜 Your Memory Lane")
    
    # Check if the file exists yet
    if not os.path.exists("my_diary_history.txt"):
        st.info("Your memory lane is empty! Write your first entry in the other tab to start your history. ✨")
    else:
        # Read the file and split entries by our delimiter '###'
        with open("my_diary_history.txt", "r", encoding="utf-8") as f:
            content = f.read()
        
        entries = content.split("###")
        
        # Filter out any empty splits and reverse them so the NEWEST diaries show up at the top
        valid_entries = [e.strip() for e in entries if e.strip()]
        
        if not valid_entries:
            st.info("No entries recorded yet!")
        else:
            for item in reversed(valid_entries):
                # Pull out the lines to display neatly
                lines = item.split("\n")
                entry_date = "Unknown Date"
                user_text = ""
                ai_text = []
                
                # Parse the saved text structure
                for line in lines:
                    if line.startswith("DATE:"):
                        entry_date = line.replace("DATE:", "").strip()
                    elif line.startswith("USER:"):
                        user_text = line.replace("USER:", "").strip()
                    elif line.startswith("AI:") or len(ai_text) > 0:
                        # Catching the AI outputs lines
                        clean_line = line.replace("AI:", "").strip()
                        if clean_line:
                            ai_text.append(clean_line)
                
                # Create a cute drop-down card for each past day!
                with st.expander(f"📅 {entry_date}"):
                    st.markdown("**What you wrote:**")
                    st.write(f"*{user_text}*")
                    st.markdown("**🧸 MoodBuddy's Response:**")
                    st.write("\n".join(ai_text))