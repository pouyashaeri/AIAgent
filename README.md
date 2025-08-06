# AI Agent for Automated Job Application Follow-Up

This project is an AI-powered agent that automatically sends personalized follow-up emails after job applications. It extracts information from a resume and the job description, uses GPT-4o-mini to generate a professional email, and sends it via the Gmail API.

## Features

- Automatically downloads the job description from a URL
- Extracts resume text from a PDF file
- Uses OpenAI's GPT-4o-mini to write a personalized follow-up email
- Sends the email through your Gmail account using OAuth2
- Logs every email interaction to a CSV file

---

## Folder Structure

```
AIAGENT/
├── creds/                  # Google API credentials (token.json, credentials.json)
├── resume/                 # Your resume PDF (named resume.pdf)
├── job_description.txt     # Automatically generated job description file
├── log.csv                 # Log file recording sent emails
├── .env                    # Environment variables
├── main.py                 # Main script to run the agent
├── utils.py                # Utility functions (email generation and logging)
└── README.md               # Project documentation
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/AIAGENT.git
cd AIAGENT
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages include:
- `openai`
- `python-dotenv`
- `PyPDF2`
- `google-auth`
- `google-auth-oauthlib`
- `google-api-python-client`
- `requests`
- `beautifulsoup4`

### 3. Prepare Your `.env` File

Create a `.env` file in the root directory and populate it as follows:

```env
OPENAI_API_KEY=your_openai_api_key
SENDER_EMAIL=your_gmail_address@gmail.com
TARGET_EMAIL=recipient_email@example.com
JOB_LINK=https://example.com/job-posting
```

### 4. Add Your Resume

Place your resume PDF in the `resume/` folder and name it `resume.pdf`.

### 5. Setup Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the Gmail API
3. Create OAuth 2.0 credentials for a desktop app
4. Download the `credentials.json` and place it inside the `creds/` folder

The first time you run the script, a browser window will open asking for Gmail permission. It will generate a `token.json` file for future use.

---

## Running the Agent

```bash
python main.py
```

This will:
1. Download the job description from the link in `.env`
2. Extract resume text
3. Generate a follow-up email using GPT-4o-mini
4. Send the email to the target address
5. Log the interaction in `log.csv`

---

## Customization

You can edit the email subject in `main.py`:

```python
subject = "Follow-up: Student Researcher 2025 Application"
```

My signature is just an example. You can modify the email signature in `utils.py`:

```python
SIGNATURE = """
Best regards,
Pouya Shaeri  
https://www.linkedin.com/in/pouyashaeri/  
https://pouyashaeri.github.io
""".strip()
```

---

## License

This project is intended for personal and academic use only. Please respect all API terms of service (OpenAI, Google).

---

## Author

Pouya Shaeri  
PhD Student, Arizona State University  
[LinkedIn](https://www.linkedin.com/in/pouyashaeri/) | [GitHub](https://pouyashaeri.github.io)