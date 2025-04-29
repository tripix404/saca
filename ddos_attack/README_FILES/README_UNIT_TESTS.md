# README – Unit Tests voor ddos_attack.py

## 📋 Overzicht

Deze unit tests zijn geschreven voor het Python-script `ddos_attack.py`, dat een educatieve DDoS-simulator bevat. De tests zijn bedoeld om de betrouwbaarheid, veiligheid en correctheid van de belangrijkste functies van het script te waarborgen.

---

## 🧩 Opbouw van de Unit Tests

### 1. **Waarom deze elementen?**
- **unittest**: De standaard Python testbibliotheek, gekozen vanwege eenvoud, brede ondersteuning en geen externe dependencies nodig. Alternatieven als `pytest` zijn krachtiger, maar minder standaard en voegen voor deze scope weinig toe.
- **unittest.mock**: Gebruikt om netwerkverkeer (`socket`), tijd (`time.sleep`) en user input te simuleren. Zo blijven de tests snel, herhaalbaar en onafhankelijk van de echte infrastructuur.
- **AAA-patroon (Arrange, Act, Assert)**: Elke test is opgezet volgens dit patroon voor maximale leesbaarheid en onderhoudbaarheid.
- **Korte, beschrijvende testnamen**: De naam van elke test geeft direct aan welk gedrag wordt getest, zodat de testoutput ook als documentatie dient.

### 2. **Waarom geen alternatieven?**
- **Geen integratietests**: Er wordt niet getest met echte netwerkverbindingen of externe systemen. Dit zou de tests traag en minder betrouwbaar maken en hoort thuis in aparte integratietests.
- **Geen complexe testframeworks**: Voor deze scope is unittest voldoende en overzichtelijk.
- **Geen infrastructuurafhankelijkheden**: Door alles te mocken, zijn de tests altijd herhaalbaar en snel, ongeacht de omgeving.

---

## 🧪 Wat wordt er getest en waarom?

| Test                        | Wat wordt getest?                                      | Waarom is dit belangrijk?                                  |
|-----------------------------|--------------------------------------------------------|------------------------------------------------------------|
| test_initial_parameters     | Of de standaard parameters veilig en correct zijn      | Voorkomt onbedoelde aanvallen op verkeerde doelen/poorten  |
| test_packet_count           | Of het juiste aantal threads wordt aangemaakt en gestart | Zodat de aanvalssimulatie correct parallel verloopt        |
| test_payload_randomization  | Of de payloads voldoende willekeurig zijn              | Voorkomt detectie door simpele patroonherkenning           |
| test_rate_limiting          | Of de rate limiting per thread klopt                   | Beschermt het netwerk en zorgt voor realistische simulatie |
| test_target_ip_format       | Of het target IP een geldig privé-adres is             | Voorkomt dat het script onbedoeld naar het internet stuurt |

**Waarom deze onderdelen?**  
Deze aspecten zijn essentieel voor een veilige, betrouwbare en reproduceerbare simulatie. Elk getest punt sluit aan bij best practices voor unit testing: snel, geïsoleerd, herhaalbaar en zonder afhankelijkheden van externe systemen.

---

## 🏁 Hoe voer je de tests uit?

1. Zorg dat je in dezelfde directory zit als `test_ddos_simulator.py` en `ddos_attack.py`.
2. Voer de tests uit met:
