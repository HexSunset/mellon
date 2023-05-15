from PIL import Image
from typing import Tuple
from bitarray import bitarray
from bitimanip import bitideks, bitidest, joonda_bitid
from plokk import Plokk, arvuta_kontrollsumma

class DekodeerimisViga(Exception):
    pass

class PildiHaldur:
    __pildi_nimi: str
    __pilt: Image.Image

    # piksli indeks
    __indeks: int

    def __init__(self, pildi_nimi: str):
        self.__pildi_nimi = pildi_nimi
        self.__pilt = Image.open(pildi_nimi)
        self.__indeks = 0

    def salvesta_pilt(self, nimi: str):
        self.__pilt.save(nimi)

    def kodeeri_bait(self, sisend: bitarray):
        """Kodeeri üks bait ühte pikslisse. Suurendab indeksit."""

        algne_px = self.get_piksel()

        punased_bitid = joonda_bitid(sisend[0:2])
        rohelised_bitid = joonda_bitid(sisend[2:5])
        sinised_bitid = joonda_bitid(sisend[5:8])

        m_punane = bitideks(algne_px[0])
        m_punane[-2:] = False
        m_roheline = bitideks(algne_px[1])
        m_roheline[-3:] = False
        m_sinine = bitideks(algne_px[2])
        m_sinine[-3:] = False

        uus_punane = bitidest(punased_bitid | m_punane)
        uus_roheline = bitidest(rohelised_bitid | m_roheline)
        uus_sinine = bitidest(sinised_bitid | m_sinine)

        uus_px = (uus_punane, uus_roheline, uus_sinine)

        self.set_piksel(uus_px)
        self.__indeks += 1

    def kodeeri_baidid(self, baidid: bytes):
        for bait in baidid:
            self.kodeeri_bait(bitideks(bait))

    def dekodeeri_bait(self) -> bitarray:
        """Dekodeeri üks bait. Suurendab indeksit"""
        
        piksel = self.get_piksel()

        punane = bitideks(piksel[0])
        roheline = bitideks(piksel[1])
        sinine = bitideks(piksel[2])

        bait = bitarray()
        bait += punane[-2:]
        bait += roheline[-3:]
        bait += sinine[-3:]

        self.__indeks += 1

        return bait

    def dekodeeri_baidid(self, baitide_arv: int) -> bitarray:
        baidid = bitarray()
        for _ in range(baitide_arv):
            baidid += self.dekodeeri_bait()

        return baidid

    def kodeeri_plokk(self, plokk: Plokk):
        for bait in plokk.baidid():
            bait = bitideks(bait)
            self.kodeeri_bait(bait)

    def dekodeeri_plokk(self):
        # Päis
        kontroll_summa = bitidest(self.dekodeeri_baidid(2))
        järjenumber = bitidest(self.dekodeeri_bait())
        plokke_kokku = bitidest(self.dekodeeri_bait())
        pikkus = bitidest(self.dekodeeri_baidid(4))
        if self.get_pikslite_arv() - self.get_lineaarne_indeks() < pikkus:
            print(f"indeks: {self.get_lineaarne_indeks()}")
            raise DekodeerimisViga("Kodeeritud info pikkus on suurem kui faili maht.") 

        # Sisu
        baidid = self.dekodeeri_baidid(pikkus).tobytes()

        if kontroll_summa != arvuta_kontrollsumma(baidid):
            raise DekodeerimisViga("Dekodeeritud kontrollsumma ja arvutatud kontrollsumma ei klapi")
        
        väljund = Plokk(järjenumber, plokke_kokku, baidid)


        return väljund

    def get_indeks(self):
        x = self.__indeks % self.get_laius()
        y = self.__indeks // self.get_kõrgus()
        return (x, y)

    def get_lineaarne_indeks(self):
        return self.__indeks

    def set_indeks(self, indeks: int):
        if indeks < 0 or indeks >= self.get_pikslite_arv():
            raise ValueError(f"Indeks peab olema vahemikus [0; pikslite_arv).")

        self.__indeks = indeks

    def get_kõrgus(self) -> int:
        return self.__pilt.size[1]
 
    def get_laius(self) -> int:
        return self.__pilt.size[0]

    # Pikslite arv on võrdne mahuga baitides, sest me mahutame igasse pikslisse ühe baidi
    def get_pikslite_arv(self) -> int:
        return self.get_laius() * self.get_kõrgus()

    def set_piksel(self, piksel: Tuple[int, int, int]):
        self.__pilt.putpixel(self.get_indeks(), piksel)

    def get_piksel(self) -> Tuple[int, int, int]:
        return self.__pilt.getpixel(self.get_indeks())
