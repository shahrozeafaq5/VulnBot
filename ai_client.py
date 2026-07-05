import json
import requests
from config import HF_TOKEN, HF_API_URL, HF_MODEL


def analyze_vulnerability(vuln_text, user_profile):
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    messages = [
        {
            "role": "system",
            "content": "You are a senior cybersecurity analyst. Return only valid JSON. No markdown."
        },
        {
            "role": "user",
            "content": f"""
Analyze this vulnerability for the user's environment.

User environment:
{user_profile}

Return ONLY valid JSON in this exact format:

{{
  "what_happened": "",
  "who_is_affected": "",
  "personal_relevance": "Low/Medium/High/Critical",
  "relevance_reason": "",
  "risk_level": "Low/Medium/High/Critical",
  "should_i_care": "Yes/No",
  "recommended_action": ""
}}

Vulnerability details:
{vuln_text}
"""
        }
    ]

    payload = {
        "model": HF_MODEL,
        "messages": messages,
        "max_tokens": 350,
        "temperature": 0.1
    }

    res = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

    if res.status_code != 200:
        print("HF ERROR:", res.status_code, res.text)
        return {
            "what_happened": "AI analysis unavailable.",
            "who_is_affected": "Unknown",
            "personal_relevance": "Unknown",
            "relevance_reason": "Hugging Face API error.",
            "risk_level": "Unknown",
            "should_i_care": "Unknown",
            "recommended_action": "Review the vulnerability manually."
        }

    content = res.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("JSON PARSE ERROR:", content)
        return {
            "what_happened": content,
            "who_is_affected": "Unknown",
            "personal_relevance": "Unknown",
            "relevance_reason": "Model did not return valid JSON.",
            "risk_level": "Unknown",
            "should_i_care": "Unknown",
            "recommended_action": "Review the vulnerability manually."
        }