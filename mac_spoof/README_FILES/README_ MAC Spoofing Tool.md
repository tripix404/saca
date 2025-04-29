# README: MAC Spoofing Tool

## Overzicht

Deze MAC spoofing tool is een cross-platform Python-script dat je in staat stelt om MAC-adressen van netwerkinterfaces te wijzigen op zowel Windows als Linux systemen. De tool is ontwikkeld als onderdeel van een cybersecurity toolkit voor de opleiding cybersecurity bij HoWest in Brugge.

## Functionaliteiten

- **Cross-platform compatibiliteit**: Werkt op zowel Windows als Linux
- **Automatische besturingssysteemdetectie**: Past automatisch de juiste methodes toe
- **Willekeurige MAC-adres generatie**: Genereert geldige MAC-adressen volgens IEEE-standaarden
- **Interactieve interface**: Toont beschikbare netwerkadapters en laat gebruiker kiezen
- **Verificatie**: Controleert of de MAC-adres wijziging succesvol was
- **Robuuste foutafhandeling**: Vangt fouten op en toont informatieve berichten
- **Verhoogde rechten controle**: Controleert of het script met admin/root rechten wordt uitgevoerd


## Technische keuzes

### Gebruikte modules

- **subprocess**: Voor het uitvoeren van systeemcommando's
- **random**: Voor het genereren van willekeurige MAC-adressen
- **platform**: Voor detectie van het besturingssysteem
- **argparse**: Voor het verwerken van command-line argumenten
- **re**: Voor reguliere expressies bij het parsen van commando-output
- **os, sys**: Voor systeeminteracties en padmanipulatie
- **ctypes**: Voor administratorrechtencontrole op Windows
- **time**: Voor wachttijden tussen commando's


### Implementatiedetails

#### Windows-specifiek

- **netsh en registry**: Twee methodes voor MAC-adres wijziging voor maximale compatibiliteit
- **wmic queries**: Voor het ophalen van netwerkadapter informatie
- **Fallback mechanisme**: Als één methode faalt, wordt automatisch een andere geprobeerd


#### Linux-specifiek

- **ip commando's**: Moderne vervanging voor ifconfig
- **Directe MAC-adres wijziging**: Via ip link commando's


#### Algemene verbeteringen

- **Centrale run_command functie**: Voor consistente foutafhandeling
- **Meerdere methodes voor adapter-detectie**: Voor betere betrouwbaarheid
- **Emoji's in output**: Voor betere leesbaarheid en gebruikerservaring


## Voorbeeldcommando's

### Basis gebruik

```bash
# Toon beschikbare interfaces en kies interactief
python mac_spoof.py

# Wijzig MAC-adres van specifieke interface
python mac_spoof.py -i eth0

# Wijzig naar specifiek MAC-adres
python mac_spoof.py -i eth0 -m 00:11:22:33:44:55
```


### Alle beschikbare opties

```bash
# Toon alle beschikbare interfaces
python mac_spoof.py -l

# Wijzig MAC-adres van Wi-Fi adapter naar willekeurig adres
python mac_spoof.py -i "Wi-Fi"

# Wijzig MAC-adres van eth0 naar specifiek adres
python mac_spoof.py -i eth0 -m aa:bb:cc:dd:ee:ff
```


## Argumenten

| Argument | Beschrijving | Voorbeeld |
| :-- | :-- | :-- |
| `-i`, `--interface` | Netwerkinterface om te wijzigen | `-i eth0` |
| `-m`, `--mac` | Nieuw MAC-adres (willekeurig indien niet opgegeven) | `-m 00:11:22:33:44:55` |
| `-l`, `--list` | Toon beschikbare interfaces | `-l` |

## Vereisten

- Python 3.6 of hoger
- Administratorrechten (Windows) of root-rechten (Linux)


## Veiligheidsoverwegingen

- Het wijzigen van MAC-adressen kan netwerkverbindingen verstoren
- Sommige netwerken blokkeren apparaten met onbekende MAC-adressen
- Het script vereist verhoogde rechten om systeeminstellingen te wijzigen
- MAC spoofing kan in sommige jurisdicties onderhevig zijn aan wettelijke beperkingen


## Gebruik in educatieve context

Deze tool is ontwikkeld voor educatieve doeleinden in het kader van de cybersecurity opleiding. Gebruik deze tool alleen in gecontroleerde omgevingen en met toestemming van de netwerkbeheerder.

<div>⁂</div>

[^1]: https://pplx-res.cloudinary.com/image/upload/v1744799857/user_uploads/kXPHFaTnaHUEUHV/image.jpg

[^2]: https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/56115639/4291361a-8969-49fa-a300-67d1ff4fc15c/paste-2.txt

