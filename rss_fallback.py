import feedparser

def extract_articles_from_rss(rss_url: str, limit: int = 5) -> list:
    print(f"🌐 Trying RSS feed: {rss_url}")
    feed = feedparser.parse(rss_url)
    article_links = []

    for entry in feed.entries[:limit]:
        article_links.append(entry.link)

    return article_links