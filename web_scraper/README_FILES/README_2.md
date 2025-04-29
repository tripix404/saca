# README – web_scraper.py

## 📄 Overzicht

`web_scraper.py` is een Python-tool voor het **crawlen van websites**, het opslaan van HTML (en optioneel tekst), en het loggen van verdachte patronen (zoals wachtwoorden, tokens, enz.).  
De tool is bedoeld voor educatieve, onderzoeks- en security-auditdoeleinden, en **respecteert robots.txt** en de ethische grenzen van webscraping.

---

## ⚙️ Gebruikte elementen en keuzes

### 1. **requests**
- **Waarom?**  
  De requests-bibliotheek is dé standaard voor HTTP-verzoeken in Python: eenvoudig, krachtig en breed ondersteund[4][5].
- **Alternatief:**  
  - *urllib*: Minder gebruiksvriendelijk, meer boilerplate.
  - *httpx*: Geavanceerder, maar requests is voor deze scope voldoende.

### 2. **BeautifulSoup (beautifulsoup4)**
- **Waarom?**  
  Voor het efficiënt en flexibel parsen van HTML, met ondersteuning voor CSS-selectors en robuuste fouttolerantie[2][4][5].
- **Alternatief:**  
  - *lxml*: Sneller, maar minder intuïtief voor beginners en minder tolerant voor slecht gevormde HTML.
  - *Selenium*: Nodig voor dynamische sites met veel JavaScript, maar veel zwaarder/slomer.

### 3. **argparse**
- **Waarom?**  
  Maakt het script flexibel en makkelijk te gebruiken via de commandline.
- **Alternatief:**  
  - *click*: Mooi voor grotere CLI-projecten, maar argparse is standaard en voldoende voor deze tool.

### 4. **logging**
- **Waarom?**  
  Logging is beter dan print-statements: het is configureerbaar, professioneel en geschikt voor foutopsporing.
- **Alternatief:**  
  - *print*: Niet geschikt voor grotere of herbruikbare projecten.

### 5. **robots.txt-check (RobotFileParser)**
- **Waarom?**  
  Respecteren van robots.txt is essentieel voor ethisch scrapen en voorkomt juridische problemen.
- **Alternatief:**  
  - *Geen check*: Onverantwoord en mogelijk onwettig.

### 6. **Regex pattern matching**
- **Waarom?**  
  Maakt het mogelijk om gevoelige of verdachte patronen te detecteren in content (bijvoorbeeld: wachtwoorden, API-tokens).
- **Alternatief:**  
  - *Handmatige string search*: Minder krachtig en minder flexibel dan regex.

### 7. **Bestandsnaam-sanitatie**
- **Waarom?**  
  Voorkomt problemen met rare tekens in URLs bij het opslaan op schijf.

### 8. **Progress-indicator & retry-logica**
- **Waarom?**  
  Gebruikersvriendelijk en maakt de tool robuuster tegen netwerkproblemen.

---

## 🚀 Voorbeeldgebruik

### **Standaard crawl**


Hier is een **Markdown-bestand** met alleen de gevraagde voorbeeldcommando’s, netjes gebundeld en voorzien van korte toelichting:

```markdown
# Voorbeeldcommando's voor web_scraper.py

Hieronder vind je de belangrijkste voorbeeldcommando's voor het gebruik van `web_scraper.py`:

---

**1. Standaard crawl naar een map**

```

python web_scraper.py --start-url https://example.com --output-dir ./dump

```

*Start met crawlen vanaf de opgegeven URL en sla alle gevonden pagina’s op in de map `./dump`.*

---

**2. Crawl met patroonherkenning (bijvoorbeeld wachtwoorden of tokens)**

```

python web_scraper.py --start-url https://example.com --pattern "password|token|api[_-]?key" --output-dir ./dump

```

*Zoek in elke pagina naar patronen zoals 'password', 'token' of 'api_key' en log deze.*

---

**3. Crawl met een limiet op het aantal pagina’s**

```

python web_scraper.py --start-url https://example.com --max-pages 50 --output-dir ./dump

```

*Stop met crawlen na het bereiken van 50 unieke pagina’s.*

---

**4. Alleen zichtbare tekst opslaan (geen HTML)**

```

python web_scraper.py --start-url https://example.com --text-only --output-dir ./dump

```

*Sla van elke pagina alleen de zichtbare tekst op als `.txt`-bestand.*

---

**Let op:**  
- Combineer opties naar wens, bijvoorbeeld om maximaal 10 pagina’s te crawlen en alleen tekst op te slaan:
```

python web_scraper.py --start-url https://example.com --max-pages 10 --text-only --output-dir ./dump



<div style="text-align: center">⁂</div>
