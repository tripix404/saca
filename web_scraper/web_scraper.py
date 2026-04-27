#!/usr/bin/env python3
"""
HOWEST Web Scraper - Uitgebreide versie
- Download opties voor HTML, tekst, afbeeldingen en PDF's
- Interactieve keuzemodus bij geen argumenten
- Aparte mappen per bestandstype
- Gebruikersvriendelijke interface
"""

import argparse
import os
import re
import time
import logging
import glob
from urllib.parse import urljoin, urlparse, urldefrag
import requests
from bs4 import BeautifulSoup
import sys

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.INFO
)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; WebScraper/1.0)"}


def get_safe_output_dir(start_url):
    """
    Genereer een veilige naam voor de output directory op basis van de start-URL."""
    parsed = urlparse(start_url)
    domain = parsed.netloc
    path = parsed.path.strip("/").replace("/", "_")
    safe_name = domain
    if path:
        safe_name += f"_{path}"
    return safe_name


def sanitize_filename(url):
    """
    Maak een veilige bestandsnaam op basis van de URL."""
    parsed = urlparse(url)
    safe = parsed.path.strip("/").replace("/", "_").replace("\\", "_")
    if not safe:
        safe = "index"
    if parsed.query:
        safe += "_" + re.sub(r"\W+", "_", parsed.query)
    return safe


def allowed_by_robots(url, robots_txt_cache, base_url):
    """
    Controleer of de URL is toegestaan door de robots.txt van de website."""
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
    return rp.can_fetch(HEADERS["User-Agent"], url)


class WebScraper:
    """
    Een eenvoudige webscraper die pagina's crawlt en bestanden downloadt."""

    def __init__(
        self,
        start_url,
        output_dir=None,
        download_html=False,
        download_text=False,
        download_images=False,
        download_pdfs=False,
        pattern=None,
        max_pages=100,
    ):
        self.start_url = start_url.rstrip("/")
        self.base_domain = urlparse(start_url).netloc
        self.download_html = download_html
        self.download_text = download_text
        self.download_images = download_images
        self.download_pdfs = download_pdfs
        self.pattern = re.compile(pattern, re.IGNORECASE) if pattern else None
        self.max_pages = max_pages

        if not output_dir:
            output_dir = get_safe_output_dir(self.start_url)

        self.output_dir = output_dir
        self.visited = set()
        self.queue = [self.start_url]
        self.queue_set = set(self.queue)
        self.robots_txt_cache = {}

        os.makedirs(self.output_dir, exist_ok=True)
        if self.download_html:
            os.makedirs(os.path.join(self.output_dir, "html"), exist_ok=True)
        if self.download_text:
            os.makedirs(os.path.join(self.output_dir, "text"), exist_ok=True)
        if self.download_images:
            os.makedirs(os.path.join(self.output_dir, "images"), exist_ok=True)
        if self.download_pdfs:
            os.makedirs(os.path.join(self.output_dir, "pdfs"), exist_ok=True)

        logging.info(f"Output directory: {os.path.abspath(self.output_dir)}")

    def download_file(self, url, file_type):
        """
        Download een bestand van de opgegeven URL en sla het op in de juiste map."""
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            response.raise_for_status()

            safe_name = sanitize_filename(url)
            ext = url.split(".")[-1].lower() if "." in url else "bin"

            if file_type == "image":
                path = os.path.join(self.output_dir, "images", f"{safe_name}.{ext}")
            elif file_type == "pdf":
                path = os.path.join(self.output_dir, "pdfs", f"{safe_name}.pdf")
            else:
                return False

            with open(path, "wb") as f:
                f.write(response.content)
            logging.info(f"Saved {file_type.upper()}: {path}")
            return True

        except Exception as e:
            logging.error(f"Fout bij download {file_type}: {e}")
            return False

    def save_page(self, url, html, text):
        """
        Sla de HTML- en tekstinhoud van de pagina op in de juiste map."""
        if self.download_html:
            safe_name = sanitize_filename(url)
            file_html = os.path.join(self.output_dir, "html", f"{safe_name}.html")
            with open(file_html, "w", encoding="utf-8") as f:
                f.write(html)
            logging.info(f"Saved HTML: {file_html}")

        if self.download_text:
            safe_name = sanitize_filename(url)
            file_txt = os.path.join(self.output_dir, "text", f"{safe_name}.txt")
            with open(file_txt, "w", encoding="utf-8") as f:
                f.write(text)
            logging.info(f"Saved TEXT: {file_txt}")

        if self.pattern:
            matches_html = set(self.pattern.findall(html))
            matches_text = set(self.pattern.findall(text))
            matches = matches_html | matches_text
            if matches:
                logging.warning(
                    f"Pattern '{self.pattern.pattern}' found on {url}: {matches}"
                )

    def crawl(self):
        """
        Start de crawl en verwerk de pagina's in de wachtrij."""
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
                """Skip if URL is already visited"""
                resp = requests.get(url, headers=HEADERS, timeout=10)
                resp.raise_for_status()
                content_type = resp.headers.get("Content-Type", "")

                if "pdf" in content_type and self.download_pdfs:
                    self.download_file(url, "pdf")
                    self.visited.add(url)
                    continue

                elif any(
                    img_type in content_type
                    for img_type in ["image/jpeg", "image/png", "image/gif"]
                ):
                    if self.download_images:
                        self.download_file(url, "image")
                    self.visited.add(url)
                    continue

                soup = BeautifulSoup(resp.text, "html.parser")
                text = soup.get_text(separator="\n", strip=True)
                self.save_page(url, resp.text, text)

                for link in soup.find_all(["a", "img"]):
                    if link.name == "a" and self.download_pdfs:
                        href = link.get("href", "")
                        if href.lower().endswith(".pdf"):
                            pdf_url = urljoin(url, href)
                            if pdf_url not in self.visited:
                                self.download_file(pdf_url, "pdf")

                    elif link.name == "img" and self.download_images:
                        img_url = urljoin(url, link.get("src", ""))
                        if img_url not in self.visited:
                            self.download_file(img_url, "image")

                for link in soup.find_all("a", href=True):
                    """Verwerk alleen interne links"""
                    href = urljoin(url, link["href"])
                    href, _ = urldefrag(href)
                    parsed = urlparse(href)
                    if (
                        parsed.netloc == self.base_domain
                        and href not in self.visited
                        and href not in self.queue_set
                    ):
                        self.queue.append(href)
                        self.queue_set.add(href)

                self.visited.add(url)
                count += 1
                print(f"\rProgress: {count}/{self.max_pages} pages", end="", flush=True)
                time.sleep(0.5)

            except Exception as e:
                logging.error(f"Fout bij verwerken {url}: {e}")
                self.visited.add(url)
                continue

        print("\n\nCrawling voltooid!")
        self.report()

    def report(self):
        """
        Genereer een rapport van de gedownloade bestanden."""
        print("\n=== Downloadrapport ===")
        for file_type in ["html", "text", "images", "pdfs"]:
            files = glob.glob(os.path.join(self.output_dir, file_type, "*"))
            print(f"{file_type.upper()}: {len(files)} bestanden")


def interactive_prompt():
    print(
        """
=== HOWEST Web Scraper ===
Kies welke bestanden je wilt downloaden:
1. HTML-pagina's
2. Tekstbestanden
3. Afbeeldingen (JPG/PNG/GIF)
4. PDF-bestanden
5. Alles downloaden
6. Annuleren
"""
    )
    choices = input("Voer nummers in (gescheiden door spaties): ").split()

    options = {
        "download_html": False,
        "download_text": False,
        "download_images": False,
        "download_pdfs": False,
    }

    for choice in choices:
        if choice == "1":
            options["download_html"] = True
        elif choice == "2":
            options["download_text"] = True
        elif choice == "3":
            options["download_images"] = True
        elif choice == "4":
            options["download_pdfs"] = True
        elif choice == "5":
            options = {k: True for k in options}
        elif choice == "6":
            print("Annulering...")
            sys.exit(0)

    if not any(options.values()):
        print("❌ Geen downloadopties geselecteerd!")
        sys.exit(1)

    start_url = input("Start-URL (verplicht): ").strip()
    if not start_url:
        print("❌ Start-URL is verplicht.")
        sys.exit(1)

    output_dir = input("Output directory (optioneel): ").strip()

    # Vraag naar aantal pagina's (nieuw!)
    while True:
        """Vraag naar aantal pagina's om te downloaden"""
        all_pages = (
            input("Wil je alle pagina's downloaden? (y/n) [y]: ").strip().lower()
        )
        if all_pages in ("", "y", "yes"):
            max_pages = 1000000  # Een groot getal, praktisch 'alles'
            break
        elif all_pages in ("n", "no"):
            try:
                max_pages = int(
                    input(
                        "Hoeveel pagina's wil je maximaal downloaden? [100]: "
                    ).strip()
                    or "100"
                )
                break
            except ValueError:
                print("❌ Ongeldig getal, probeer opnieuw.")
        else:
            print("Antwoord met 'y' of 'n'.")

    return {
        "start_url": start_url,
        "output_dir": output_dir,
        **options,
        "max_pages": max_pages,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Geavanceerde HOWEST Web Scraper")
    parser.add_argument("--start-url", help="Start-URL om te crawlen")
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--html", action="store_true", help="Download HTML-pagina's")
    parser.add_argument("--text", action="store_true", help="Download tekstbestanden")
    parser.add_argument("--images", action="store_true", help="Download afbeeldingen")
    parser.add_argument("--pdfs", action="store_true", help="Download PDF-bestanden")
    parser.add_argument(
        "--all", action="store_true", help="Download alle bestandstypen"
    )
    parser.add_argument("--pattern", help="Zoekpatroon in content")
    parser.add_argument(
        "--max-pages", type=int, default=100, help="Maximaal aantal pagina's"
    )

    if len(sys.argv) == 1:
        print("Geen argumenten opgegeven - start interactieve modus")
        args = interactive_prompt()
        scraper = WebScraper(**args)
    else:
        args = parser.parse_args()
        if args.all:
            args.html = args.text = args.images = args.pdfs = True

        scraper = WebScraper(
            start_url=args.start_url,
            output_dir=args.output_dir,
            download_html=args.html,
            download_text=args.text,
            download_images=args.images,
            download_pdfs=args.pdfs,
            pattern=args.pattern,
            max_pages=args.max_pages,
        )

    scraper.crawl()
