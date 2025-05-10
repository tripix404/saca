# README – Unittests voor DDoS Attack Script

## Inhoud

- [Beschrijving](#beschrijving)
- [Gebruikte modules](#gebruikte-modules)
- [Waarom deze modules?](#waarom-deze-modules)
- [Niet-gebruikte alternatieven](#niet-gebruikte-alternatieven)
- [Uitvoeren van de tests](#uitvoeren-van-de-tests)
- [Testoverzicht](#testoverzicht)

---

## Beschrijving

Dit bestand bevat unittests voor het script `ddos_attack.py`.
De tests zijn bedoeld om de werking van de DDoS-simulator te controleren zonder echte netwerkverzoeken, gebruikersinteractie of systeemveranderingen.
Belangrijke aspecten als schermopmaak, gebruikersbevestiging, flood-functie, threadbeheer en foutafhandeling worden getest.

---

## Gebruikte modules

- **unittest**
Het standaard Python test-framework, gebruikt voor het structureren en uitvoeren van de tests.
- **unittest.mock**
Gebruikt voor het mocken van externe afhankelijkheden zoals systeemaanroepen (`os.system`), netwerkfuncties (`socket.socket`), threading, gebruikersinput, en systeem-exits.
Onderdelen: `patch`, `MagicMock`, `call`.
- **io.StringIO**
Gebruikt om standaarduitvoer te vangen, bijvoorbeeld voor het testen van banner-uitvoer.
- **sys**
Nodig voor het patchen van `sys.exit` en om de standaarduitvoer te mocken.
- **os**
Nodig voor het patchen van `os.system` en `os.get_terminal_size`.
- **ddos_attack**
Het eigen script waarin de te testen functies zich bevinden.

---

## Waarom deze modules?

- **unittest** en **unittest.mock** zijn standaard in Python, breed ondersteund, en krachtig genoeg om alle externe afhankelijkheden te isoleren.
- **MagicMock** maakt het eenvoudig om complexe objecten zoals sockets of threads na te bootsen.
- **patch** zorgt ervoor dat tijdens tests geen echte netwerk-, systeem- of gebruikersacties worden uitgevoerd.
- **StringIO** maakt het mogelijk om de uitvoer van functies te controleren zonder de terminal te gebruiken.
- **os** en **sys** zijn nodig om systeemfuncties te patchen en te controleren.

---

## Niet-gebruikte alternatieven

- **pytest**
Hoewel `pytest` populair is vanwege zijn eenvoud en krachtige fixture-systeem, is het voor deze unittests niet noodzakelijk.
`unittest` is voldoende krachtig en vereist geen extra installatie.
- **responses** of **requests-mock**
Deze modules zijn bedoeld voor HTTP-verkeer, niet voor UDP-sockets of threading.
- **tempfile**
Niet nodig, omdat er geen echte bestanden worden aangemaakt of gelezen.
- **hypothesis**
Property-based testing is krachtig, maar voor deze functionele tests is het overkill.
- **mockito**
Een alternatieve mocking-library, maar `unittest.mock` is standaard en krachtig genoeg.

---

## Uitvoeren van de tests

1. Zorg dat je `ddos_attack.py` en dit unittest-bestand in dezelfde map staan.
2. Voer de tests uit met:

```bash
python -m unittest test_ddos.py -v
```


---

## Testoverzicht

De volgende scenario’s worden getest:

- **Scherm wissen**: Zowel voor Windows als Linux/Unix.
- **Banner tonen**: Controle of de banner correct wordt weergegeven.
- **Bevestiging van veilige omgeving**: Zowel annulering als terugkeer naar menu.
- **Flood-functie**: Zowel met als zonder DNS-camouflage.
- **Threadbeheer en hoofdlogica**: Controle of het juiste aantal threads wordt gestart en of de juiste functies worden aangeroepen.
- **KeyboardInterrupt/foutafhandeling**: Controleren of het script netjes stopt bij een onderbreking.

Alle externe afhankelijkheden zijn gemockt, zodat de tests snel, veilig en onafhankelijk van het netwerk of het besturingssysteem zijn.

---
