import streamlit as st
import openai
import os

# Load your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("OccupAI Prototype")
st.subheader("Analyze AI-generated tasks and prompts")

# Input fields
user_task = st.text_area("Describe your task", height=150)
ai_prompt = st.text_area("Describe the AI prompt or tool you used", height=100)

if st.button("🔍 Analyze Task"):
    if not user_task or not ai_prompt:
        st.warning("Please fill in both fields.")
    else:
        with st.spinner("Analyzing..."):
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are an AI expert helping to analyze how people use language models. "
                                "Given a task description and an AI prompt, explain what kind of AI behavior is being used "
                                "and how well the prompt matches the task. Offer suggestions if something could be improved."
                            ),
                        },
                        {"role": "user", "content": f"Task:\n{user_task}\n\nPrompt:\n{ai_prompt}"},
                    ],
                    temperature=0.7,
                )
                result = response.choices[0].message.content.strip()
                st.success("Analysis complete:")
                st.markdown(result)
            except Exception as e:
                st.error(f"❌ Error: {e}")
