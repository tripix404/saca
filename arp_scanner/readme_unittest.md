
# kan je een readme bestand schrijven van de unittesten, daarbij ook uitleg waarom de gebruikte elementen gekozen zijn en niet de mogelijke alternatieven?

```markdown
# Ethical Hacking Toolkit - Unit Tests

## 📋 Overzicht
Deze tests valideren de kernfunctionaliteit van het ethical hacking script **zonder echt netwerkverkeer** te genereren. Alle externe afhankelijkheden (netwerk, bestanden, user input) worden gesimuleerd voor veilige en reproduceerbare tests.

## 🧪 Teststrategie
### 1. ARP-scan tests
- **Doel**: Valideer interface detectie en device discovery
- **Gebruikte technieken**:
  - `unittest.mock.patch` voor `srp` en `get_working_ifaces`
  - MagicMock voor gesimuleerde netwerkinterfaces
- **Reden keuze**: Vermijdt echte netwerkoperaties terwijl scapy's interne logica behouden blijft

### 2. SSH Bruteforce tests
- **Doel**: Test wachtwoordpogingen en error handling
- **Gebruikte technieken**:
  - `mock_open` voor het simuleren van `passwords.txt`
  - Side effects voor gesimuleerde loginpogingen
- **Reden keuze**: Voorkomt echte SSH-connecties naar externe hosts

### 3. Asynchrone portscan tests
- **Doel**: Valideer basis werking async I/O
- **Gebruikte technieken**:
  - `asyncio.run()` voor async test execution
  - Test op localhost-poort 65535 (altijd gesloten)
- **Reden keuze**: Minimaliseert false positives zonder netwerkconfiguratie

## 🔑 Belangrijke designkeuzes
### 1. `unittest.mock` i.p.v. externe mocking libraries
- **Waarom**:  
  ✅ Standaard Python library (geen extra dependencies)  
  ✅ Eenvoudige integratie met unittest  
  ❌ Alternatief (bv. `pytest-mock`): Vereist pytest installatie

### 2. MagicMock voor complexe objecten
- **Waarom**:  
  ✅ Simuleert scapy interface objecten realistisch  
  ✅ Vermijdt complexe subclassing van echte objecten  
  ❌ Alternatief (manual mocks): Meer onderhoudsgevoelig

### 3. Asyncio test wrapper
```

async def run_test():
result = await async_port_scan(...)
asyncio.run(run_test())

```
- **Waarom**:  
  ✅ Eenvoudig async functies testen in sync context  
  ❌ Alternatief (pytest-asyncio): Vereist extra plugin

### 4. Side effects voor SSH-connect
```

mock_connect.side_effect = lambda...

```
- **Waarom**:  
  ✅ Simuleert dynamisch gedrag per wachtwoordpoging  
  ❌ Alternatief (statische return values): Minder realistisch

## 🚫 Niet-gebruikte alternatieven
### 1. Echte netwerkpoorten scannen
- **Waarom niet**:  
  ⚠️ Onbetrouwbaar (firewalls, beschikbare services)  
  ⚠️ Langzaam bij grote port ranges

### 2. Parameterized tests
```

@parameterized.expand([...])

```
- **Waarom niet**:  
  ✅ Mogelijk met `unittest`, maar vereist extra lib  
  ✅ Handmatige parametrisatie houdt tests expliciet

### 3. Dockerized testomgeving
- **Waarom niet**:  
  ⚠️ Complex opzetten voor unit tests  
  ⚠️ Overkill voor geïsoleerde functietests

## ▶️ Tests uitvoeren
### Vereisten
```

pip install scapy paramiko

```

### Commando
```

python -m unittest test_toolkit.py -v

```

### Voorbeelduitvoer
```

test_arp_scan (test_toolkit.TestEthicalHackingToolkit) ... ok
test_async_port_scan (test_toolkit.TestEthicalHackingToolkit) ... ok
test_save_results (test_toolkit.TestEthicalHackingToolkit) ... ok
test_ssh_bruteforce_fail (test_toolkit.TestEthicalHackingToolkit) ... ok
test_ssh_bruteforce_success (test_toolkit.TestEthicalHackingToolkit) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.002s
OK

```

## 📊 Resultaatinterpretatie
- **OK**: Alle mocked scenario's werken zoals verwacht
- **FAIL**: Logicafout in specifieke use case
- **ERROR**: Onverwachte exception (bv. import fout)

## Conclusie
Deze testaanpak balanceert **realisme** en **veiligheid** door kritieke componenten te isoleren zonder complexe testinfrastructuur. Keuzes zijn gericht op onderhoudbaarheid en minimale externe afhankelijkheden.
```

