# BrightEdge URL Crawler Assignment

**Candidate:** Soundarya Beathnabotla

---

## Overview

A URL crawler that fetches any webpage, extracts metadata (title, description, body preview), and classifies topics automatically. Built in Python and deployed on AWS Lambda with a live API endpoint.

---

## Live API

**Endpoint:**

```
GET https://femqsni8gc.execute-api.us-east-2.amazonaws.com/default/brightedge-url-crawler?url=YOUR_URL
```

**Click to test live:**
- [Test with CNN](https://femqsni8gc.execute-api.us-east-2.amazonaws.com/default/brightedge-url-crawler?url=https://www.cnn.com)
- [Test with Amazon](https://femqsni8gc.execute-api.us-east-2.amazonaws.com/default/brightedge-url-crawler?url=https://www.amazon.com)
- [Test with Example.com](https://femqsni8gc.execute-api.us-east-2.amazonaws.com/default/brightedge-url-crawler?url=https://example.com)

---

## Example Outputs

### Success - CNN

```json
{
  "url": "https://www.cnn.com",
  "title": "Breaking News, Latest News and Videos | CNN",
  "description": "View the latest news and breaking news today for U.S., world, weather, entertainment, politics and health at CNN.com.",
  "body_preview": "CNN values your feedback...",
  "topics": [
    "technology",
    "news"
  ],
  "status": "success"
}
```

### Success - Amazon

```json
{
  "url": "https://www.amazon.com",
  "title": "Amazon.com",
  "description": "",
  "body_preview": "Click the button below to continue shopping...",
  "topics": [
    "shopping"
  ],
  "status": "success"
}
```

### Graceful Failure - Anti-bot Protected Site

```json
{
  "url": "https://www.rei.com",
  "status": "failed",
  "error": "The read operation timed out",
  "note": "Site may have anti-bot protection or be temporarily unavailable"
}
```

---

## Architecture Flow

User Request (URL) → API Gateway (HTTP GET) → AWS Lambda (Python) → urllib.request (Fetch HTML) → MetadataParser (HTMLParser) → Extract Metadata → classify_topics() → JSON Response

---

## Topic Classification

Topics are classified using **keyword-based matching** across title, description, and body text.

| Topic | Sample Keywords |
|------------|-------------------------------|
| technology | ai, tech, software, computer |
| shopping | buy, price, product, amazon |
| outdoors | camp, hiking, outdoor, trail |
| news | breaking, report, cnn, today |

> **Note:** This is intentionally simple for the POC. In production, this can be replaced with an ML model (e.g. zero-shot classification using HuggingFace transformers) for higher accuracy.

---

## Scale Design (Billions of URLs)

See `design.md` for the full architecture. Key assumptions:

| Assumption | Value |
|------------------------|------------------------|
| Target URL volume | 1 billion+ URLs |
| Crawl throughput | ~10,000 URLs/second |
| Storage per URL | ~2 KB metadata |
| Total storage estimate | ~2 TB per billion URLs |
| Deduplication | URL hash via DynamoDB |
| Fault tolerance | SQS dead-letter queues |

**Stack:** AWS SQS → Lambda → S3 → DynamoDB → Athena

---

## Files

| File | Description |
|--------------|--------------------------------------|
| `crawler.py` | Core crawler logic (Part 1) |
| `design.md` | Distributed system design (Part 2) |
| `poc_plan.md` | POC phases, estimates, release plan (Part 3) |

---

## How to Run Locally

```bash
pip install requests beautifulsoup4
python crawler.py
```

---

## AWS Deployment

- **Runtime:** Python 3.12
- **Region:** us-east-2
- **Function:** brightedge-url-crawler
- **Trigger:** API Gateway (public HTTP endpoint)
- **Timeout:** 30 seconds

---

## Known Limitations

- Some sites (REI, LinkedIn) block AWS Lambda IPs via Cloudflare — handled gracefully with error response
- `body_preview` limited to 300 characters to stay within Lambda response limits
- Topic classification is keyword-based (not semantic)

---

## AI Tools Used

- **Claude AI:** Architecture design, debugging assistance
- **GitHub Copilot:** Code suggestions
- All decisions reviewed and validated personally