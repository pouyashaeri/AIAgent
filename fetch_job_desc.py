# fetch_job_desc.py

import requests
from bs4 import BeautifulSoup

def save_job_description_from_url(url, output_path="job_description.txt"):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Try to extract main job description text
    # (This may vary per website!)
    job_text = soup.get_text(separator="\n")  # Fallback: whole page text
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(job_text)
    print(f"Saved job description from {url} to {output_path}")

if __name__ == "__main__":
    url = input("Paste job URL: ").strip()
    save_job_description_from_url(url)