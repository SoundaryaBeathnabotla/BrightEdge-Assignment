# BrightEdge URL Crawler Assignment
**Candidate:** Soundarya Beathnabotla

---

## Files
- `crawler.py` — Core crawler (Part 1)
- `design.md` — System design for billions of URLs (Part 2)
- `poc_plan.md` — Proof of concept plan (Part 3)

---

## How to Run

Install dependencies:

    pip install requests beautifulsoup4

Run the crawler:

    python crawler.py

---

## What it does
- Accepts any URL as input
- Fetches the page content
- Extracts title, description, body
- Classifies topics automatically
- Handles errors gracefully

---

## AI Tools Used
- Claude AI: Architecture design, debugging assistance
- GitHub Copilot: Code suggestions
- All decisions reviewed and validated personally

---

## Challenges and Solutions
- Anti-bot protection: Added User-Agent headers
- Timeouts: Added timeout parameter and try/except
- Scale: Designed AWS distributed architecture
## AWS Deployment
- Deployed on AWS Lambda (us-east-2)
- Function: brightedge-url-crawler
- Runtime: Python 3.14
- Successfully tested with CNN URL
- API Endpoint: https://femqsni8gc.execute-api.us-east-2.amazonaws.com/default/brightedge-url-crawler