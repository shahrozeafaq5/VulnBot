import requests
from datetime import datetime, timedelta, timezone

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


def fetch_recent_nvd(days=2):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)

    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "pubEndDate": end.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "resultsPerPage": 20,
    }

    res = requests.get(NVD_API_URL, params=params, timeout=30)
    res.raise_for_status()

    data = res.json()
    results = []

    for item in data.get("vulnerabilities", []):
        cve = item.get("cve", {})
        cve_id = cve.get("id")
        

        descriptions = cve.get("descriptions", [])
        description = ""
        for desc in descriptions:
            if desc.get("lang") == "en":
                description = desc.get("value", "")
                break

        metrics = cve.get("metrics", {})
        cvss_score = None
        severity = "Unknown"

        if "cvssMetricV31" in metrics:
            cvss_data = metrics["cvssMetricV31"][0]["cvssData"]
            cvss_score = cvss_data.get("baseScore")
            severity = cvss_data.get("baseSeverity", "Unknown")
        elif "cvssMetricV30" in metrics:
            cvss_data = metrics["cvssMetricV30"][0]["cvssData"]
            cvss_score = cvss_data.get("baseScore")
            severity = cvss_data.get("baseSeverity", "Unknown")
        elif "cvssMetricV2" in metrics:
            cvss_data = metrics["cvssMetricV2"][0]["cvssData"]
            cvss_score = cvss_data.get("baseScore")
            severity = metrics["cvssMetricV2"][0].get("baseSeverity", "Unknown")

        results.append({
            "source": "NVD",
            "cveID": cve_id,
            "vendorProject": "Unknown",
            "product": "Unknown",
            "vulnerabilityName": description[:120],
            "notes": description,
            "requiredAction": "Review vendor advisory and apply available patches or mitigations.",
            "dueDate": "N/A",
            "dateAdded": cve.get("published", "")[:10],
            "severity": severity,
            "cvssScore": cvss_score,
        })

    return results

def fetch_nvd_by_cve(cve_id):
    params = {
        "cveId": cve_id
    }

    res = requests.get(NVD_API_URL, params=params, timeout=30)
    res.raise_for_status()

    data = res.json()
    vulnerabilities = data.get("vulnerabilities", [])

    if not vulnerabilities:
        return {
            "severity": "Unknown",
            "cvssScore": "N/A"
        }

    cve = vulnerabilities[0].get("cve", {})
    metrics = cve.get("metrics", {})

    if "cvssMetricV31" in metrics:
        cvss_data = metrics["cvssMetricV31"][0]["cvssData"]
        return {
            "severity": cvss_data.get("baseSeverity", "Unknown"),
            "cvssScore": cvss_data.get("baseScore", "N/A")
        }

    if "cvssMetricV30" in metrics:
        cvss_data = metrics["cvssMetricV30"][0]["cvssData"]
        return {
            "severity": cvss_data.get("baseSeverity", "Unknown"),
            "cvssScore": cvss_data.get("baseScore", "N/A")
        }

    if "cvssMetricV2" in metrics:
        metric = metrics["cvssMetricV2"][0]
        cvss_data = metric.get("cvssData", {})
        return {
            "severity": metric.get("baseSeverity", "Unknown"),
            "cvssScore": cvss_data.get("baseScore", "N/A")
        }

    return {
        "severity": "Unknown",
        "cvssScore": "N/A"
    }