import ollama


MODEL_NAME = "qwen2.5-coder:7b "


def analyze_vulnerability(vuln_text):
    prompt = f"""
You are a cybersecurity analyst.

Analyze this vulnerability in simple words.

Return the answer in this format:

What happened:
Who is affected:
Why it matters:
Recommended action:

Keep it short and easy to understand.

Vulnerability details:
{vuln_text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]