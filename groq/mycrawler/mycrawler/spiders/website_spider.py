import logging
from urllib.parse import urlparse

import scrapy


class WebsiteSpider(scrapy.Spider):
    name = "website_spider"

    custom_settings = {
        "DEPTH_LIMIT": 3,  # Limit crawl depth
        "LOG_LEVEL": "DEBUG",  # Detailed debug logs
        "LOG_FORMAT": "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        "LOG_DATEFORMAT": "%Y-%m-%d %H:%M:%S",
    }

    def __init__(self, start_url=None, max_pages=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not start_url:
            raise ValueError("You must provide a start_url")
        self.start_urls = [start_url]
        domain = urlparse(start_url).netloc
        self.allowed_domains = [domain]
        self.max_pages = int(max_pages)
        self.visited_pages = 0

    def parse(self, response):
        if self.visited_pages >= self.max_pages:
            self.logger.debug(f"Reached max pages limit: {self.max_pages}")
            return

        self.visited_pages += 1
        self.logger.debug(f"Processing page {self.visited_pages}: {response.url}")

        # Extract text content
        page_text = "\n".join(response.xpath("//body//text()").getall()).strip()

        yield {
            "page_content": page_text,
            "source": response.url,
        }

        # Follow internal links only
        for href in response.css("a::attr(href)").getall():
            absolute_url = response.urljoin(href)
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc == self.allowed_domains[0]:
                self.logger.debug(f"Following link: {absolute_url}")
                yield scrapy.Request(absolute_url, callback=self.parse)


### command to run the spider
# scrapy crawl website_spider -a start_url=https://aman.ai/primers/ai/RAG/ -a max_pages=20 -o output.json
# Note: Adjust the start_url and max_pages as needed.
