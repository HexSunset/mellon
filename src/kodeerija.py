from jagaja import Jagaja
from funktsioonid import *
from pildi_muutja import PildiMuutja

class Kodeerija(PildiMuutja):
    """Pildimuutja alamklass, kodeerib binaarse info faili."""

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
