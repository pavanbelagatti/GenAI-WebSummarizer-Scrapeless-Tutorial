from scrapeless_client import extract_page_text
from summarizer_agent import summarize_html
from link_extractor import extract_article_links
from db_client import save_summary
from rss_fallback import extract_articles_from_rss

from bs4 import BeautifulSoup

# Optional: known RSS feeds for fallback
RSS_FEEDS = {
    "techcrunch.com": "https://techcrunch.com/feed/",
    "theverge.com": "https://www.theverge.com/rss/index.xml"
}

def get_fallback_rss_url(homepage_url: str) -> str:
    for domain, feed_url in RSS_FEEDS.items():
        if domain in homepage_url:
            return feed_url
    return None

def main():
    homepage_url = input("Enter a news site homepage URL: ").strip()

    print(f"\n🔍 Fetching homepage content from: {homepage_url}")
    try:
        homepage_html = extract_page_text(homepage_url)

        # Save for debug
        with open("homepage_dump.html", "w", encoding="utf-8") as f:
            f.write(homepage_html)
        print("🧪 Dumped homepage HTML to homepage_dump.html")

    except Exception as e:
        print(f"❌ Error fetching homepage: {e}")
        return

    print("🔗 Extracting article links...")
    article_urls = extract_article_links(homepage_url, homepage_html, limit=5)

    if not article_urls:
        print("⚠️ No links found via homepage. Falling back to RSS...")
        rss_url = get_fallback_rss_url(homepage_url)
        if rss_url:
            article_urls = extract_articles_from_rss(rss_url, limit=5)
        else:
            print("❌ No RSS feed known for this domain.")
            return

    for idx, url in enumerate(article_urls, start=1):
        print(f"\n📄 [{idx}] Processing article: {url}")
        try:
            article_html = extract_page_text(url)
            summary = summarize_html(article_html)

            soup = BeautifulSoup(article_html, "html.parser")
            title = soup.title.string.strip() if soup.title and soup.title.string else "No Title Found"

            print("📝 Summary:\n")
            print(summary)

            save_summary(url, title, summary)
            print("💾 Saved to SingleStore!")

        except Exception as e:
            print(f"❌ Failed to process {url}: {e}")

if __name__ == "__main__":
    main()