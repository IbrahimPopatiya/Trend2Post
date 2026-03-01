import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List

from backend.processing.content_store import ContentStore


class BlogCollector:
    """
    Generic blog collector (HTML-based).
    """

    def __init__(self, store: ContentStore):
        self.store = store

    def fetch_page(self, url: str) -> BeautifulSoup:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def collect_huggingface_blog(self):
        """
        Collect recent posts from Hugging Face blog.
        """
        base_url = "https://huggingface.co"
        url = f"{base_url}/blog"

        soup = self.fetch_page(url)
        articles = soup.find_all("article")

        print(f"Found {len(articles)} articles on Hugging Face blog")

        for article in articles[:5]:  # limit for MVP
            link_tag = article.find("a")
            title_tag = article.find("h4")

            if not link_tag or not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = base_url + link_tag.get("href")

            # Fetch full article page
            article_soup = self.fetch_page(link)

            # Hugging Face blog content lives mostly inside <p>
            paragraphs = article_soup.find_all("p")
            content = "\n".join(
                p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 40
            )

            if not content:
                continue

            self.store.add_item(
                title=title,
                content=content,
                source_id="hf_blog",
                source_name="Hugging Face Blog",
                url=link,
                niche="ai",
                published_date=None,
            )

            print(f"Collected: {title}")