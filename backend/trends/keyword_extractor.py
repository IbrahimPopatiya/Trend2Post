import re
from collections import Counter
from typing import List

STOPWORDS = {
    "the", "and", "that", "this", "with", "from", "have", "they",
    "when", "what", "more", "each", "same", "their", "there",
    "will", "would", "could", "should", "about", "into", "over",
    "also", "than", "then", "them", "these", "those", "your",
    "been", "being", "because", "while", "where", "which",
    "such", "using", "used", "use"
}

DOMAIN_STOPWORDS = {
    "only", "might", "first", "single", "like", "real",
    "level", "three", "many", "different", "example",
    "paper", "result", "results", "based", "approach"
}

class KeywordExtractor:
    """
    Extracts keywords from cleaned content for trend detection.
    """

    def __init__(self, min_word_length: int = 4):
        self.min_word_length = min_word_length

    def normalize(self, word: str) -> str:
        """
        Normalize word forms (simple plural handling).
        """
        if word.endswith("s") and len(word) > 4:
            return word[:-1]
        return word    

    def extract(self, text: str) -> List[str]:
        """
        Extract normalized keywords from text.
        """
        if not text:
            return []

        # Lowercase
        text = text.lower()

        # Remove punctuation
        text = re.sub(r"[^a-z0-9\s]", " ", text)

        words = text.split()

        keywords = []

        for word in words:
            if (
                len(word) >= self.min_word_length
                and not word.isdigit()
                and word not in STOPWORDS
                and word not in DOMAIN_STOPWORDS
            ):
                keywords.append(self.normalize(word))

        return keywords

    def top_keywords(self, texts: List[str], top_k: int = 10):
        """
        Get top keywords across multiple documents.
        """
        counter = Counter()

        for text in texts:
            counter.update(self.extract(text))

        return counter.most_common(top_k)