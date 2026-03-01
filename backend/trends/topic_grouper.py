from collections import defaultdict
from typing import Dict, List, Tuple


class TopicGrouper:
    """
    Groups related keywords into higher-level topics.
    """

    def __init__(self):
        # Simple concept seeds (MVP – editable later)
        self.seed_topics = {
            "retrieval": ["retrieval", "pipeline", "rag", "index", "search"],
            "models": ["model", "models", "training", "parameter"],
            "agents": ["agent", "agents", "expert", "planner"],
            "vision": ["image", "visual", "aesthetic", "vision"],
            "autonomous_driving": ["carla", "driving", "vehicle", "rl"],
            "text_generation": ["text", "generation", "language", "llm"],
        }

    def group(self, keyword_scores: Dict[str, float]) -> List[Dict]:
        """
        Group keywords into topics and compute topic scores.
        """
        topic_buckets = defaultdict(list)
        used_keywords = set()

        # Assign keywords to seed topics
        for topic, seeds in self.seed_topics.items():
            for kw, score in keyword_scores.items():
                if kw in seeds:
                    topic_buckets[topic].append((kw, score))
                    used_keywords.add(kw)

        # Handle unassigned keywords
        for kw, score in keyword_scores.items():
            if kw not in used_keywords:
                topic_buckets["misc"].append((kw, score))

        # Build final topic objects
        topics = []
        for topic, items in topic_buckets.items():
            if not items:
                continue

            topic_score = sum(score for _, score in items)
            if topic != "misc":
                topics.append({
                    "topic": topic,
                    "score": round(topic_score, 2),
                    "keywords": [kw for kw, _ in items]
                })

        # Sort by score
        topics.sort(key=lambda x: x["score"], reverse=True)
        return topics