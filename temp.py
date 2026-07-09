import requests

url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

params = {
    "keywordSearch": "Microsoft SharePoint",
    "cvssV3Severity": "CRITICAL"
}

response = requests.get(url, params=params, timeout=20)
response.raise_for_status()

data = response.json()

print(data)

# for items in data["vulnerabilities"]:
#     print(items["cvss"])