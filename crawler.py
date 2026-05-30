import requests
from bs4 import BeautifulSoup

def classify_topics(text):
    topics = {
        "technology": ["ai", "tech", "software", "computer", "data"],
        "shopping": ["buy", "price", "product", "toaster", "amazon"],
        "outdoors": ["camp", "hiking", "outdoor", "nature", "trail"],
        "news": ["breaking", "report", "cnn", "news", "today"]
    }
    
    text_lower = text.lower()
    found_topics = []
    
    for topic, keywords in topics.items():
        if any(word in text_lower for word in keywords):
            found_topics.append(topic)
    
    return found_topics if found_topics else ["uncategorized"]


def crawl_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No title found"
        
        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")

        body = soup.get_text(separator=" ", strip=True)[:100]
        topics = classify_topics(title + " " + description + " " + body)

        return {
            "url": url,
            "title": title,
            "description": description,
            "body_preview": body,
            "topics": topics
        }

    except Exception as e:
        return {"url": url, "error": str(e)}


# Test URLs
urls = [
    "https://www.cnn.com/2025/09/23/tech/google-study-90-percent-tech-jobs-ai",
    "https://httpbin.org/html",
    "https://example.com"
]

for url in urls:
    result = crawl_url(url)
    print("\n" + "="*50)
    for key, value in result.items():
        print(f"{key}: {value}")