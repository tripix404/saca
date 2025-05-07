Belangrijkste verbeteringen:

1. **Geavanceerde logging**:
    - Combineert console output en file logging
    - Duidelijke severity levels (INFO, WARNING, CRITICAL)
2. **Netwerkprestaties**:
    - Asynchrone portscanner met `asyncio`
    - Multi-threaded SSH bruteforce
    - Optimalisaties in ARP-scantijden
3. **Beveiliging**:
    - SSH host key policy met waarschuwingen
    - Wachtwoorden uit extern bestand (`passwords.txt`)
    - Timeout handling in alle netwerkoperaties
4. **Code kwaliteit**:
    - Type hints voor alle functies
    - Uitgebreide foutafhandeling
    - Gestructureerde configuratie

**Benodigde stappen voor gebruik**:

1. Installeer vereisten:
```bash
pip install scapy paramiko
```

2. Maak een `passwords.txt` bestand aan met veelvoorkomende wachtwoorden
3. Voor Linux/macOS:
```bash
sudo python3 toolkit_v2.py
```

4. Voor Windows:
```powershell
python toolkit_v2.py
```

Deze versie bevat alle eerder voorgestelde verbeteringen en voegt extra veiligheids- en prestatieoptimalisaties toe. Wil je specifieke onderdelen verder aanpassen of uitbreiden?

