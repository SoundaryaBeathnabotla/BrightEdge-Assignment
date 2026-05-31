# BrightEdge URL Crawler - System Design
## Scaling to Billions of URLs

---

## 1. Architecture Overview

For processing billions of URLs, we need a distributed, fault-tolerant system.

URLs Input (text file / MySQL)
        ↓
   Message Queue (AWS SQS)
        ↓
   Worker Fleet (AWS Lambda / EC2)
        ↓
   Crawler Service (Python)
        ↓
   Raw Storage (AWS S3)
        ↓
   Metadata Store (AWS DynamoDB)
        ↓
   Analytics Layer (AWS Athena)
        ↓
   Monitoring (AWS CloudWatch)

---

## 2. Input Sources

The system accepts billions of URLs from two sources:

### Option A - Text File
- URLs stored in a .txt file, one per line
- Uploaded to S3
- Lambda reads and pushes each URL to SQS queue

### Option B - MySQL Database
- URLs stored in MySQL table with year_month column
- Example: all URLs for July 2024
- Query: SELECT url FROM urls WHERE year_month = '2024-07'
- Results pushed to SQS queue in batches of 1000

### Input Flow

Text File / MySQL
        ↓
   Input Processor (Lambda)
        ↓
   AWS SQS Queue
        ↓
   Crawler Workers (Lambda)
        ↓
   S3 + DynamoDB Storage

---

## 3. Data Schema

URL: https://example.com
crawled_at: 2024-07-01T10:00:00Z
title: Page Title
description: Meta description
body_preview: First 500 chars...
topics: ["technology", "news"]
status: success
http_status: 200
year_month: 2024-07

---

## 4. Scale Design

| Component | Choice | Reason |
|---|---|---|
| Queue | AWS SQS | Handles millions of messages |
| Workers | AWS Lambda | Auto-scales, pay per use |
| Storage | AWS S3 | Cheap, unlimited storage |
| Database | DynamoDB | Fast key-value lookups |
| Analytics | Athena | SQL on S3, no servers |
| Monitoring | CloudWatch | AWS native, real-time |

---

## 5. Cost Optimization

- Use S3 Intelligent Tiering — auto moves old data to cheaper storage
- Lambda spot instances for workers — 70% cheaper
- Compress data before storing in S3 (gzip)
- Cache frequently accessed URLs in ElastiCache
- Partition Athena tables by year/month — reduces query cost

---

## 6. Performance Optimization

- Process URLs in parallel — 1000 Lambda workers simultaneously
- Retry failed URLs with exponential backoff
- Use connection pooling for database writes
- CDN caching for frequently requested metadata

---

## 7. Reliability

- SQS dead letter queue — failed URLs retried 3 times
- Multi-region deployment — US-East and US-West
- Circuit breaker pattern — stop crawling if error rate exceeds 10%
- Daily backups of DynamoDB to S3

---

## 8. API Layer - Millions of Requests

To allow millions of requests on the crawled content:

- AWS API Gateway — handles millions of requests per second
- Lambda functions — serve metadata on demand
- ElastiCache (Redis) — cache hot URLs for instant response
- CloudFront CDN — distribute responses globally

API Response time target: less than 200ms for cached content

---

## 9. SLOs and SLAs

| Metric | Target |
|---|---|
| Crawl success rate | more than 95% |
| API response time | less than 200ms |
| System uptime | 99.9% |
| Data freshness | less than 24 hours |
| Error rate | less than 1% |

---

## 10. Monitoring Metrics

- URLs crawled per minute
- Error rate by domain
- Lambda execution time
- SQS queue depth
- S3 storage growth
- API latency (p50, p95, p99)

Tools: AWS CloudWatch, CloudWatch Alarms, AWS X-Ray for tracing

---

## 11. AI Tools Used

- Claude AI: System architecture design, cost optimization strategies
- GitHub Copilot: Code suggestions during crawler development
- All design decisions reviewed and validated personally

---

## 12. Throughput & Cost Analysis

### Target: 1 Billion URLs

**Step 1 — Required throughput:**
- 1,000,000,000 URLs ÷ 86,400 seconds/day = ~11,574 URLs/sec to finish in 1 day
- Rounded target: ~10,000 URLs/sec sustained

**Step 2 — Worker count:**
- Average HTTP fetch latency: 1–3 seconds per URL
- To sustain 10,000 req/sec with 2s avg latency → 20,000 concurrent workers needed
- Lambda default concurrency limit: 1,000 per region
- Solution: Request AWS limit increase to 20,000 (standard enterprise request) OR distribute across 2–3 AWS regions (us-east-1, us-west-2, eu-west-1) → ~7,000 workers per region, within limits

**Step 3 — Per-domain rate limiting:**
- Hammering a single domain at 10,000 req/sec triggers IP bans (as seen with REI/Cloudflare)
- Solution: SQS FIFO queues per domain with max 1–5 req/sec per domain
- Total concurrency stays high, but spread across millions of unique domains

**Step 4 — Cost estimate (monthly):**

| Resource | Usage | Est. Cost/month |
|---|---|---|
| Lambda | 1B invocations × 2s × 128MB | ~$2,000 |
| SQS | 1B messages | ~$400 |
| S3 | 2TB storage + PUT requests | ~$150 |
| DynamoDB | 1B writes (dedup table) | ~$1,250 |
| Athena | 10TB scanned/month | ~$50 |
| **Total** | | **~$3,850/month** |

**Step 5 — Optimization levers:**
- Use Spot-based ECS Fargate instead of Lambda for sustained crawls → 60–70% cost reduction
- Parquet + S3 instead of raw HTML → 10x storage reduction
- DynamoDB TTL to expire old URLs and control table size