from typing import Dict, List


class TrendExplainer:
    """
    Generates human-readable explanations for trends.
    """

    def explain(self, topic: Dict) -> str:
        """
        Generate explanation text for a topic.
        """
        topic_name = topic["topic"].replace("_", " ").title()
        keywords = topic["keywords"]
        score = topic["score"]

        keyword_phrase = ", ".join(keywords[:5])

        explanation = (
            f"{topic_name} is trending in AI right now because it appears "
            f"frequently across recent articles from trusted sources. "
            f"The discussion focuses on key concepts such as {keyword_phrase}. "
            f"This indicates growing interest and active development in this area."
        )

        return explanation