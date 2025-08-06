# utils.py

import os
import openai
from datetime import datetime
from dotenv import load_dotenv

# Load the OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_followup_email(resume_text, job_description, recipient_email):
    system_prompt = (
        "You are an expert job recruiter assistant. Write a concise and personalized follow-up email "
        "on behalf of a candidate who has applied for a job. Use their resume and the job description "
        "to highlight key alignments. Keep the tone polite and professional. "
        "Start the email directly without any salutation like 'Dear [Name]'. "
        "Do not include placeholders or generic greetings."
    )

    user_prompt = (
    f"Resume:\n{resume_text}\n\n"
        f"Job Description:\n{job_description}\n\n"
        f"Write a concise follow-up email based on the above. "
        f"Do NOT include any greeting like 'Dear [Name]' or placeholders. "
        f"Start the email directly and keep the tone polite and professional."
    )


    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


def log_interaction(email, job_title, status, logfile="log.csv"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{now},{email},{job_title},{status}\n"
    with open(logfile, "a") as f:
        f.write(line)
