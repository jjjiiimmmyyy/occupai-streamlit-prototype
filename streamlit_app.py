import streamlit as st
import openai
import os

# Load the OpenAI API key from environment variables
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")

st.title("OccuPAI - Job Task Analyzer")

task = st.text_area("Describe your task", height=150)
tool = st.text_area("Describe the AI prompt or tool you used", height=100)

if st.button("🔍 Analyze Task"):
    if not task or not tool:
        st.warning("Please fill in both fields before submitting.")
    else:
        with st.spinner("Analyzing..."):
            try:
                # This uses the new SDK method
                response = openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an AI job analyst. Evaluate the task and prompt."},
                        {"role": "user", "content": f"Task: {task}\n\nTool: {tool}\n\nGive feedback on effectiveness and potential improvements."}
                    ],
                    temperature=0.7,
                )
                st.success("✅ Analysis Complete")
                st.markdown("### 💬 AI Feedback")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
