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

## 2. Data Schema

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

## 3. Scale Design

| Component | Choice | Reason |
|---|---|---|
| Queue | AWS SQS | Handles millions of messages |
| Workers | AWS Lambda | Auto-scales, pay per use |
| Storage | AWS S3 | Cheap, unlimited storage |
| Database | DynamoDB | Fast key-value lookups |
| Analytics | Athena | SQL on S3, no servers |
| Monitoring | CloudWatch | AWS native, real-time |

---

## 4. Cost Optimization

- Use S3 Intelligent Tiering — auto moves old data to cheaper storage
- Lambda spot instances for workers — 70% cheaper
- Compress data before storing in S3 (gzip)
- Cache frequently accessed URLs in ElastiCache
- Partition Athena tables by year/month — reduces query cost

---

## 5. Performance Optimization

- Process URLs in parallel — 1000 Lambda workers simultaneously
- Retry failed URLs with exponential backoff
- Use connection pooling for database writes
- CDN caching for frequently requested metadata

---

## 6. Reliability

- SQS dead letter queue — failed URLs retried 3 times
- Multi-region deployment — US-East and US-West
- Circuit breaker pattern — stop crawling if error rate exceeds 10%
- Daily backups of DynamoDB to S3

---

## 7. SLOs and SLAs

| Metric | Target |
|---|---|
| Crawl success rate | more than 95% |
| API response time | less than 200ms |
| System uptime | 99.9% |
| Data freshness | less than 24 hours |
| Error rate | less than 1% |

---

## 8. Monitoring Metrics

- URLs crawled per minute
- Error rate by domain
- Lambda execution time
- SQS queue depth
- S3 storage growth
- API latency (p50, p95, p99)

Tools: AWS CloudWatch, CloudWatch Alarms, AWS X-Ray for tracing

---

## 9. AI Tools Used

- Claude AI: System architecture design, cost optimization strategies
- GitHub Copilot: Code suggestions during crawler development
- All design decisions reviewed and validated personally