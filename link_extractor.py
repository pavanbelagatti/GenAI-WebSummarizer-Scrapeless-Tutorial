from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def extract_article_links(base_url: str, html: str, limit: int = 5) -> list:
    soup = BeautifulSoup(html, "html.parser")
    links = set()

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if not href or href.startswith("#") or "javascript:" in href:
            continue

        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if parsed.netloc != urlparse(base_url).netloc:
            continue

        if any(x in full_url for x in ["/tag", "/video", "/events", "/newsletter", "/about", "/privacy"]):
            continue

        if "-" in parsed.path and len(parsed.path.split("/")) > 2:
            links.add(full_url)

        if len(links) >= limit:
            break

    return list(links)