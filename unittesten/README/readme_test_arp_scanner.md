# README – Unittests voor ARP Scanner

## Inhoud

- [Beschrijving](#beschrijving)
- [Gebruikte modules](#gebruikte-modules)
- [Waarom deze modules?](#waarom-deze-modules)
- [Niet-gebruikte alternatieven](#niet-gebruikte-alternatieven)
- [Uitvoeren van de tests](#uitvoeren-van-de-tests)
- [Testoverzicht](#testoverzicht)

---

## Beschrijving

Dit bestand bevat unittests voor de `arp_scan`-functie uit het script `toolkit.py`.
De tests zijn bedoeld om de werking van de ARP-scanner te controleren zonder echte netwerkverzoeken of gebruikersinteractie.
Belangrijke aspecten zoals interface selectie, foutafhandeling en logging worden gecontroleerd.

---

## Gebruikte modules

- **unittest**
Het standaard Python test-framework, gebruikt voor het structureren en uitvoeren van de tests.
- **unittest.mock**
Gebruikt voor het mocken van externe afhankelijkheden zoals Scapy-functies, gebruikersinvoer (`input`), en logging.
Onderdelen: `patch`, `MagicMock`, `call`.
- **io.StringIO**
Kan gebruikt worden om standaarduitvoer te vangen, bijvoorbeeld voor het testen van print-statements.
- **logging**
Gebruikt om logberichten op te vangen en te controleren of de juiste meldingen worden gelogd.
- **pathlib.Path**
Wordt geïmporteerd voor mogelijke pad-bewerkingen, maar in deze tests niet direct gebruikt.
- **scapy.all**
Wordt gemockt om te voorkomen dat er echte netwerkpakketten worden verzonden tijdens het testen.
- **scapy.arch.common.NetworkInterface**
Wordt gebruikt om netwerkinterfaces te mocken.
- **toolkit**
Het eigen script waarin de te testen functie `arp_scan` zich bevindt.

---

## Waarom deze modules?

- **unittest** en **unittest.mock** zijn standaard in Python, breed ondersteund, en krachtig genoeg voor het isoleren van alle externe afhankelijkheden.
- **MagicMock** maakt het eenvoudig om complexe objecten zoals netwerkinterfaces of pakketten na te bootsen.
- **patch** zorgt ervoor dat tijdens tests geen echte netwerkverzoeken, gebruikersinput, of logging wordt uitgevoerd.
- **logging** wordt getest om te controleren of foutmeldingen correct worden afgehandeld.
- **scapy** wordt alleen als dependency gebruikt om de interface van de echte functies te behouden; alle netwerkverkeer wordt volledig gemockt.

---

## Niet-gebruikte alternatieven

- **pytest**
Hoewel `pytest` populair is vanwege zijn eenvoud en krachtige fixture-systeem, is het voor deze unittests niet noodzakelijk.
`unittest` is voldoende krachtig en vereist geen extra installatie.
- **responses** of **requests-mock**
Deze modules zijn bedoeld voor HTTP-verkeer, niet voor ARP/scapy-verkeer.
- **tempfile**
Niet nodig, omdat er geen echte bestanden worden aangemaakt of gelezen.
- **hypothesis**
Property-based testing is krachtig, maar voor deze functionele tests is het overkill.

---

## Uitvoeren van de tests

1. Zorg dat je `toolkit.py` en dit unittest-bestand in dezelfde map staan.
2. Installeer Scapy als dat nog niet gebeurd is (`pip install scapy`).
3. Voer de tests uit met:

```bash
python -m unittest test_arp_scanner.py -v
```


---

## Testoverzicht

De volgende scenario’s worden getest:

- **Succesvolle ARP-scan**: Mocked ARP-antwoorden worden correct verwerkt.
- **Geen apparaten gevonden**: Logging wordt correct uitgevoerd.
- **Annulering door gebruiker**: De scan wordt netjes afgebroken.
- **Foutafhandeling**: Fouten in Scapy worden gelogd en correct afgehandeld.
- **Interface selectie**: Meerdere netwerkinterfaces en gebruikerskeuze worden getest.

Alle externe afhankelijkheden zijn gemockt, zodat de tests snel, veilig en onafhankelijk van het netwerk zijn.

---
