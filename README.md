# BrightEdge URL Crawler Assignment
**Candidate:** Soundarya Beathnabotla

---

## Overview
A URL crawler that fetches any webpage, extracts metadata, and classifies topics. Built in Python and deployed on AWS Lambda.

## Architecture
Crawler → HTML Parsing → Metadata Extraction → Topic Classification → JSON Output → API Response

---

## Files
- `crawler.py` — Core crawler (Part 1)
- `design.md` — System design for billions of URLs (Part 2)
- `poc_plan.md` — Proof of concept plan (Part 3)

---

## How to Run Locally

Install dependencies:

    pip install requests beautifulsoup4

Run the crawler:

    python crawler.py

---

## AWS Lambda API Demo

Public API Endpoint:
https://femqsni8gc.execute-api.us-east-2.amazonaws.com/default/brightedge-url-crawler

Example Request:

    GET https://femqsni8gc.execute-api.us-east-2.amazonaws.com/default/brightedge-url-crawler?url=https://www.cnn.com

Example Output:

    {
      "url": "https://www.cnn.com",
      "title": "Breaking News, Latest News and Videos | CNN",
      "description": "View the latest news and breaking news today...",
      "body_preview": "CNN values your feedback...",
      "topics": ["technology", "news"],
      "status": "success"
    }

---

## What it does
- Accepts any URL as input
- Fetches the page content
- Extracts title, description, body
- Classifies topics automatically
- Handles errors gracefully

---

## AWS Deployment
- Deployed on AWS Lambda (us-east-2)
- Function: brightedge-url-crawler
- Runtime: Python 3.14
- API Gateway: Public HTTP endpoint
- API Endpoint: https://femqsni8gc.execute-api.us-east-2.amazonaws.com/default/brightedge-url-crawler
- Successfully tested with CNN, example.com

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