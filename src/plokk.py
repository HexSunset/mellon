from bitarray import bitarray
from bitimanip import bitideks
from typing import Dict, Tuple
from io import BytesIO

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


class PlokkideHaldaja:
    def __init__(self, saladuse_fail: str):
        with open(saladuse_fail, "rb") as f:
            salajased_baidid = f.read()
            self.saladuse_pikkus = len(salajased_baidid)
            self.saladus = BytesIO(salajased_baidid)

    def jaota_saladus_seifide_vahel(self, pildid: list[Tuple[str, int]]) -> Dict[str, Plokk]:
        """Jaotab saladuse baidid plokkideks, mis mahuvad antud faili mahtude sisse."""

        pildid.sort(key=lambda x: x[1])

        nimed = [pilt[0] for pilt in pildid]
        mahud = [pilt[1] for pilt in pildid]

        plokkide_arv = len(mahud)

        saladuse_pikkus_koos_päisega = 8 * plokkide_arv + self.saladuse_pikkus

        if sum(mahud) < saladuse_pikkus_koos_päisega:
            raise ValueError("Antud failide mahud on liiga väiksed.")

        plokid: Dict[str, Plokk] = dict()

        võrdse_ploki_suurus = saladuse_pikkus_koos_päisega // plokkide_arv
        viimase_ploki_suurus = võrdse_ploki_suurus + (saladuse_pikkus_koos_päisega % võrdse_ploki_suurus)

        ülejääk = 0

        for (järjenumber, maht) in enumerate(mahud):
            järjenumber += 1

            ploki_pikkus = 0

            if võrdse_ploki_suurus == maht:
                ploki_pikkus = võrdse_ploki_suurus
            elif võrdse_ploki_suurus < maht:
                ülejäägist = min(ülejääk, maht - võrdse_ploki_suurus)
                ülejääk -= ülejäägist
                ploki_pikkus = võrdse_ploki_suurus + ülejäägist
            else:
                ploki_pikkus = maht
                ülejäägi_lisa = võrdse_ploki_suurus - maht
                ülejääk += ülejäägi_lisa

            if järjenumber == plokkide_arv:
                # Oleme viimase ploki juures ja loeme nii palju infot kui võimalik.
                info_pikkus = -1
            else:
                # võtame päise suuruse välja
                info_pikkus = ploki_pikkus - 8
            baidid = self.saladus.read(info_pikkus)
            plokk = Plokk(järjenumber, plokkide_arv, baidid)
            faili_nimi = pildid[järjenumber - 1][0]
            plokid[faili_nimi] = plokk

        return plokid
