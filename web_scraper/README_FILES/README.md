
## 1. Web Scraper (`web_scraper.py`)

### Doel

- Recursief een website crawlen en alle gevonden pagina’s lokaal opslaan.
- Specifieke patronen (bijv. ‘password’, ‘token’) herkennen en loggen voor forensisch onderzoek of misleiding van aanvallers.

### Gebruikte elementen en keuzes

| Element         | Reden                                            | Alternatief           |
| --------------- | ------------------------------------------------ | --------------------- |
| `requests`      | Eenvoudig HTTP-verzoeken, brede ondersteuning    | `httpx`, `urllib`     |
| `BeautifulSoup` | Gebruiksvriendelijke HTML-parser                 | `lxml`, `pyquery`     |
| `argparse`      | Standaard CLI-parser, geen extra afhankelijkheid | `click`, `typer`      |
| `logging`       | Flexibele logniveaus en formaten                 | `print`               |
| `re` (regex)    | Krachtige patroonherkenning                      | handmatige parsing    |
| `time.sleep(1)` | Eenvoudige rate limiting om servers te ontzien   | asynchrone throttling |

### CLI-opties

```bash
# Begin met scannen van https://example.com, sla op in ./dump, zoek naar ‘password’ of ‘token’, max 50 pagina’s
python3 web_scraper.py \
  --start-url https://example.com \
  --output-dir ./dump \
  --pattern "password|token" \
  --max-pages 50
```
---------------------------------------------------------------------------------------------------------------------
Basis‑crawl (maximaal 10 pagina’s)
Crawlt https://example.com, slaat alle HTML op in ./data/basic_scrape en stopt na 10 pagina’s.
```
python web_scraper.py \
  --url https://example.com \
  --output ./data/basic_scrape \
  --max_pages 10

```
---------------------------------------------------------------------------------------------------------------------
Forensisch onderzoek met regex‑logging
Crawlt https://testsite.local, zoekt op de woorden “password” of “login” (case‑insensitive) en logt alle matches.
```
python web_scraper.py \
  --url https://testsite.local \
  --output ./data/forensic_scrape \
  --regex "(?i)password|login" \
  --max_pages 50

```
---------------------------------------------------------------------------------------------------------------------
Langdurige crawl met vertraging en custom User‑Agent
Ideaal wanneer je de server niet wilt overbelasten en je jezelf wilt voor­doen als “ScrapeBot/1.0”.
```
python web_scraper.py \
  --url https://news.example.org \
  --output ./data/news_scrape \
  --max_pages 100 \
  --delay 1.0 \
  --user_agent "Mozilla/5.0 (compatible; ScrapeBot/1.0; +https://jouwnode.com/bot)"

```
---------------------------------------------------------------------------------------------------------------------
Korte blog‑crawl met short flags
Zelfde als (1), maar met de korte vlaggen (-u, -o, -m):
```
python web_scraper.py -u https://blog.example.com \
                      -o ./data/blog_scrape \
                      -m 20

```
---------------------------------------------------------------------------------------------------------------------

Help‑scherm oproepen
Overzicht van alle opties en korte uitleg:
```
python web_scraper.py --help

```



---
