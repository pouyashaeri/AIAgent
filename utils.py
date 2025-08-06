# utils.py

import os
import openai
from datetime import datetime
from dotenv import load_dotenv

# Load the OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Hardcoded email signature
SIGNATURE = """
Best regards,
Pouya Shaeri  
https://www.linkedin.com/in/pouyashaeri/  
https://pouyashaeri.github.io
""".strip()

def generate_followup_email(resume_text, job_description, recipient_email):
    system_prompt = (
        "You are an expert job recruiter assistant. Write a concise and personalized follow-up email "
        "on behalf of a candidate who has applied for a job. Use their resume and the job description "
        "to highlight key alignments. Keep the tone polite and professional. "
        "Start the email directly without any salutation like 'Dear [Name]'. Just say 'Hi, ' at the beginning."
        "Do not include any signature or contact info at the end."
        "I already have 'Best regards,' in my signature, so do not include it."
    )

    user_prompt = (
        f"Resume:\n{resume_text}\n\n"
        f"Job Description:\n{job_description}\n\n"
        f"Write a concise follow-up email based on the above. "
        f"Do NOT include any greeting or signature. "
        f"Start the email directly and keep the tone polite and professional."
        f"I already have 'Best regards,' in my signature, so do not include it."
    )

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    body = response.choices[0].message.content.strip()
    return f"{body}\n\n{SIGNATURE}"


def log_interaction(email, job_title, status, logfile="log.csv"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{now},{email},{job_title},{status}\n"
    with open(logfile, "a") as f:
        f.write(line)
