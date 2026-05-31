import json
import urllib.request
from html.parser import HTMLParser

class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.body_text = []
        self.in_title = False
        self.in_body = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            if attrs_dict.get("name") == "description":
                self.description = attrs_dict.get("content", "")
        if tag == "body":
            self.in_body = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_body:
            self.body_text.append(data.strip())


def classify_topics(text):
    # Keyword-based classification using word boundaries to avoid false matches
    # e.g. "camp" should not match "campaign" or "campus"
    # Replaceable with ML model (e.g. HuggingFace zero-shot) in production
    import re
    topics = {
        "technology": ["ai", "tech", "software", "computer", "data"],
        "shopping": ["shopping", "price", "product", "amazon", "buy"],
        "outdoors": ["hiking", "outdoor", "nature", "trail", "camping"],
        "news": ["breaking news", "report", "cnn", "headlines", "today"]
    }
    text_lower = text.lower()
    found = []
    for topic, keywords in topics.items():
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', text_lower):
                found.append(topic)
                break
    return found if found else ["uncategorized"]


def crawl_url(url):
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode("utf-8", errors="ignore")

        parser = MetadataParser()
        parser.feed(html)

        body = " ".join(parser.body_text)[:300]
        topics = classify_topics(parser.title + " " + parser.description + " " + body)

        return {
            "url": url,
            "title": parser.title.strip(),
            "description": parser.description,
            "body_preview": body,
            "topics": topics,
            "status": "success"
        }
    except Exception as e:
        return {
            "url": url,
            "status": "failed",
            "error": str(e),
            "note": "Site may have anti-bot protection or be temporarily unavailable"
        }


# Test URLs
urls = [
    "https://www.cnn.com",
    "https://www.amazon.com",
    "https://example.com"
]

for url in urls:
    result = crawl_url(url)
    print("\n" + "="*50)
    print(json.dumps(result, indent=2))