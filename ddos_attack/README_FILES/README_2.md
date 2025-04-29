## 🔍 Doelstelling
Een realistisch maar veilig instrument om DDoS-aanvalprincipes te bestuderen, met focus op:
- UDP-flood dynamiek
- Detectie-ontwijkingstechnieken
- Mitigatie-experimenten

## 🛠️ Kenmerken

### 📦 **Kernfunctionaliteit**
| Functie                | Implementatie          | Reden                          | Alternatief Niet Gebruikt      |
|------------------------|------------------------|--------------------------------|--------------------------------|
| **Transportprotocol**  | UDP                    | Connectionless, low overhead  | TCP (moeilijker te spoofen)    |
| **Payload**            | Willekeurige bytes     | Detectie-ontwijking            | Vaste patronen (makkelijker te filteren) |
| **Timing**             | Poisson-distributie    | Natuurlijk verkeerspatroon     | Vaste intervals (onnatuurlijk) |
| **Parallelisatie**     | Threading              | Eenvoudige implementatie       | Async I/O (complexer)          |

### 🔒 **Veiligheidsmaatregelen**
| Maatregel              | Technische Implementatie       | Reden                          |
|------------------------|---------------------------------|--------------------------------|
| Bevestigingscheck      | `input()`-validatie            | Voorkomt accidenteel misbruik  |
| Rate limiting          | `RATE_PPS` (hardcoded)         | Beperkt netwerkimpact          |
| Geen IP-spoofing       | Gebruik echte source IP's       | Traceerbaarheid behouden       |
| Lokale target          | `192.168.1.1` (privé-IP)       | Voorkomt extern misbruik       |

## ⚖️ Voor- en Nadelen

### ✅ **Voordelen**
1. **Educatieve duidelijkheid**  
   - Eenduidige codestructuur voor analyse
   - Geen externe dependencies (`python3` standaardbibliotheek)

2. **Configureerbare veiligheid**  
   - Harde limieten voor packets/sec en totaal volume
   - DNS-camouflage optioneel

3. **Detectie-ontwijking**  
   - Willekeurige packetgroottes (64-1500 bytes)
   - Exponentiële timingverdeling

### ⚠️ **Beperkingen**
1. **Schaalbaarheid**  
   - Python's GIL limiteert parallelle prestaties (~500 pps max)
   - Geen echte IP-spoofing mogelijk

2. **Camouflage-niveau**  
   - Basis DNS-header (statische velden)
   - Gebruikt poort 8080 i.p.v. 53 (standaard DNS)

3. **Monitoring**  
   - Geen real-time statistieken
   - Beperkte error handling

## 🚀 Gebruiksaanwijzing

### 1. Testomgeving Opzetten
