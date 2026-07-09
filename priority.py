RISK_WEIGHT = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1,
    "Unknown": 0
}

RELEVANCE_WEIGHT = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1,
    "Unknown": 0
}


def calculate_priority_score(vuln, analysis):
    score = 0

    cvss = vuln.get("cvssScore")
    try:
        if cvss != "N/A":
            score += float(cvss) * 5
    except:
        pass

    if vuln.get("source") == "CISA KEV":
        score += 25

    risk_level = analysis.get("risk_level", "Unknown")
    relevance = analysis.get("personal_relevance", "Unknown")

    score += RISK_WEIGHT.get(risk_level, 0) * 8
    score += RELEVANCE_WEIGHT.get(relevance, 0) * 8

    return min(round(score), 100)


def sort_report_items(report_items):
    return sorted(
        report_items,
        key=lambda item: item.get("priority_score", 0),
        reverse=True
    )