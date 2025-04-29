
## 2. Mini DDoS Attack Capability (`mini_ddos.py`)

### Doel

- Simuleer een lichte UDP-flood naar een lokaal target voor test- en tegenmaatregelen in een veilige omgeving.
- Hard-coded standaard-IP voor veiligheid, met CLI-overriding.

### Gebruikte elementen en keuzes

| Element          | Reden                                         | Alternatief         |
| ---------------- | --------------------------------------------- | ------------------- |
| `socket.AF_INET` | Directe UDP-sockets zonder extra bibliotheken | `scapy`             |
| `argparse`       | CLI-configuratie zonder externe pakketten     | `click`, `typer`    |
| `time.sleep`     | Simpele throttle van packet-per-second (pps)  | erlang-rate limiter |
| Hard-coded IP    | Voorkomt per ongeluk gevaarlijke targets      | config-bestand      |

### CLI-opties

```bash
# Stuur 1000 UDP-pakketten naar 192.168.1.100:8080 met max 200 pakketten/sec
python3 mini_ddos.py \
  --target-ip 192.168.1.100 \
  --target-port 8080 \
  --packets 1000 \
  --pps 200
```

---

## Installatie

1. Clone de repository:
   ```bash
   ```

git clone https\:///jouwerzijn/cyber\_toolkit.git cd cyber\_toolkit

````
2. Installeer afhankelijkheden (voor de web scraper):
```bash
pip install requests beautifulsoup4
````

---

## Ethische richtlijnen

- **Alle scripts zijn alleen bedoeld voor test‐ en leeromgevingen.**
- **Gebruik nooit tegen productie‑sites of zonder expliciete toestemming.**
- Beperk tests tot lokale of geautoriseerde sandboxes.

---

*README aangemaakt door Georges Devos voor de cursus "Scripting and Code Analysis" aan HoWest.*

