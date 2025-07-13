import streamlit as st
from openai import OpenAI
import os

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.title("OccupAI™ Task Analyzer")

st.write("### Describe your task")
task_input = st.text_area("What are you working on?", height=180)

st.write("### Describe the AI prompt or tool you used")
tool_input = st.text_area("What prompt or tool did you use?", height=120)

if st.button("🔍 Analyze Task"):
    if not task_input.strip() or not tool_input.strip():
        st.warning("Please fill in both fields.")
    else:
        with st.spinner("Analyzing your task..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert at classifying and evaluating modern AI tasks across productivity, creativity, and research. Analyze the user's task and tool."
                        },
                        {
                            "role": "user",
                            "content": f"Task: {task_input}\n\nTool or Prompt Used: {tool_input}"
                        }
                    ],
                    temperature=0.6
                )
                result = response.choices[0].message.content
                st.success("Analysis complete:")
                st.markdown(result)
            except Exception as e:
                st.error(f"Something went wrong: {e}")
