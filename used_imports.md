### 📦 Standaard Python Modules

```python
# Algemeen
import os
import sys
import time
import re
import random
import json
import logging
import signal
import fnmatch
import platform
import argparse
import glob
import base64
import datetime
import warnings
from typing import List, Tuple, Dict, Optional

# Netwerk
import socket
import subprocess
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser
from http.client import HTTPResponse  # Indirect via requests

# Multi-threading/processing
import threading
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Systeemintegratie
import ctypes
import winreg  # Alleen op Windows

# Bestandspaden
from pathlib import Path

# Kleurgebruik (hoofdmenu)
from colorama import init, Fore, Back, Style
```


---

### 📡 Externe Packages (via pip)

```python
# Packet manipulation
from scapy.all import ARP, Ether, srp, get_working_ifaces

# SSH bruteforce
import paramiko

# Web scraping
import requests
from bs4 import BeautifulSoup

# Geavanceerde port scanning
import python-nmap  # Optioneel, gebruikt in ARP scanner
```


---

### 🔄 Afhankelijkheden per Script

#### 1. DDoS Simulator (`ddos_attack.py`)

```python
# Vereist
import colorama
```


#### 2. MAC Spoofer (`mac_spoof.py`)

```python
# Vereist (Windows)
import winreg  # Standaard op Windows
import ctypes   # Standaard op Windows
```


#### 3. Web Scraper (`web_scraper.py`)

```python
# Vereist
pip install requests beautifulsoup4
```


#### 4. ARP Scanner (`arp_scanner.py`)

```python
# Vereist
pip install scapy python-nmap
```


#### 5. Hoofdmenu (`main.py`)

```python
# Vereist
pip install colorama
```


---

### 📋 `requirements.txt`

```txt
# Basis
colorama==0.4.6
scapy==2.5.0
paramiko==3.4.0
requests==2.31.0
beautifulsoup4==4.12.0

# Optioneel voor geavanceerde features
python-nmap==0.7.1
```


---

### 🛠️ Installatie

```bash
# Installeer alle dependencies
pip install -r requirements.txt

# Windows specifiek (voor MAC Spoofer):
pip install pywin32
```


---

### 💡 Belangrijke Notities

1. **Windows-afhankelijkheden**
    - `winreg` en `ctypes` zijn standaard aanwezig
    - Voor admin-rechten: Draai scripts als Administrator
2. **Linux/Mac compatibiliteit**
    - `winreg` wordt automatisch overgeslagen
    - Gebruik `sudo` voor netwerkoperaties
3. **Performantie**
    - Scapy vereist root/admin-rechten voor raw socket toegang
    - Paramiko werkt het beste met Python 3.8+
