from jagaja import Jagaja
from bitarray import bitarray
from bitimanip import bitideks

MAX_PLOKI_PIKKUS = 2 ** (4 * 8)

class Plokk:
    def __init__(self, kontroll_summa: int, järjenumber: int, plokke_kokku: int, info: bytes):
        päis = bitarray()
        päis += bitideks(kontroll_summa, 16)
        päis += bitideks(järjenumber)
        päis += bitideks(plokke_kokku)

        self.__päis = Jagaja(päis)
        self.__info = Jagaja(info)

    def pikkus(self) -> int:
        """Info pikkus koos päise pikkusega"""

        PÄISE_PIKKUS = 8
        
        return self.__info.pikkus + PÄISE_PIKKUS

def arvuta_kontrollsumma(baidid: bytes) -> int:
    """Arvutab antud baitide kontrollsumma 2 baidi suuruse numbrina"""

    max_suurus = 0xFFFF

    summa = sum(baidid)

    return summa % max_suurus
