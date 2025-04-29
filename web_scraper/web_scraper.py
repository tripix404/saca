#!/usr/bin/env python3
"""
Verbeterde Web Scraper: web_scraper.py
--------------------------------------
- Respecteert robots.txt
- Unieke queue (geen dubbele links)
- User-Agent header
- Bestandsnaam-sanitatie
- Optioneel: alleen tekst dumpen
- Progress indicator
- Retry bij netwerkfout
"""

import argparse
import os
import re
import time
import logging
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO
)

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; WebScraper/1.0)'}

def sanitize_filename(url):
    """Zorg voor veilige bestandsnamen."""
    parsed = urlparse(url)
    safe = parsed.path.strip('/').replace('/', '_').replace('\\', '_')
    if not safe:
        safe = 'index'
    # Voeg query toe als die er is, maar veilig
    if parsed.query:
        safe += '_' + re.sub(r'\W+', '_', parsed.query)
    return safe

def allowed_by_robots(url, robots_txt_cache, base_url):
    """Check robots.txt (heel basic)."""
    from urllib.robotparser import RobotFileParser
    parsed = urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    if robots_url not in robots_txt_cache:
        rp = RobotFileParser()
        try:
            rp.set_url(robots_url)
            rp.read()
        except Exception:
            rp = None
        robots_txt_cache[robots_url] = rp
    rp = robots_txt_cache[robots_url]
    if rp is None:
        return True  # Als robots.txt niet bereikbaar is, ga door
    return rp.can_fetch(HEADERS['User-Agent'], url)

class WebScraper:
    def __init__(self, start_url, output_dir, pattern=None, max_pages=100, text_only=False):
        self.start_url = start_url.rstrip('/')
        self.base_domain = urlparse(start_url).netloc
        self.output_dir = output_dir
        self.pattern = re.compile(pattern, re.IGNORECASE) if pattern else None
        self.max_pages = max_pages
        self.text_only = text_only
        self.visited = set()
        self.queue = [self.start_url]
        self.queue_set = set(self.queue)
        self.robots_txt_cache = {}
        os.makedirs(self.output_dir, exist_ok=True)

    def save_page(self, url, html, text):
        safe_name = sanitize_filename(url)
        file_html = os.path.join(self.output_dir, f"{safe_name}.html")
        with open(file_html, 'w', encoding='utf-8') as f:
            f.write(html)
        logging.info(f"Saved HTML: {file_html}")

        if self.text_only:
            file_txt = os.path.join(self.output_dir, f"{safe_name}.txt")
            with open(file_txt, 'w', encoding='utf-8') as f:
                f.write(text)
            logging.info(f"Saved TEXT: {file_txt}")

        if self.pattern:
            # Zoek in zowel HTML als tekst
            matches_html = set(self.pattern.findall(html))
            matches_text = set(self.pattern.findall(text))
            matches = matches_html | matches_text
            if matches:
                logging.warning(f"Pattern '{self.pattern.pattern}' found on {url}: {matches}")

    def crawl(self):
        count = 0
        while self.queue and count < self.max_pages:
            url = self.queue.pop(0)
            self.queue_set.discard(url)
            if url in self.visited:
                continue
            # Respect robots.txt
            if not allowed_by_robots(url, self.robots_txt_cache, self.start_url):
                logging.info(f"Disallowed by robots.txt: {url}")
                self.visited.add(url)
                continue

            logging.info(f"Crawling ({count+1}/{self.max_pages}): {url}")
            try:
                for attempt in range(3):
                    try:
                        resp = requests.get(url, headers=HEADERS, timeout=10)
                        resp.raise_for_status()
                        break
                    except Exception as e:
                        if attempt == 2:
                            raise
                        logging.warning(f"Retry {attempt+1} for {url} due to {e}")
                        time.sleep(2)
            except Exception as e:
                logging.error(f"Failed to fetch {url}: {e}")
                self.visited.add(url)
                continue

            soup = BeautifulSoup(resp.text, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
            self.save_page(url, resp.text, text)
            self.visited.add(url)
            count += 1

            # Progress indicator
            print(f"\rProgress: {count}/{self.max_pages} pages", end='', flush=True)

            # Links verzamelen
            for link in soup.find_all('a', href=True):
                href = urljoin(url, link['href'])
                href, _ = urldefrag(href)  # Verwijder fragment
                parsed = urlparse(href)
                if parsed.netloc == self.base_domain and href not in self.visited and href not in self.queue_set:
                    self.queue.append(href)
                    self.queue_set.add(href)
            time.sleep(1)  # be gentle
        print()
        logging.info("Crawling complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Recursive Web Scraper with pattern logging")
    parser.add_argument('--start-url', required=True, help='URL to begin crawling')
    parser.add_argument('--output-dir', default='./dump', help='Directory to save downloaded pages')
    parser.add_argument('--pattern', help='Regex pattern to search for in pages')
    parser.add_argument('--max-pages', type=int, default=100, help='Maximum number of pages to crawl')
    parser.add_argument('--text-only', action='store_true', help='Save only visible text (as .txt)')
    args = parser.parse_args()

    scraper = WebScraper(
        start_url=args.start_url,
        output_dir=args.output_dir,
        pattern=args.pattern,
        max_pages=args.max_pages,
        text_only=args.text_only
    )
    scraper.crawl()
