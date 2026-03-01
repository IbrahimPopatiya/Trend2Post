import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List
import re
from typing import List
from backend.processing.content_store import ContentStore
from backend.processing.content_cleaner import ContentCleaner
from dateutil import parser as date_parser

class ContentCleaner:
    """
    Cleans and normalizes raw scraped content.
    """

    def __init__(self, min_line_length: int = 40):
        self.min_line_length = min_line_length

    def clean(self, raw_text: str) -> str:
        """
        Clean raw scraped text into high-quality content.
        """
        if not raw_text:
            return ""

        # Split into lines
        lines = raw_text.split("\n")

        cleaned_lines: List[str] = []

        for line in lines:
            line = line.strip()

            # Skip empty or very short lines
            if len(line) < self.min_line_length:
                continue

            # Skip common noise patterns
            if self._is_noise(line):
                continue

            cleaned_lines.append(line)

        return "\n".join(cleaned_lines)

    def _is_noise(self, line: str) -> bool:
        """
        Detect noisy lines like navigation, cookies, social links.
        """
        noise_patterns = [
            r"cookie",
            r"privacy policy",
            r"terms of service",
            r"subscribe",
            r"sign up",
            r"twitter",
            r"linkedin",
            r"github",
            r"©",
        ]

        line_lower = line.lower()
        return any(re.search(pattern, line_lower) for pattern in noise_patterns)


class BlogCollector:
    """
    Generic blog collector (HTML-based).
    """

    def __init__(self, store: ContentStore):
        self.store = store
        self.cleaner = ContentCleaner() 

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

            published_date = None

            time_tag = article_soup.find("time")
            if time_tag and time_tag.get("datetime"):
                try:
                    published_date = date_parser.parse(time_tag.get("datetime"))
                except Exception:
                    published_date = None

            # Author (best effort)
            author = None
            author_tag = article_soup.find("a", href=lambda x: x and x.startswith("/profile/"))
            if author_tag:
                author = author_tag.get_text(strip=True)

            # Hugging Face blog content lives mostly inside <p>
            paragraphs = article_soup.find_all("p")
            # content = "\n".join(
                # p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 40
            # )

            
            raw_content = "\n".join(p.get_text(strip=True) for p in paragraphs)
            content = self.cleaner.clean(raw_content)

            if not content:
                continue

            self.store.add_item(
                title=title,
                content=content,
                source_id="hf_blog",
                source_name="Hugging Face Blog",
                url=link,
                niche="ai",
                published_date=published_date,
                author=author,
            )

            print(f"Collected: {title}")