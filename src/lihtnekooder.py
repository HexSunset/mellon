from jagaja import Jagaja
from pildi_muutja import PildiMuutja, uus_piksel, bitideks, bitidest

class LihtneKooder(PildiMuutja):
    """Pildimuutja alamklass, kodeerib binaarse info faili."""

    def __init__(self, sisend_pilt, väljund_pilt):
        super().__init__(sisend_pilt)
        self.väljundi_nimi = väljund_pilt

    def __del__(self):
        self.fail.save(self.väljundi_nimi)
        self.fail.close()

    # Kodeerib sisendi tükid faili otse, kõige lõppu paneb 0-baidi (b'\x00'), et dekodeerija teaks millal dekodeerimist lõpetada.
    def kodeeri_otse(self, sisend: Jagaja):
        # TODO: korralik mahu arvutamine
        #if not sisend.tükkide_arv <= self.maht - self.indeks:
        #    raise ValueError("Sisend on liiga suur")

        for tükk in sisend:
            kanal = self.piksli_kanal()
            algne_px = self.get_piksel()
            uus_px = uus_piksel(algne_px, tükk, kanal)
            self.set_piksel(uus_px)

            self.indeks += 1

        # Lisame 0-baidi
        for _ in Jagaja(b'\x00'):
            kanal = self.piksli_kanal()
            algne_px = self.get_piksel()
            uus_px = uus_piksel(algne_px, bitideks(0), kanal)
            self.set_piksel(uus_px)

            self.indeks += 1
