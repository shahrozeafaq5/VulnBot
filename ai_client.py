import requests
from config import HF_TOKEN, HF_API_URL


def analyze_vulnerability(vuln_text):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a cybersecurity analyst.

Analyze this vulnerability and write a short security report.

Include:
1. What happened
2. Who is affected
3. Why it matters
4. Risk level
5. Recommended action

Keep it simple and under 180 words.

Vulnerability details:
{vuln_text}
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_length": 180,
            "min_length": 40,
            "do_sample": False
        }
    }

    res = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

    if res.status_code != 200:
        print("HF ERROR:", res.status_code, res.text)
        return "AI analysis unavailable. Hugging Face API error."

    data = res.json()
    return data[0]["summary_text"]