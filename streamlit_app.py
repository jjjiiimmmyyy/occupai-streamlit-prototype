import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="OccupAI - AI Applicability Score", layout="centered")

st.title("🧠 OccupAI™ — AI Labor Shift Scoring Tool")
st.markdown("Estimate how much generative AI can assist with or perform your work task.")

# Input fields
job_title = st.text_input("Job Title", "Customer Service Representative")
task_description = st.text_area("Describe your task", "Writing personalized responses to customer complaints about delivery issues.")
ai_prompt = st.text_area("Describe the AI prompt or tool you used", "I used ChatGPT to write an email response to a frustrated customer about a late shipment.")

submit = st.button("🔍 Analyze Task")

if submit:
    with st.spinner("Classifying and scoring your task..."):
        # Construct the GPT prompt
        system_prompt = (
            "You are a labor economist trained on O*NET occupational standards and generative AI use cases. "
            "Your task is to analyze how much of a user's described task is currently supported by AI. "
            "Your output should classify the task's AI applicability across three dimensions: Coverage, Completion, and Scope."
        )

        user_prompt = f"""
        Job Title: {job_title}
        Task Description: {task_description}
        AI Prompt Used: {ai_prompt}

        Based on this input, answer the following:
        1. Which O*NET Intermediate Work Activities (IWAs) best describe this task? List up to 3.
        2. How much of the task is covered by current AI tools like ChatGPT or Bing Copilot? (0 to 1 scale)
        3. What is the likely success rate for AI in performing or assisting with this task? (0 to 1 scale)
        4. How broad is the AI's impact on this type of task? Choose one: None, Minimal, Limited, Moderate, Significant, Complete
        5. Brief explanation for the above scores.

        Return your answer as a JSON object.
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )

            reply = response.choices[0].message.content
            import json
            result = json.loads(reply)

            st.success("AI Applicability Score calculated!")

            # Scope rating mapping
            scope_map = {
                "None": 0.0, "Minimal": 0.2, "Limited": 0.4,
                "Moderate": 0.6, "Significant": 0.8, "Complete": 1.0
            }

            score = round(result["coverage_score"] * result["completion_score"] * scope_map[result["scope_rating"]], 3)

            st.metric("AI Applicability Score", score)
            st.markdown("### Top Matching IWAs")
            st.write(result["iwAs"])
            st.markdown("### Scoring Breakdown")
            st.write(f"Coverage: {result['coverage_score']}")
            st.write(f"Completion: {result['completion_score']}")
            st.write(f"Scope: {result['scope_rating']}")
            st.markdown("### Explanation")
            st.info(result["justification"])

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.stop()

st.markdown("---")
st.caption("Built with ❤️ by OccupAI™ | Pre-Seed Prototype v0.1")
