import feedparser
import json
from datetime import datetime

TARGET_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch/fundings-exits"
]

KEYWORDS = ["funding", "raised", "series", "acquisition", "expansion", "million"]

def extract_high_intent_leads():
    leads = []
    for feed_url in TARGET_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title_lower = entry.title.lower()
            if any(keyword in title_lower for keyword in KEYWORDS):
                leads.append({
                    "company_signal": entry.title,
                    "source_link": entry.link,
                    "published_at": entry.published,
                    "scraped_at": datetime.now().isoformat(),
                    "status": "raw"
                })
    return leads

if __name__ == "__main__":
    new_leads = extract_high_intent_leads()
    with open("new_leads.json", "w") as f:
        json.dump(new_leads, f, indent=4)
    print(f"Estrazione completata. {len(new_leads)} lead trovati.")
