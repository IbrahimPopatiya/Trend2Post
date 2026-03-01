from typing import List
from datetime import datetime
from uuid import uuid4

from backend.processing.content_schema import ContentItem


class ContentStore:
    """
    Temporary in-memory store for collected content.
    This will later be replaced by a database.
    """

    def __init__(self):
        self._items: List[ContentItem] = []

    def add_item(
        self,
        title: str,
        content: str,
        source_id: str,
        source_name: str,
        url: str,
        niche: str,
        published_date=None,
        author: str | None = None,
    ) -> ContentItem:
        """
        Validate and store a content item.
        """
        item = ContentItem(
            id=str(uuid4()),
            title=title,
            content=content,
            source_id=source_id,
            source_name=source_name,
            url=url,
            published_date=published_date,
            author=author,
            collected_at=datetime.utcnow(),
            niche=niche,
        )

        self._items.append(item)
        return item

    def list_items(self) -> List[ContentItem]:
        """
        Return all stored content items.
        """
        return self._items

    def count(self) -> int:
        return len(self._items)
    

if __name__ == "__main__":
    store = ContentStore()

    store.add_item(
        title="AI is moving fast",
        content="New advances in generative AI are released daily.",
        source_id="openai_blog",
        source_name="OpenAI Blog",
        url="https://openai.com/blog/example",
        niche="ai",
    )

    store.add_item(
        title="RAG techniques are evolving",
        content="Hybrid search and better chunking improve RAG.",
        source_id="langchain_blog",
        source_name="LangChain Blog",
        url="https://blog.langchain.dev/example",
        niche="ai",
    )

    print(f"Stored items count: {store.count()}\n")

    for item in store.list_items():
        print(item.title, "->", item.source_name)    