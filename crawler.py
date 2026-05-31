import json
import urllib.request
from html.parser import HTMLParser


class MetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.body_text = []
        self.headings = []
        self.schema_types = []
        self.og_tags = {}
        self.meta_keywords = ""
        self.in_title = False
        self.in_body = False
        self.in_heading = False
        self.current_heading = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description":
                self.description = content
            if name == "keywords":
                self.meta_keywords = content
            if prop.startswith("og:"):
                self.og_tags[prop] = content
        if tag in ("h1", "h2", "h3"):
            self.in_heading = True
            self.current_heading = ""
        if tag == "body":
            self.in_body = True
        if attrs_dict.get("itemtype", ""):
            schema = attrs_dict["itemtype"].split("/")[-1]
            if schema:
                self.schema_types.append(schema)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag in ("h1", "h2", "h3"):
            if self.current_heading.strip():
                self.headings.append(self.current_heading.strip())
            self.in_heading = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_heading:
            self.current_heading += data
        if self.in_body:
            self.body_text.append(data.strip())


def extract_topics(parser):
    """Extract topics from real SEO signals:
    meta keywords, og:type, og:section, H1/H2 headings, schema.org"""
    topics = set()

    # 1. Meta keywords tag
    if parser.meta_keywords:
        for kw in parser.meta_keywords.split(","):
            kw = kw.strip().lower()
            if kw and len(kw) > 2:
                topics.add(kw)

    # 2. og:type (article, product, website etc.)
    if parser.og_tags.get("og:type"):
        topics.add(parser.og_tags["og:type"].lower())

    # 3. og:section (Technology, Sports, Health etc.)
    if parser.og_tags.get("og:section"):
        topics.add(parser.og_tags["og:section"].lower())

    # 4. H1/H2/H3 headings (first 5)
    for heading in parser.headings[:5]:
        words = heading.lower().split()[:4]
        if words:
            topics.add(" ".join(words))

    # 5. schema.org types
    for schema_type in parser.schema_types[:3]:
        topics.add(schema_type.lower())

    return sorted(list(topics)) if topics else ["uncategorized"]


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
        topics = extract_topics(parser)

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