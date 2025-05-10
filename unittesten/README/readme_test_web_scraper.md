# README – Unittests voor Web Scraper

## Inhoud

- [Beschrijving](#beschrijving)
- [Benodigde modules](#benodigde-modules)
- [Waarom deze modules?](#waarom-deze-modules)
- [Niet-gebruikte alternatieven](#niet-gebruikte-alternatieven)
- [Uitvoeren van de tests](#uitvoeren-van-de-tests)
- [Testoverzicht](#testoverzicht)

---

## Beschrijving

Deze unittests zijn bedoeld om de functionaliteit van de `WebScraper`-klasse en bijbehorende hulpfuncties te controleren. De tests dekken onder andere:

- Bestandsnaam-sanitatie
- Output-directory-constructie
- Downloaden van bestanden (HTML, afbeeldingen, PDF's)
- Pagina-opslag
- Crawlen van links
- Foutafhandeling

De tests zijn ontworpen om **veilig, snel en reproduceerbaar** te zijn, zonder afhankelijk te zijn van externe netwerken of het echte bestandssysteem.

---

## Benodigde modules

De volgende Python-modules worden gebruikt in de unittests:

- **unittest**
Standaard Python testframework voor het schrijven en uitvoeren van tests.
- **unittest.mock**
Voor het mocken van externe afhankelijkheden zoals netwerkverkeer, bestandssysteem en HTML-parsing.
Gebruikt onderdelen als `patch`, `MagicMock`, en `mock_open`.
- **os**
Voor mocken van directory-operaties zoals `os.makedirs` en `os.path.join`.
- **paste**
(Jouw eigen module, met daarin de `WebScraper`-klasse en hulpfuncties.)

---

## Waarom deze modules?

- **unittest** is de standaard in de Python-wereld, goed ondersteund, en vereist geen extra installatie.
- **unittest.mock** is krachtig en flexibel voor het isoleren van de te testen logica en het voorkomen van echte netwerk- of schijfoperaties.
- **os** wordt alleen gebruikt om het gedrag van directory- en padfuncties te simuleren.

Deze combinatie maakt het mogelijk om **alle externe interacties te isoleren** en te controleren of de interne logica correct werkt.

---

## Niet-gebruikte alternatieven

- **pytest**
Hoewel zeer populair en gebruiksvriendelijk, is `pytest` niet strikt noodzakelijk voor deze tests. `unittest` is voldoende krachtig en vereist geen extra dependencies.
Voor eenvoudige projecten en maximale compatibiliteit is `unittest` vaak de beste keus.
- **responses** of **requests-mock**
Deze modules zijn handig voor het mocken van HTTP-verkeer, maar in deze tests is het eenvoudiger om direct `requests.get` te mocken met `unittest.mock`.
Dit houdt de dependencies minimaal.
- **tempfile**
Voor het testen van bestandsoperaties kan `tempfile` nuttig zijn, maar omdat we geen echte bestanden willen aanmaken, gebruiken we `mock_open` uit `unittest.mock`.
- **fixtures of hypothesis**
Voor property-based testing of geavanceerde fixtures zijn deze modules krachtig, maar voor deze unittests is dat overkill.

---

## Uitvoeren van de tests

1. Zorg dat je `web_scraper.py` (of `paste.py` als dat de naam is) en `test_web_scraper.py` in dezelfde map staan.
2. Installeer dependencies indien nodig (alle gebruikte modules zijn standaard in Python 3.6+).
3. Voer de tests uit met:

```bash
python -m unittest test_web_scraper.py -v
```


---

## Testoverzicht

De tests controleren onder andere:

- Correcte bestandsnaam-sanitatie
- Correcte constructie van output directories
- Downloaden en opslaan van HTML, afbeeldingen en PDF's (met mocks)
- Correcte aanroep van bestandsoperaties
- Het crawlen van links en het vermijden van dubbele bezoeken
- Foutafhandeling bij netwerkproblemen

Alle externe interacties (HTTP, bestandsysteem, BeautifulSoup) worden gemockt, zodat de tests snel en zonder bijwerkingen zijn.

---