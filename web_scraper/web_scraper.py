#!/usr/bin/env python3
"""
HOWEST Web Scraper
- Maakt automatisch een map aan met domeinnaam + pad als output directory
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
import glob  # <-- Toegevoegd voor bestandsmatching
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup
import sys

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s: %(message)s',
    level=logging.INFO
)

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; WebScraper/1.0)'}

def get_safe_output_dir(start_url):
    """Genereer veilige mapnaam gebaseerd op domein en pad"""
    parsed = urlparse(start_url)
    domain = parsed.netloc
    path = parsed.path.strip('/').replace('/', '_')
    safe_name = domain
    if path:
        safe_name += f"_{path}"
    return safe_name

def sanitize_filename(url):
    parsed = urlparse(url)
    safe = parsed.path.strip('/').replace('/', '_').replace('\\', '_')
    if not safe:
        safe = 'index'
    if parsed.query:
        safe += '_' + re.sub(r'\W+', '_', parsed.query)
    return safe

def allowed_by_robots(url, robots_txt_cache, base_url):
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
        return True
    return rp.can_fetch(HEADERS['User-Agent'], url)

class WebScraper:
    def __init__(self, start_url, output_dir=None, pattern=None, max_pages=100, text_only=False):
        self.start_url = start_url.rstrip('/')
        self.base_domain = urlparse(start_url).netloc
        
        # Genereer automatische mapnaam indien niet opgegeven
        if not output_dir:
            output_dir = get_safe_output_dir(self.start_url)
        
        self.output_dir = output_dir
        self.pattern = re.compile(pattern, re.IGNORECASE) if pattern else None
        self.max_pages = max_pages
        self.text_only = text_only
        self.visited = set()
        self.queue = [self.start_url]
        self.queue_set = set(self.queue)
        self.robots_txt_cache = {}
        os.makedirs(self.output_dir, exist_ok=True)
        logging.info(f"Output directory: {os.path.abspath(self.output_dir)}")

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

            print(f"\rProgress: {count}/{self.max_pages} pages", end='', flush=True)

            for link in soup.find_all('a', href=True):
                href = urljoin(url, link['href'])
                href, _ = urldefrag(href)
                parsed = urlparse(href)
                if parsed.netloc == self.base_domain and href not in self.visited and href not in self.queue_set:
                    self.queue.append(href)
                    self.queue_set.add(href)
            time.sleep(0.1)
        print()
        logging.info("Crawling complete.")

        # Toegevoegd: lijst alle tekstbestanden, pdf bestanden en jpg bestanden in de output directory
        txt_files = glob.glob(os.path.join(self.output_dir, "*.txt"))
        print(f"\nAangemaakte tekstbestanden ({len(txt_files)}):")
        for txt_file in txt_files:
            print(f"- {os.path.basename(txt_file)}")
        
        pdf_files = glob.glob(os.path.join(self.output_dir, "*.pdf"))
        print(f"\nAangemaakte pdfbestanden ({len(pdf_files)}):")
        for pdf_file in pdf_files:
            print(f"- {os.path.basename(pdf_file)}")
        
        jpg_files = glob.glob(os.path.join(self.output_dir, "*.jpg"))
        print(f"\nAangemaakte fotobestanden ({len(jpg_files)}):")
        for jpg_file in jpg_files:
            print(f"- {os.path.basename(jpg_file)}")

EXAMPLES = """
Voorbeelden van gebruik:

  Basis scraping (automatische mapnaam):
    python web_scraper.py --start-url https://example.com/blog

  Handmatige mapnaam:
    python web_scraper.py --start-url https://example.com --output-dir mijn_custom_map
"""

def interactive_argument_prompt():
    print("\nGeen argumenten opgegeven. Vul de volgende gegevens in om verder te gaan:")
    start_url = input("Start-URL (verplicht): ").strip()
    if not start_url:
        print("❌ Start-URL is verplicht.")
        sys.exit(1)
    
    auto_dir = get_safe_output_dir(start_url)
    output_dir = input(f"Output directory [{auto_dir}]: ").strip() or auto_dir
    
    pattern = input("Regex pattern (optioneel): ").strip() or None
    try:
        max_pages = int(input("Maximaal aantal pagina's [100]: ").strip() or "100")
    except ValueError:
        max_pages = 100
    text_only = input("Alleen tekst opslaan? (y/n) [n]: ").strip().lower() == "y"
    return argparse.Namespace(
        start_url=start_url,
        output_dir=output_dir,
        pattern=pattern,
        max_pages=max_pages,
        text_only=text_only
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="🔍 HOWEST Web Scraper - Gestructureerde website data extractie",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EXAMPLES
    )

    required = parser.add_argument_group('Verplichte argumenten')
    required.add_argument(
        '--start-url',
        required=True,
        help="Start-URL om te crawlen (bijv. 'https://voorbeeld.nl/pagina')"
    )

    optional = parser.add_argument_group('Optionele argumenten')
    optional.add_argument(
        '--output-dir',
        help="Handmatige mapnaam (default: domein + pad)")
    optional.add_argument(
        '--pattern',
        help="Regex patroon om te zoeken (bijv. 'admin|password')"
    )
    optional.add_argument(
        '--max-pages',
        type=int,
        default=100,
        help="Maximaal aantal te crawlen pagina's (default: 100)"
    )
    optional.add_argument(
        '--text-only',
        action='store_true',
        help="Sla alleen tekst op (geen HTML)"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        args = interactive_argument_prompt()
    else:
        args = parser.parse_args()

    scraper = WebScraper(
        start_url=args.start_url,
        output_dir=args.output_dir,
        pattern=args.pattern,
        max_pages=args.max_pages,
        text_only=args.text_only
    )
    scraper.crawl()
