import os
import json
from datetime import datetime
from dotenv import load_dotenv
from scraper import get_scrapers
from gemini_client import GeminiProcessor

# Load environment variables
load_dotenv()

DATA_FILE = os.path.join(os.path.dirname(__file__), '../data/updates.json')

def load_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    # Ensure directory exists
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    print("Starting Daily Ad Update Collector...")
    
    # 1. Load existing
    existing_data = load_existing_data()
    existing_urls = set(item['url'] for item in existing_data)
    
    # 2. Scrape
    scrapers = get_scrapers()
    new_articles = []
    
    for scraper in scrapers:
        try:
            articles = scraper.scrape()
            for article in articles:
                # Filter by 24h freshness (optional, but good for daily runs)
                # For now, we rely on the implementation in scraper or here
                # Let's filter by URL uniqueness first
                if article.url not in existing_urls:
                    # Check if recent (e.g. within last 2 days to catch up)
                    if scraper.is_recent(article.date, days=2):
                        new_articles.append(article)
        except Exception as e:
            print(f"Error scraping {scraper.name}: {e}")

    print(f"Found {len(new_articles)} potential new articles.")
    
    # 3. Process with Gemini
    gemini = GeminiProcessor()
    
    processed_count = 0
    final_updates = []
    
    for article in new_articles:
        print(f"Processing: {article.title}")
        result = gemini.process_article(article.title, article.content)
        
        if result:
            article.summary = result['summary']
            article.is_relevant = True
            
            # Format for frontend
            update_entry = {
                "id": len(existing_data) + len(final_updates) + 1,
                "source": article.source,
                "date": article.date,
                "title": article.title,
                "summary": article.summary,
                "url": article.url,
                "timestamp": datetime.now().isoformat()
            }
            final_updates.append(update_entry)
            processed_count += 1
        else:
            print(" -> Skipped (Not relevant or not an update)")
            
    # 4. Save
    if final_updates:
        # Prepend new updates
        all_data = final_updates + existing_data
        save_data(all_data)
        print(f"Saved {len(final_updates)} new updates.")
    else:
        print("No new relevant updates found.")

if __name__ == "__main__":
    main()
