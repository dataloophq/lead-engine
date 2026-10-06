import feedparser
import os
from datetime import datetime
from supabase import create_client, Client

TARGET_FEEDS = [
    "https://feeds.feedburner.com/TechCrunch/fundings-exits"
]

KEYWORDS = ["funding", "raised", "series", "acquisition", "expansion", "million"]

def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Credenziali Supabase mancanti. Verifica i Secret su GitHub.")
    return create_client(url, key)

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
    print("Avvio estrazione dati...")
    new_leads = extract_high_intent_leads()
    
    if new_leads:
        print(f"Trovati {len(new_leads)} lead. Connessione al database in corso...")
        supabase = get_supabase_client()
        supabase.table("high_intent_leads").insert(new_leads).execute()
        print("Dati salvati con successo nel database cloud!")
    else:
        print("Nessun nuovo lead trovato in questa esecuzione.")
