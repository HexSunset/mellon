# Mellon
Pythonis implementeeritud steganograafia programm.

## Vajalikud teegid
- `bitarray` - bitimanipulatsioonid
- `pillow` - pildifailide muutmine

## Kasutamine
```sh
usage: mellon.py [-h] salajane_fail sisend_pilt väljund_pilt

positional arguments:
  salajane_fail  salajane fail, mille sisu peidetakse pilti
  sisend_pilt    pilt, millesse peidetakse info
  väljund_pilt   uus nimi, millena infot sisaldav pilt salvestatakse

options:
  -h, --help     show this help message and exit
```

## Projekti progress
- [x] Naiivne kodeerimine/dekodeerimine
- [x] PNG failid
- [ ] JPEG failid
- [ ] Targem (de)kodeerimisalgoritm
