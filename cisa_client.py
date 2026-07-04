import requests
from config import CISA_KEV_URL


def fetch_cisa_kev():
    res = requests.get(CISA_KEV_URL, timeout=20)
    res.raise_for_status()

    results = []

    for vuln in res.json().get("vulnerabilities", []):
        results.append({
            "source": "CISA KEV",
            "cveID": vuln.get("cveID"),
            "vendorProject": vuln.get("vendorProject"),
            "product": vuln.get("product"),
            "vulnerabilityName": vuln.get("vulnerabilityName"),
            "notes": vuln.get("notes", ""),
            "requiredAction": vuln.get("requiredAction"),
            "dueDate": vuln.get("dueDate"),
            "dateAdded": vuln.get("dateAdded"),
            "severity": "Known Exploited",
            "cvssScore": "N/A"
        })

    return results