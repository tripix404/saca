<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# wat voor effect of welke functie hebben de veiligheidsoverwegingen die in de script zijn geïmplementeerd?

De veiligheidsmaatregelen in het aangepaste script hebben **drie kernfuncties** die cruciaal zijn voor ethisch hacken en netwerkbeveiliging:

## 1. Preventie van detectie door beveiligingssystemen

- **Rate limiting** in SSH-bruteforce (`time.sleep(MIN_RATE_LIMIT)`):
Vertraagt aanvallen om IDS/IPS-systemen te omzeilen[^8][^18][^20]
- **Beperkt poortscannen** (`MAX_SCAN_PORTS=15`):
Voorkomt verdachte netwerkactiviteit door scanbereik te limiteren[^5][^14]
- **Multi-threading controle** (`max_workers=3`):
Beperkt parallelle aanvallen om resource-uitputting te voorkomen[^16][^17]


## 2. Beveiliging van scanresultaten

- **Base64-gecodeerde filenamen**:
Beschermt gevoelige data tegen onbevoegde toegang[^13]
- **Geautomatiseerde logging**:
Documenteert alle acties voor auditdoeleinden[^1][^9]
- **Versleutelde JSON-opslag**:
Voorkomt datastructuren met kwetsbare informatie[^3][^15]


## 3. Netwerkintegriteitsbewaking

- **ARP-scan validatie**:
Detecteert rogue devices en MAC-spoofing[^2][^5]
- **Dynamische interface-selectie**:
Voorkomt per ongeluk scannen van gevoelige netwerken[^4][^13]
- **Service-detectie**:
Identificeert ongepatchte services via poortscanning[^7][^9]

**Kritieke impact volgens NIS2-richtlijnen[^11]:**
Deze maatregelen helpen bij compliance door:

- Risico-inventarisatie van netwerkapparaten
- Detectie van onbeheerde IoT-devices
- Preventie van lateral movement door aanvallers

De **timeout-aanpassingen** (van 2 naar 5 seconden) in de ARP-scan verminderen false negatives bij trage netwerken, wat essentieel is voor accurate asset discovery[^6][^14]. De **geïntegreerde waarschuwingen** voor open poort 22 voorkomen onnodige bruteforce-pogingen, wat essentieel is in onderwijsomgevingen met strikte gebruikersbeleiden[^9][^19].

<div style="text-align: center">⁂</div>

[^1]: https://www.security.nl/posting/796407/Network+scanners

[^2]: http://atwork.safeonweb.be/nl/tools-resources/beveilig-uw-netwerk

[^3]: https://www.mitservices.nl/blog/blog-3/waarom-is-een-virusscanner-belangrijk-920

[^4]: https://www.ncsc.nl/wat-kun-je-zelf-doen/weerbaarheid/beschermen/grip-op-security-controls

[^5]: https://anoniem-surfen.nl/netwerk-scanner/

[^6]: https://ant.isi.edu/~johnh/PAPERS/Guo18a.pdf

[^7]: https://www.phoenixnap.nl/woordenlijst/boze-ip-scan

[^8]: https://www.red-button.net/6-tips-for-preventing-ddos-attacks-using-rate-limits/

[^9]: https://id.nl/zekerheid-en-gemak/veilig-online/beveiligingssoftware/houd-je-data-veilig-van-identiteitsbescherming-tot-ransomware

[^10]: https://www.solo.io/topics/rate-limiting

[^11]: https://www.2n.com/nl-NL/blog/de-weg-naar-digitale-veiligheid-een-blik-op-de-nis2-richtlijn-van-de-eu/

[^12]: https://community.cloudflare.com/t/waf-rate-limiting/584771

[^13]: https://atwork.safeonweb.be/sites/default/files/2024-03/Netwerkbeveiligingsbeleid.docx

[^14]: https://pdl.cmu.edu/PDL-FTP/associated/CMU-PDL-05-103.pdf

[^15]: https://validatagroup.com/nl/screening-checks/internet-scan/

[^16]: https://totaluptime.com/kb/how-to-implement-connection-rate-limiting/

[^17]: https://www.haproxy.com/blog/four-examples-of-haproxy-rate-limiting

[^18]: https://www.imperva.com/learn/application-security/rate-limiting/

[^19]: https://learn.snyk.io/lesson/no-rate-limiting/

[^20]: https://www.tencentcloud.com/document/product/1145/55943

