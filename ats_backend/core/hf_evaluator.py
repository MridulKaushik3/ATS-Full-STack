from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=os.getenv("HF_API_KEY")
)

def evaluate_resume(resume_text, jd_text, prompt):
    messages = [
        {
            "role": "system",
            "content": "You are an ATS (Applicant Tracking System) resume evaluator."
        },
        {
            "role": "user",
            "content": f"""
{prompt}

Job Description:
{jd_text}

Resume:
{resume_text}

Respond ONLY in the requested format.
"""
        }
    ]

    response = client.chat_completion(
        messages=messages,
        max_tokens=400,
        temperature=0.2
    )

    return response.choices[0].message.content.strip()
