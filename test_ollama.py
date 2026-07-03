from ollama_client import analyze_vulnerability

sample = """
CVE: CVE-2025-1234
Vendor: Microsoft
Product: Windows
Vulnerability: Remote Code Execution
Required Action: Apply latest security update.
"""

result = analyze_vulnerability(sample)

print(result)