# Contributing to Domoticz

Bedankt voor je interesse om bij te dragen aan Domoticz! Dit is een fork van het officiële [Domoticz](https://github.com/domoticz/domoticz) project.

## Hoe kan ik bijdragen?

### Bugs rapporteren

1. Controleer eerst of de bug al is gerapporteerd in de [Issues](https://github.com/hmol33/domoticz/issues)
2. Maak een nieuwe issue aan met:
   - Een duidelijke titel
   - Stappen om de bug te reproduceren
   - Verwacht vs. werkelijk gedrag
   - Je OS en architectuur (Linux x86_64, ARM, Windows, macOS)
   - Relevante log-output

### Features voorstellen

1. Open eerst een issue om de feature te bespreken
2. Wacht op goedkeuring voordat je code schrijft
3. Kleine, gefocuste features hebben voorkeur

### Pull Requests

1. Fork de repo en maak een feature-branch aan vanaf `development`
2. Zorg dat de build slaagt op zowel Linux als Windows
3. Test je changes lokaal voordat je pusht
4. Maak een PR aan met een duidelijke beschrijving van wat en waarmee

## Code Stijl

- Volg de bestaande code-stijl in de betreffende module
- Gebruik `clang-format` voor C++ bestanden (zie `clang-format.txt`)
- Voeg comments toe aan nieuwe functies
- Houd commits klein en atomair

## Ontwikkelomgeving

### Linux

```bash
# Clone de repo
git clone https://github.com/hmol33/domoticz.git
cd domoticz

# Installeer dependencies (Debian/Ubuntu)
sudo apt-get install -y build-essential cmake libboost-dev libboost-thread-dev \
  libboost-system-dev libsqlite3-dev subversion curl libcurl4-openssl-dev \
  libusb-dev libudev-dev zlib1g-dev libssl-dev

# Build
cmake -DCMAKE_BUILD_TYPE=Release .
make -j$(nproc)
```

### Windows

Zie de [Windows build instructies](https://wiki.domoticz.com/Build_Domoticz_from_source) op de Domoticz wiki.

## Testen

```bash
# Run de test-suite
cd test
./runtests.sh
```

## Documentatie

- Gebruikersdocumentatie: zie [Wiki](https://wiki.domoticz.com/)
- Beveiliging: zie [SECURITY.md](SECURITY.md) en [SECURITY_SETUP.md](SECURITY_SETUP.md)
- Installatie: zie [INSTALL.md](INSTALL.md)

## Licentie

Door bij te dragen ga je akkoord dat je bijdragen onder de GNU GPL-licentie worden uitgebracht (zie [License.txt](License.txt)).
