# Ethical Hacking Toolkit — SACA

**HOWEST — Georges Devos**

---

## Overzicht

SACA is een Python-based cybersecurity toolkit ontwikkeld voor educatieve doeleinden binnen netwerkbeveiliging en ethisch hacken.

De tool bundelt verschillende technieken die gebruikt worden in:

* netwerk analyse
* security testing
* basis penetration testing

> **Gebruik uitsluitend in geautoriseerde en gecontroleerde omgevingen.**

---

## Functionaliteiten

De toolkit bevat volgende modules:

* **DDoS Simulator**
  Simuleert een UDP-flood om netwerkgedrag te analyseren.

* **MAC Spoofer (Windows)**
  Wijzigt het MAC-adres van een netwerkinterface.

* **Web Scraper**
  Extraheert en analyseert HTML-content van websites.

* **ARP Scanner + Portscan**
  Detecteert actieve hosts en scant open poorten.

* **SSH Bruteforce (lab-only)**
  Simuleert een brute force aanval op een SSH-service.

* **Hoofdmenu**
  Centrale interface om alle tools te bedienen.

---

## Installatie

### Vereisten

* Python 3.10+
* Linux of Windows

### Setup

```bash
git clone https://github.com/tripix404/saca.git
cd saca
pip install -r requirements.txt
```

---

## Gebruik

### Start de toolkit

```bash
python main.py
```

### Individuele tools

| Tool           | Commando                               | Beschrijving                 |
| -------------- | -------------------------------------- | ---------------------------- |
| DDoS Simulator | `python ddos_attack.py`                | UDP-flood simulatie          |
| MAC Spoofer    | `python mac_spoof.py`                  | MAC-adres wijzigen (Windows) |
| Web Scraper    | `python web_scraper.py --all`          | Website scraping             |
| ARP Scanner    | `python arp_scanner.py 192.168.1.0/24` | Netwerk discovery + portscan |

---

## Projectstructuur

```text
saca/
├── main.py
├── requirements.txt
├── arp_scanner/
├── port_scanner/
├── ssh_bruteforce/
├── web_scraper/
├── ddos_attack/
├── results/
└── README.md
```

---

## Output

* Resultaten worden opgeslagen in `results/`
* Logs worden lokaal gegenereerd en niet in Git opgeslagen

---

## Technische keuzes (kort)

* **Scapy** → low-level netwerk interactie (ARP, packets)
* **Paramiko** → SSH communicatie en authenticatie
* **Requests + BeautifulSoup** → web scraping
* **Colorama** → terminal output
* **Threading** → parallelle netwerkoperaties

---

## Veelvoorkomende problemen

### Missing dependencies

```bash
pip install -r requirements.txt
```

### Permission issues

* Linux:

```bash
sudo python3 main.py
```

* Windows:
  Run terminal als Administrator

---

### Port conflicts

Pas poort aan in code indien nodig:

```python
TARGET_PORT = 8081
```

---

## Security & Legal

Deze toolkit is **uitsluitend bedoeld voor educatieve doeleinden**.

Toegestaan gebruik:

* gecontroleerde labomgeving
* systemen waarvoor expliciete toestemming is

Verboden gebruik:

* publieke netwerken scannen zonder toestemming
* echte DDoS-aanvallen uitvoeren
* gebruik in productieomgevingen

## Auteur
 
Bachelor Cybersecurity — Howest
---

## Licentie

MIT License (educatief gebruik)

---
