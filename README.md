#  VulnBot

An AI-powered vulnerability intelligence assistant that continuously monitors newly published vulnerabilities from multiple trusted threat intelligence sources, enriches them with CVSS data, analyzes their impact using Google's Gemma instruction model, prioritizes findings based on the user's environment, and automatically delivers professional HTML security reports via email.

---

#  Features

-  Monitors newly published vulnerabilities
-  Collects intelligence from CISA KEV and NVD
-  Enriches vulnerabilities with CVSS scores and severity
-  Uses Google's Gemma 4 instruction model for AI-powered security analysis
-  Personalizes recommendations using a user environment profile
-  Generates professional HTML email reports
-  Runs automatically every 6 hours using GitHub Actions
-  Calculates a priority score for every vulnerability

---

#  Architecture

```
                    GitHub Actions
                 (Every 6 Hours)
                        │
                        ▼
          ┌───────────────────────────┐
          │   Fetch Vulnerabilities   │
          └───────────────────────────┘
              │                 │
              ▼                 ▼
          CISA KEV            NVD API
              │                 │
              └────────┬────────┘
                       ▼
          Merge & Enrich Vulnerabilities
                       ▼
             Load User Environment
                       ▼
          AI Security Analysis (Gemma)
                       ▼
        Priority Scoring & Ranking
                       ▼
           HTML Report Generation
                       ▼
             Gmail Notification
```

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| AI Model | Google Gemma 4 31B Instruct |
| AI Provider | Hugging Face Inference |
| Threat Sources | CISA KEV, NVD |
| Automation | GitHub Actions |
| Email | Gmail SMTP |
| Data Format | JSON |
| Reports | HTML |

---

#  Project Structure

```text
VulnBot/
│
├── .github/
│   └── workflows/
│       └── vulnbot.yml
│
├── ai_client.py
├── cisa_client.py
├── config.py
├── email_utils.py
├── main.py
├── nvd_client.py
├── priority.py
├── profile_loader.py
├── profile.json
├── report_builder.py
├── storage.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Setup Instructions

## 1. Clone the repository

```bash
git clone https://github.com/shahrozeafaq5/VulnBot.git
cd VulnBot
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Linux/macOS**

```bash
source venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create a `.env` file

```env
HF_TOKEN=your_huggingface_token
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_gmail_app_password
TO_EMAIL=receiver_email@gmail.com
TEST_MODE=false
```

---

## 5. Configure your environment profile

Update `profile.json`:

```json
{
  "operating_systems": ["Windows 11", "Kali Linux"],
  "languages": ["Python"],
  "frameworks": ["FastAPI", "React"],
  "vendors": ["Microsoft", "Cisco"]
}
```

---

## 6. Run locally

```bash
python main.py
```

---

## 7. GitHub Actions

Create these repository secrets:

- HF_TOKEN
- GMAIL_USER
- GMAIL_APP_PASSWORD
- TO_EMAIL
- TEST_MODE

The workflow runs automatically every 6 hours.

---

#  Example Output

The report includes:

- Executive vulnerability details
- CVSS score
- Severity
- Priority score
- AI security analysis
- Personal relevance
- Recommended actions

---

#  Future Improvements

- PDF security reports
- Slack / Discord / Microsoft Teams notifications
- Additional threat intelligence sources
- CVE search dashboard
- Real-time webhook notifications
- Threat trend visualization
- Organization-wide asset inventory integration

---

#  License

This project is licensed under the MIT License.
