from PIL import Image
from jagaja import Jagaja
from typing import Tuple
from funktsioonid import *
import math

class Kodeerija:
    """Avab pildi ja kodeerib sinna kasutaja poolt antud sisendi(d)"""
    
    def __init__(self, pildi_nimi: str):
        self.pildi_nimi = pildi_nimi
        self.fail = Image.open(pildi_nimi)

        if self.fail.mode not in ["RGB", "RGBA"]:
            raise ValueError(f"Program toetab ainult pilte, mis on RGB või RGBA formaadis, antud pilt on: {self.fail.mode}")

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
        self.fail.save("SALAJANE_" + self.pildi_nimi)
        self.fail.close()
        
    def piksli_indeks(self) -> Tuple[int, int]:
        lineaarne_indeks = math.floor(self.indeks / 3)
        y = math.floor(lineaarne_indeks / self.fail.width)
        x = lineaarne_indeks % self.fail.width
        return (x, y)

    def piksli_kanal(self) -> int:
        return self.indeks % 3

    # Kodeerib sisendi tükid faili otse, kõige lõppu paneb 0-baidi (b'\x00'), et dekodeerija teaks millal dekodeerimist lõpetada.
    def kodeeri_otse(self, sisend: Jagaja):
        # TODO: korralik mahu arvutamine
        #if not sisend.tükkide_arv <= self.maht - self.indeks:
        #    raise ValueError("Sisend on liiga suur")

        for tükk in sisend:
            kanal = self.piksli_kanal()
            algne_px = self.fail.getpixel(self.piksli_indeks())
            uus_px = uus_piksel(algne_px, tükk, kanal)
            self.fail.putpixel(self.piksli_indeks(), uus_px)

            self.indeks += 1

        # Lisame 0-baidi
        for _ in Jagaja(b'\x00'):
            kanal = self.piksli_kanal()
            algne_px = self.fail.getpixel(self.piksli_indeks())
            uus_px = uus_piksel(algne_px, bitideks(0), kanal)
            self.fail.putpixel(self.piksli_indeks(), uus_px)

            self.indeks += 1
