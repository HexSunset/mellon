from PIL import Image
import math
from typing import Tuple
from bitarray import bitarray

def uus_piksel(algne_px: Tuple[int, int, int], sisend: bitarray, kanal: int):
    if kanal not in range(0, 3):
        raise ValueError("Kanal peab olema vahemikus range(0, 3)")

    algne = bitideks(algne_px[kanal])
    uus = algne
    uus[-2:] = False # Viimased kaks bitti nulliks, et sinna sisend asendada
    uus |= sisend
    # Peame alguses looma selle listina, sest tupleit pole võimalik peale loomist muuta
    uus_px = [algne_px[0], algne_px[1], algne_px[2]]
    uus_px[kanal] = bitidest(uus)
    return tuple(uus_px)

def võta_bitid(piksel: Tuple[int, int, int], kanal: int, bitide_arv=2) -> bitarray:
    a = bitideks(piksel[kanal])
    #mask = bitarray("11111111") >> (8 - bitide_arv)
    mask = bitarray("00000011")

    väljund = (a & mask)[-2:]

    return väljund

def bitideks(number: int, pikkus=8) -> bitarray:
    """Muudab numbri bitarray objektiks, kõige väiksema väärtusega bitt kõige paremal."""

    biti_string = (bin(number)[2:]).rjust(pikkus, '0')
    väljund = bitarray(biti_string)
    return väljund

def bitidest(bitid: bitarray) -> int:
    """Bitarray objekt int objektiks. Kõige väiksema väärtusega bitt kõige paremal."""

    return int(bitid.to01(), 2)

class PildiMuutja:
    """Pildi muutmise algklass, implementeerib põhifunktsioonid"""
    
    def __init__(self, pildi_nimi: str):
        self.pildi_nimi = pildi_nimi
        self.fail = Image.open(pildi_nimi)

        if self.fail.mode not in ["RGB", "RGBA"]:
            raise ValueError(f"Programm toetab ainult pilte, mis on RGB või RGBA formaadis, antud pilt on: {self.fail.mode}")

        if self.fail.format not in ["PNG"]:
            raise ValueError(f"Programm toetab hetkel ainult PNG faile.")

        # pikslite arv
        self.maht = self.fail.width * self.fail.height
        
        # Igal pikslil kolm kasutatavat kanalit
        self.maht *= 3

        # See indeks sisaldab nii piksli indeksit kui ka värvikanalit
        # Värvikanali kätte saamiseks: self.indeks % 3
        # Piksli indeksi kätte saamiseks: math.floor(self.indeks / 3)
        self.indeks = 0

    # Destruktor
    def __del__(self):
        self.fail.close()

    def set_piksel(self, piksel: Tuple[int, int, int]):
        xy = self.piksli_indeks()
        self.fail.putpixel(xy, piksel)

    def get_piksel(self) -> Tuple[int, int, int]:
        xy = self.piksli_indeks()
        return self.fail.getpixel(xy)

    def piksli_indeks(self) -> Tuple[int, int]:
        lineaarne_indeks = math.floor(self.indeks / 3)
        y = math.floor(lineaarne_indeks / self.fail.width)
        x = lineaarne_indeks % self.fail.width
        return (x, y)

    def piksli_kanal(self) -> int:
        return self.indeks % 3
