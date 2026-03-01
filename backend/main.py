from backend.processing.content_store import ContentStore
from backend.collectors.blog_collector import BlogCollector


if __name__ == "__main__":
    store = ContentStore()
    collector = BlogCollector(store)

    collector.collect_huggingface_blog()

    print("\nFinal stored items:", store.count())