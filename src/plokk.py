from bitarray import bitarray
from bitimanip import bitideks
from typing import Tuple

BAIT = 8
MAX_PLOKI_PIKKUS = 2 ** (4 * 8)
PÄISE_PIKKUS_BAITIDES = 8

class Plokk:
    def __init__(self, järjenumber: int, plokke_kokku: int, baidid: bytes):
        if len(baidid) > MAX_PLOKI_PIKKUS:
            raise ValueError(f"Maksimaalne baitide arv plokis on: {MAX_PLOKI_PIKKUS}, funktsioon sai {len(baidid)} baiti.")
        kontroll_summa = arvuta_kontrollsumma(baidid)
        self.__kontroll_summa = kontroll_summa
        self.__järjenumber = järjenumber
        self.__plokke_kokku = plokke_kokku
        self.__sisu_pikkus = len(baidid)
        self.__sisu = baidid

    def kontroll_summa(self) -> int:
        return self.__kontroll_summa

    def järjenumber(self) -> int:
        return self.__järjenumber

    def plokkide_arv(self) -> int:
        return self.__plokke_kokku

    def set_plokkide_arv(self, num: int):
        self.__plokke_kokku = num

    def sisu_pikkus(self) -> int:
        return self.__sisu_pikkus

    def kogu_pikkus(self) -> int:
        """Terve ploki pikkus baitides."""

        return self.sisu_pikkus() + PÄISE_PIKKUS_BAITIDES

    def baidid(self) -> bytes:
        kodeeritud = bitarray()
        kodeeritud += bitideks(self.__kontroll_summa, 2 * BAIT)
        kodeeritud += bitideks(self.__järjenumber)
        kodeeritud += bitideks(self.__plokke_kokku)
        kodeeritud += bitideks(len(self.__sisu), 4 * BAIT)
        kodeeritud.frombytes(self.__sisu)

        self.__kodeeritud = kodeeritud.tobytes()

        return self.__kodeeritud

    def sisu_baidid(self) -> bytes:
        return self.__sisu

def arvuta_kontrollsumma(baidid: bytes) -> int:
    """Arvutab antud baitide kontrollsumma 2 baidi suuruse numbrina"""

    max_suurus = 0xFFFF

    summa = sum(baidid)

    return summa % max_suurus
