import requests
from config import HF_TOKEN, HF_API_URL, HF_MODEL


def analyze_vulnerability(vuln_text):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    messages = [
        {
            "role": "system",
            "content": "You are a senior cybersecurity analyst. Give clear, practical vulnerability analysis."
        },
        {
            "role": "user",
            "content": f"""
Analyze this vulnerability.

Return exactly these sections:
1. What happened
2. Who is affected
3. Why it matters
4. Risk level: Low/Medium/High/Critical
5. Should I care?
6. Recommended action

Keep it under 180 words.

Vulnerability details:
{vuln_text}
"""
        }
    ]

    payload = {
        "model": HF_MODEL,
        "messages": messages,
        "max_tokens": 220,
        "temperature": 0.2
    }

    res = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

    if res.status_code != 200:
        print("HF ERROR:", res.status_code, res.text)
        return "AI analysis unavailable. Hugging Face API error."

    data = res.json()
    return data["choices"][0]["message"]["content"]