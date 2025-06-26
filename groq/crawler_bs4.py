from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def crawl_website(start_url, max_pages=10):
    visited = set()
    to_visit = [start_url]
    documents = []

    base_domain = urlparse(start_url).netloc

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue

        print(f"Fetching: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        visited.add(url)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)

        # Collect the page content as a document (we can create a LangChain Document here or keep as dict)
        documents.append({"page_content": text, "metadata": {"source": url}})

        # Find all internal links
        for link_tag in soup.find_all("a", href=True):
            link = urljoin(url, link_tag["href"])
            link_parsed = urlparse(link)
            # Keep only links on the same domain and http(s)
            if (
                link_parsed.scheme in ("http", "https")
                and link_parsed.netloc == base_domain
            ):
                if link not in visited and link not in to_visit:
                    to_visit.append(link)

    return documents


docs = crawl_website("https://aman.ai/primers/ai/RAG/", max_pages=20)
print(f"Collected {len(docs)} pages.")
