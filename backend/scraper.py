import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class Article:
    def __init__(self, title: str, url: str, date: str, content: str, source: str):
        self.title = title
        self.url = url
        self.date = date  # ISO format YYYY-MM-DD
        self.content = content
        self.source = source
        self.summary: Optional[str] = None
        self.is_relevant: bool = False

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "date": self.date,
            "content": self.content,
            "source": self.source,
            "summary": self.summary,
            "is_relevant": self.is_relevant
        }

class BaseScraper(ABC):
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url

    @abstractmethod
    def scrape(self) -> List[Article]:
        pass

    def is_recent(self, date_str: str, days: int = 1) -> bool:
        try:
            # Handle various date formats if necessary
            # For now assuming ISO or simple formats, can be expanded
            article_date = datetime.fromisoformat(date_str)
            cutoff = datetime.now() - timedelta(days=days)
            return article_date > cutoff
        except ValueError:
            return True # If date parsing fails, keep it to be safe, filter later or improve parsing

class RSSScraper(BaseScraper):
    def scrape(self) -> List[Article]:
        print(f"Scraping RSS: {self.name} - {self.url}")
        feed = feedparser.parse(self.url)
        articles = []
        for entry in feed.entries:
            # Extract date
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                 published = datetime(*entry.published_parsed[:6]).isoformat()
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                 published = datetime(*entry.updated_parsed[:6]).isoformat()
            else:
                 published = datetime.now().isoformat() # Fallback

            # Content
            content = ""
            if hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'content'):
                content = entry.content[0].value
            
            # Simple HTML strip for content
            soup = BeautifulSoup(content, 'html.parser')
            text_content = soup.get_text()[:1000] # Limit content length for API

            articles.append(Article(
                title=entry.title,
                url=entry.link,
                date=published,
                content=text_content,
                source=self.name
            ))
        return articles

class SimpleHTMLScraper(BaseScraper):
    # Specialized scraper for sites without RSS if needed, 
    # for now we will stick to RSS where possible or add specific HTML parsers here
    def scrape(self) -> List[Article]:
        # Implementation depends on specific site structure
        return []

# List of target feeds
MEDIA_SOURCES = [
    # Example feeds - These would need to be verified real RSS feeds
    {"name": "Google Ads Blog", "url": "https://blog.google/products/ads-commerce/rss/", "type": "rss"},
    {"name": "Yahoo! JAPAN Ads", "url": "https://www.lycbiz.com/jp/news/yahoo-ads/rss.xml", "type": "rss"}, # Hypothetical/Example URL
    # Add more real feeds here
]

def get_scrapers():
    scrapers = []
    for source in MEDIA_SOURCES:
        if source["type"] == "rss":
            scrapers.append(RSSScraper(source["name"], source["url"]))
    return scrapers
