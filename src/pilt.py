from PIL import Image
from typing import Tuple
from bitarray import bitarray
from bitimanip import bitideks, bitidest
import math

class PildiHaldur:
    __faili_nimi: str
    __fail: Image.Image

    # piksli indeks
    __indeks: int

    def __init__(self, faili_nimi: str):
        self.__faili_nimi = faili_nimi
        self.__fail = Image.open(faili_nimi)
        self.__indeks = 0

    def peida_tükid(self, sisend: Tuple[bitarray, bitarray, bitarray]):
        """Peida Jagaja poolt tagastatud tükid pikslisse"""

        algne_px = self.get_piksel()

        uus_punane = sisend[0] & algne_px[0]
        uus_roheline = sisend[1] & algne_px[1]
        uus_sinine = sisend[2] & algne_px[2]
        
        uus_px = (uus_punane, uus_roheline, uus_sinine)

        self.set_piksel(uus_px)
        self.__indeks += 1

    def get_indeks(self):
        return self.__indeks

    def get_kõrgus(self) -> int:
        return self.__fail.size[1]

    def get_laius(self) -> int:
        return self.__fail.size[0]

    # Pikslite arv on võrdne mahuga baitides, sest me mahutame igasse pikslisse ühe baidi
    def get_pikslite_arv(self) -> int:
        return self.get_laius() * self.get_kõrgus

    def set_piksel(self, piksel: Tuple[int, int, int]):
        self.__fail.putpixel(self.__indeks, piksel)

    def get_piksel(self) -> Tuple[int, int, int]:
        return self.__fail.getpixel(self.__indeks)
