# Egento-pa-3-projekt

Třetí projekt na Python Akademii od Engeta

## Popis projektu

Tento projekt slouží k extrahování výsledků z parlamentních voleb 2017. Odkaz k prohlédnutí najdete [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

## Instalace knihoven

Knihovny, které jsou použity v kódu jsou uložené v souboru `requirements.txt`. Pro instalaci doporučuji použít nové
virtuální prostředí a s nainstalovaným manažerem spustit následovně:

```bash
pip -- version                    # overim verzi manageru
pip install -r requirements.txt   # nainstalujeme knihovny
```

## Spuštění projektu

Spuštění projektu `election-scraper.py` v rámci přík. řádku požaduje dva povinné argumenty.

```bash
python election-scraper <odkaz-uzemniho-celku> <vysledny soubor>
```

Následně se vám stáhnou výsledky jako soubor s příponou `.csv`.

## Ukázka projektu

Výsledky hlasování pro okres Prostějov:

1. argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`
2. argument: `vysledky_prostejov`

Spuštění programu:

```bash
python election-scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov"
```

Průběh stahování:

```bash
STAHUJI DATA Z VYBRANEHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADAM DO SOUBORU: vysledky_prostejov.csv
UKONCUJI: election-scraper
```

Částečný výstup:

```
code,location,registered,envelopes,valid,...
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
...
```