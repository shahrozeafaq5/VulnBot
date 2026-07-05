from datetime import date, timedelta
from config import TEST_MODE
from cisa_client import fetch_cisa_kev
from nvd_client import fetch_recent_nvd
from storage import load_seen, save_seen
from ai_client import analyze_vulnerability
from report_builder import build_vuln_text, build_email_section, build_email_report
from email_utils import send_email


def is_recent_vulnerability(vuln):
    today = date.today()
    yesterday = today - timedelta(days=1)

    return vuln.get("dateAdded") in {
        today.isoformat(),
        yesterday.isoformat()
    }


def main():
    seen = load_seen()

    cisa_vulns = fetch_cisa_kev()
    nvd_vulns = fetch_recent_nvd(days=2)

    vulnerabilities = cisa_vulns + nvd_vulns

    new_items = []

    for vuln in vulnerabilities:
        cve_id = vuln.get("cveID")

        if not cve_id:
            continue

        if TEST_MODE:
            new_items.append(vuln)
        elif is_recent_vulnerability(vuln) and cve_id not in seen:
            new_items.append(vuln)

    if not new_items:
        print("No new recent vulnerabilities found.")
        return

    print(f"Found {len(new_items)} new recent vulnerabilities.")

    email_sections = []

    for vuln in new_items[:5]:
        vuln_text = build_vuln_text(vuln)
        analysis = analyze_vulnerability(vuln_text)

        section = build_email_section(vuln, analysis)
        email_sections.append(section)

        seen.add(vuln.get("cveID"))

        print("=" * 60)
        print(section)

    final_report = build_email_report(email_sections, len(new_items))

    send_email(
        subject=f"🚨 VulnBot AI Report: {min(5, len(new_items))} Recent Vulnerabilities",
        body=final_report
    )

    save_seen(seen)


if __name__ == "__main__":
    main()