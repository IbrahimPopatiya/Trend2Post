from backend.processing.content_store import ContentStore
from backend.collectors.blog_collector import BlogCollector
from backend.trends.keyword_extractor import KeywordExtractor
from backend.trends.trend_scorer import TrendScorer
from backend.trends.topic_grouper import TopicGrouper
from backend.trends.trend_explainer import TrendExplainer


if __name__ == "__main__":
    store = ContentStore()
    collector = BlogCollector(store)

    collector.collect_huggingface_blog()

    extractor = KeywordExtractor()
    scorer = TrendScorer(extractor)
    grouper = TopicGrouper()
    explainer = TrendExplainer()

    keyword_scores = scorer.score(store.list_items())
    keyword_scores = dict(list(keyword_scores.items())[:50])

    topics = grouper.group(keyword_scores)

    print("\nAI Trends with explanations:\n")

    for topic in topics[:5]:
        print(f"Topic: {topic['topic']}")
        print(f"Score: {topic['score']}")
        print("Explanation:")
        print(explainer.explain(topic))
        print("-" * 50)