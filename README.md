# Ethical Hacking Toolkit - HOWEST - Georges Devos

## 🌟 Overzicht
Een verzameling Python tools ontwikkeld voor educatieve netwerkbeveiliging en ethisch hacken. **Alleen gebruiken in geautoriseerde testomgevingen!**

### Tools Inclusief:
1. **DDoS Simulator** - UDP-flood aanval demo
2. **MAC Spoofer** - Windows MAC-adres manipulatie
3. **Web Scraper Pro** - Geavanceerde content-extractie
4. **ARP Scanner** - Netwerkdevice detectie + portscan
5. **Hoofdmenu** - Geïntegreerde tool interface

## 🛠️ Installatie

### Vereisten:
```


# Linux

sudo apt install python3-pip

# Windows: Installeer Python 3.12+ van python.org

# Globale dependencies

pip install scapy paramiko colorama requests beautifulsoup4 python-nmap

```


## 🚀 Gebruik

### Hoofdmenu:
```

python main.py

```


### Individuele Tools:
| Tool                  | Commando                          | Beschrijving                     |
|-----------------------|-----------------------------------|-----------------------------------|
| DDoS Simulator        | `python ddos_attack.py`          | UDP-flood met rate limiting      |
| MAC Spoofer           | `python mac_spoof.py`            | Windows MAC-adres wijzigen       |
| Web Scraper           | `python web_scraper.py --all`    | Volledige website archivering    |
| ARP Scanner           | `python arp_scanner.py 192.168.1.0/24` | Netwerk discovery + poortscan |

## 📚 Gebruikte Modules & Rationale

### 1. Scapy (ARP Scanner)
- **Doel:** Low-level netwerkpakket manipulatie
- **Alternatieven:** `socket` (te low-level), `pypcap` (minder features)
- **Reden:** Biedt complete ARP/UDP/TCP stack controle + cross-platform ondersteuning

### 2. Paramiko (SSH Bruteforce)
- **Doel:** SSH protocol implementatie
- **Alternatieven:** `pexpect` (onbetrouwbaar), `fabric` (te high-level)
- **Reden:** Ondersteunt geavanceerde SSH features + exception handling

### 3. Colorama (Alle Tools)
- **Doel:** Terminal kleurcodering
- **Alternatieven:** `termcolor` (minder features), `blessings` (complex)
- **Reden:** Eenvoudige Windows/Linux compatibiliteit + reset functionaliteit

### 4. BeautifulSoup (Web Scraper)
- **Doel:** HTML/XML parsing
- **Alternatieven:** `lxml` (strict), `pyquery` (jQuery syntax)
- **Reden:** Uitstekende fouttolerantie + eenvoudige API

### 5. Threading/Asyncio (DDoS/Portscan)
- **Doel:** Parallelle verwerking
- **Alternatieven:** `multiprocessing` (zwaarder), `celery` (overkill)
- **Reden:** Lichtgewicht I/O-bound operaties

## ⚖️ Juridische Notities

### Verboden Gebruik:
- ❌ Publieke netwerken scannen zonder toestemming
- ❌ Echte DDoS-aanvallen uitvoeren
- ❌ MAC-adres spoofen in productieomgevingen

### Veiligheidsmaatregelen:
```


# Voorbeeld veiligheidscheck in code

def bevestig_veilige_omgeving():
confirm = input("Bevestig gecontroleerde omgeving (ja/nee): ")
if confirm.lower() != "ja":
sys.exit("Uitvoering gestopt")

```

## 🔧 Technische Specificaties

### ARP Scanner Architectuur:
```

graph TD
A[User Interface] --> B[ARP Request Generator]
B --> C[Packet Sniffer]
C --> D[Resultatenverwerker]
D --> E[JSON Output]

```

### Prestatie Statistieken:
| Tool                  | Threads | Pakketten/sec | Geheugen Usage |
|-----------------------|---------|---------------|----------------|
| DDoS Simulator        | 50      | 25.000        | <50 MB         |
| ARP Scanner           | 1       | 1000          | <30 MB         |
| Web Scraper           | 10      | 100           | <200 MB        |

## 🚨 Veelvoorkomende Problemen

### 1. Missing Dependencies:
```


# Windows fout:

ModuleNotFoundError: No module named 'winreg'

# Oplossing:

pip install pywin32

```

### 2. Permission Issues:
```


# Linux/Mac:

sudo python3 mac_spoof.py

# Windows: Run as Administrator

```

### 3. Port Conflicts:
```


# Poort wijzigen in code:

TARGET_PORT = 8080  \# -> 8081

```

## 📜 Licentie
MIT License - **Strict verbod op misbruik**  
```

Copyright 2024 HOWEST - Georges Devos

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files to use exclusively
in ethical hacking education and authorized penetration testing.

```

> **LET OP:** Deze tools zijn uitsluitend bedoeld voor educatieve doeleinden in gecontroleerde omgevingen. Ongeautoriseerd gebruik is strikt verboden en kan leiden tot juridische actie.
```

Dit README-bestand bevat alle gevraagde elementen met:

- Duidelijke installatie-instructies
- Uitgebreide moduleverantwoording
- Juridische disclaimer
- Technische achtergrond
- Probleemoplossingsgids
- Moderne opmaak voor GitHub



[^1]: paste.txt

[^2]: paste-2.txt

[^3]: paste-3.txt

[^4]: https://thepythoncode.com/article/building-network-scanner-using-scapy

[^5]: https://awjunaid.com/networking/ssh-server-and-client-to-run-remote-commands-with-paramiko/

[^6]: https://docs.python.org/3/library/asyncio-protocol.html

[^7]: https://superfastpython.com/threadpoolexecutor-vs-processpoolexecutor/

[^8]: https://pypi.org/project/colorama/

[^9]: https://www.fernandomc.com/posts/using-requests-to-get-and-post/

[^10]: https://codecut.ai/comparing-python-command-line-interface-tools-argparse-click-and-typer/

[^11]: https://www.pythonsnacks.com/p/paths-in-python-comparing-os-path-and-pathlib

[^12]: https://www.zenrows.com/blog/urllib-vs-urllib3-vs-requests

[^13]: https://proxiesapi.com/articles/is-lxml-better-than-beautifulsoup

[^14]: https://usavps.com/blog/74174/

[^15]: https://stackoverflow.com/questions/59589190/python-arp-scanner

[^16]: https://www.codu.co/articles/adding-colour-to-python-code-lbai_0u7

[^17]: https://scapy.readthedocs.io/en/latest/usage.html

[^18]: https://cs10.org/bjc-r/cur/programming/libraries/colorama/intro.html?topic=berkeley_bjc%2Flibraries%2Flibraries.topic\&course=cs10_fa20.html\&novideo\&noreading\&noassignment

[^19]: https://www.youtube.com/watch?v=l4CoCIIlCas

[^20]: https://www.clouddefense.ai/code/python/example/colorama

[^21]: https://null-byte.wonderhowto.com/how-to/build-arp-scanner-using-scapy-and-python-0162731/

[^22]: https://dev.to/visheshdvivedi/get-colored-console-output-in-python-using-colorama-4gci

[^23]: https://www.codu.co/articles/adding-colour-to-python-code-lbai_0u7

[^24]: https://dev.to/zeyu2001/network-scanning-with-scapy-in-python-3off

[^25]: https://docs.paramiko.org/en/stable/api/client.html

[^26]: https://docs.python.org/3/library/asyncio-stream.html

[^27]: https://stackoverflow.com/questions/51828790/what-is-the-difference-between-processpoolexecutor-and-threadpoolexecutor

[^28]: https://dev.to/visheshdvivedi/get-colored-console-output-in-python-using-colorama-4gci

[^29]: https://python-automation-book.readthedocs.io/en/1.0/11_paramiko/01_intro.html

[^30]: https://gist.github.com/dbehnke/9627160

[^31]: https://superfastpython.com/multiprocessing-pool-vs-processpoolexecutor/

[^32]: https://cs10.org/bjc-r/cur/programming/libraries/colorama/intro.html?topic=berkeley_bjc%2Flibraries%2Flibraries.topic\&course=cs10_fa20.html\&novideo\&noreading\&noassignment

[^33]: https://www.linode.com/docs/guides/use-paramiko-python-to-ssh-into-a-server/

[^34]: https://stackoverflow.com/questions/76710341/async-tcp-writer-close-to-avoid-resource-leaks

[^35]: https://pypi.org/project/winregistry/

[^36]: https://github.com/tartley/colorama

[^37]: https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3

[^38]: https://www.pythonsnacks.com/p/click-vs-argparse-python

[^39]: https://builtin.com/software-engineering-perspectives/python-pathlib

[^40]: https://how.dev/answers/what-is-winregcreatekey-in-python

[^41]: https://www.youtube.com/watch?v=GPBUFMOXI6M

[^42]: https://www.scraperapi.com/web-scraping/beautiful-soup/

[^43]: https://blog.mindmeldwithminesh.com/mastering-cli-development-in-python-a-comparison-of-click-and-its-competitors-97c62c5218f4

[^44]: https://www.reddit.com/r/Python/comments/l45ojr/ospath_vs_pathlib/

[^45]: https://pabitrap.wordpress.com/2016/09/08/accessing-windows-registry-using-pythons-winreg-module/

[^46]: https://www.csnewbs.com/python-5d-colorama

[^47]: https://proxiesapi.com/articles/python-requests-vs-urllib

[^48]: https://stackoverflow.com/questions/4967103/beautifulsoup-and-lxml-html-what-to-prefer

[^49]: https://pymotw.com/3/urllib.robotparser/index.html

[^50]: https://blog.heycoach.in/requests-vs-urllib-in-python/

[^51]: https://lxml.de/2.1/elementsoup.html

[^52]: https://docs.python.org/es/3.5/library/urllib.robotparser.html

[^53]: https://docs.python.org/3/library/urllib.request.html

[^54]: https://lxml.de/elementsoup.html

[^55]: https://omz-software.com/pythonista/docs-3.4/py3/library/urllib.robotparser.html

[^56]: https://www.linkedin.com/pulse/comparative-guide-argparse-click-typer-python-parsing-luís-condados-mrzjf

[^57]: https://www.reddit.com/r/Python/comments/4wl029/requests_vs_urllib_what_problem_does_it_solve/

[^58]: https://stackoverflow.com/questions/2018026/what-are-the-differences-between-the-urllib-urllib2-urllib3-and-requests-modul

[^59]: https://www.zenrows.com/blog/urllib3-vs-requests

[^60]: https://proxiesapi.com/articles/simplifying-http-requests-in-python-urllib-vs-requests

# saca
