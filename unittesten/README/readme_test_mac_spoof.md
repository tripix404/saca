# README – Unittests voor MAC Spoofing Script

## Inhoud

- [Beschrijving](#beschrijving)
- [Gebruikte modules](#gebruikte-modules)
- [Waarom deze modules?](#waarom-deze-modules)
- [Niet-gebruikte alternatieven](#niet-gebruikte-alternatieven)
- [Uitvoeren van de tests](#uitvoeren-van-de-tests)
- [Testoverzicht](#testoverzicht)

---

## Beschrijving

Dit bestand bevat unittests voor het script `mac_spoof.py`.
De tests zijn bedoeld om de werking van de belangrijkste functies van de MAC spoofing tool te controleren zonder echte systeemwijzigingen of netwerkacties.
Belangrijke aspecten als platformdetectie, MAC-adresgeneratie, commandorun, en admin-checks worden getest.

---

## Gebruikte modules

- **unittest**
Het standaard Python test-framework, gebruikt voor het structureren en uitvoeren van de tests.
- **unittest.mock**
Gebruikt voor het mocken van externe afhankelijkheden zoals OS-functies, subprocessen, random-getallen en platformdetectie.
Onderdelen: `patch`, `MagicMock`.
- **re**
Gebruikt om te controleren of het gegenereerde MAC-adres het juiste formaat heeft.
- **mac_spoof**
Het eigen script waarin de te testen functies zich bevinden.

---

## Waarom deze modules?

- **unittest** en **unittest.mock** zijn standaard in Python, breed ondersteund, en krachtig genoeg om alle externe afhankelijkheden te isoleren.
- **MagicMock** maakt het eenvoudig om complexe objecten zoals subprocess-resultaten na te bootsen.
- **patch** zorgt ervoor dat tijdens tests geen echte OS-, subprocess- of random-acties worden uitgevoerd.
- **re** is handig om te valideren of een string voldoet aan het gewenste MAC-adresformaat.

---

## Niet-gebruikte alternatieven

- **pytest**
Hoewel `pytest` populair is vanwege zijn eenvoud en krachtige fixture-systeem, is het voor deze unittests niet noodzakelijk.
`unittest` is voldoende krachtig en vereist geen extra installatie.
- **random-mock**
Alle random-functionaliteit wordt rechtstreeks met `unittest.mock.patch` gemockt, waardoor een extra library overbodig is.
- **tempfile**
Niet nodig, omdat er geen echte bestanden worden aangemaakt of gelezen.
- **hypothesis**
Property-based testing is krachtig, maar voor deze functionele tests is het overkill.
- **mockito**
Een alternatieve mocking-library, maar `unittest.mock` is standaard en krachtig genoeg.

---

## Uitvoeren van de tests

1. Zorg dat je `mac_spoof.py` en dit unittest-bestand in dezelfde map staan.
2. Voer de tests uit met:

```bash
python -m unittest test_mac_spoof.py -v
```


---

## Testoverzicht

De volgende scenario’s worden getest:

- **Platformdetectie**: Windows en Linux worden gesimuleerd.
- **MAC-adresgeneratie**: Controleren van het formaat en de inhoud van het gegenereerde MAC-adres.
- **Commandorun**: Zowel geslaagde als mislukte subprocess-aanroepen.
- **Admin-checks**: Zowel voor Linux als voor Windows, inclusief foutafhandeling.
- **Uitbreidbaarheid**: De structuur maakt het eenvoudig om meer tests toe te voegen, bijvoorbeeld voor registry-functies.

Alle externe afhankelijkheden zijn gemockt, zodat de tests snel, veilig en onafhankelijk van het besturingssysteem zijn.

---
