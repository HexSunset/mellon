from bitarray import bitarray
from bitimanip import bitideks
from typing import Tuple

BAIT = 8

class Plokk:
    def __init__(self, järjenumber: int, plokke_kokku: int, baidid: bytes):
        kodeeritud = bitarray()

        kontroll_summa = arvuta_kontrollsumma(baidid)
        self.__kontroll_summa = kontroll_summa
        kodeeritud += bitideks(kontroll_summa, 2 * BAIT)
        kodeeritud += bitideks(järjenumber)
        self.__järjenumber = järjenumber
        kodeeritud += bitideks(plokke_kokku)
        self.__plokke_kokku = plokke_kokku
        kodeeritud += bitideks(len(baidid), 4 * BAIT)
        self.__sisu_pikkus = len(baidid)

        self.__sisu = baidid

        kodeeritud.frombytes(baidid)
        self.__kodeeritud = kodeeritud.tobytes()

    def kontroll_summa(self) -> int:
        return self.__kontroll_summa

    def järjenumber(self) -> Tuple[int, int]:
        return (self.__järjenumber, self.__plokke_kokku)

    def sisu_pikkus(self) -> int:
        return self.__sisu_pikkus

    def kogu_pikkus(self) -> int:
        """Terve ploki pikkus baitides."""

        return len(self.__kodeeritud)

    def baidid(self) -> bytes:
        return self.__kodeeritud

    def sisu_baidid(self) -> bytes:
        return self.__sisu

def arvuta_kontrollsumma(baidid: bytes) -> int:
    """Arvutab antud baitide kontrollsumma 2 baidi suuruse numbrina"""

    max_suurus = 0xFFFF

    summa = sum(baidid)

    return summa % max_suurus
