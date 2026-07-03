import os
import json
import requests
from dotenv import load_dotenv
from email_utils import send_email
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
SEEN_FILE = "seen_cves.json"

CISA_KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

HF_API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-cnn"


def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(json.load(f))


def save_seen(cves):
    with open(SEEN_FILE, "w") as f:
        json.dump(sorted(list(cves)), f, indent=2)


def fetch_cisa_kev():
    res = requests.get(CISA_KEV_URL, timeout=20)
    res.raise_for_status()
    return res.json()["vulnerabilities"]


def summarize_with_hf(text):
    
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": text,
        "parameters": {
            "max_length": 80,
            "min_length": 25,
            "do_sample": False
        }
    }

    res = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)

    if res.status_code != 200:
    print("HF ERROR:", res.status_code, res.text)
    return "Summary unavailable. Hugging Face API error."

    data = res.json()
    return data[0]["summary_text"]


def main():
    send_email(
        subject="✅ VulnBot Test",
        body="GitHub Actions ran successfully and Gmail is working."
    )
    seen = load_seen()
    vulnerabilities = fetch_cisa_kev()

    new_items = []

    for vuln in vulnerabilities:
        cve_id = vuln.get("cveID")

        if cve_id not in seen:
            new_items.append(vuln)

    if not new_items:
        print("No new vulnerabilities found.")
        return

    print(f"Found {len(new_items)} new vulnerabilities.\n")

    for vuln in new_items[:5]:
        cve_id = vuln.get("cveID")
        vendor = vuln.get("vendorProject")
        product = vuln.get("product")
        name = vuln.get("vulnerabilityName")
        notes = vuln.get("notes", "")
        action = vuln.get("requiredAction")
        due_date = vuln.get("dueDate")

        text = f"""
        CVE: {cve_id}
        Vendor: {vendor}
        Product: {product}
        Vulnerability: {name}
        Notes: {notes}
        Required Action: {action}
        Due Date: {due_date}
        """

        summary = summarize_with_hf(text)

        email_body = f"""
         New Vulnerability Alert

        CVE: {cve_id}
        Vendor/Product: {vendor} {product}
        Issue: {name}

        AI Summary:
        {summary}

        Required Action:
        {action}

        Due Date:
        {due_date}
            """

        send_email(
        subject=f"🚨 VulnBot Alert: {cve_id}",
        body=email_body)
        print("=" * 60)
        print(f"CVE: {cve_id}")
        print(f"Vendor/Product: {vendor} {product}")
        print(f"Issue: {name}")
        print(f"AI Summary: {summary}")
        print(f"Action: {action}")
        print(f"Due Date: {due_date}")

        seen.add(cve_id)

    save_seen(seen)


if __name__ == "__main__":
    main()