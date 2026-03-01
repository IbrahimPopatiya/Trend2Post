from datetime import datetime
from typing import Optional
from pydantic import BaseModel, HttpUrl


class ContentItem(BaseModel):
    id: str
    title: str
    content: str

    source_id: str
    source_name: str
    url: HttpUrl

    published_date: Optional[datetime]
    author: Optional[str] = None
    collected_at: datetime

    niche: str


if __name__ == "__main__":
    sample = ContentItem(
        id="test_001",
        title="Test AI Content",
        content="This is a test content about AI trends.",
        source_id="hf_blog",
        source_name="Hugging Face Blog",
        url="https://huggingface.co/blog/test",
        published_date=None,
        collected_at=datetime.utcnow(),
        niche="ai"
    )

    print(sample)    