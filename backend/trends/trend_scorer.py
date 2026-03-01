from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict

from backend.processing.content_schema import ContentItem
from backend.trends.keyword_extractor import KeywordExtractor


class TrendScorer:
    """
    Scores trends based on frequency, recency, and source trust.
    """

    def __init__(self, keyword_extractor: KeywordExtractor, recency_days: int = 7):
        self.extractor = keyword_extractor
        self.recency_days = recency_days

    def score(self, items: List[ContentItem]) -> Dict[str, float]:
        """
        Compute trend scores for keywords.
        """
        scores = defaultdict(float)
        now = datetime.utcnow()

        for item in items:
            # Recency weight
            published = item.published_date or item.collected_at
            age_days = (now - published).days
            recency_weight = max(0.1, 1 - (age_days / self.recency_days))

            # Source trust (fallback = 0.8)
            trust = self._source_trust(item.source_id)

            keywords = self.extractor.extract(item.content)

            for kw in keywords:
                scores[kw] += 1 * recency_weight * trust

        return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

    def _source_trust(self, source_id: str) -> float:
        """
        Temporary trust mapping.
        """
        TRUST_MAP = {
            "hf_blog": 0.95,
            "openai_blog": 0.95,
            "langchain_blog": 0.9,
            "llamaindex_blog": 0.9,
        }
        return TRUST_MAP.get(source_id, 0.8)