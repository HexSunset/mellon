from bitarray import bitarray
from pildi_muutja import PildiMuutja, bitideks, bitidest, võta_bitid

class Dekooder(PildiMuutja):
    def dekodeeri_otse(self) -> bytes:
        väljund = bytearray()

        # Võta baite kuni \x00
        while True:
            bait = bitarray()
            for _ in range(4):
                bait += self.get_bitid()


            if bitidest(bait) == 0:
                break

            väljund += bait.tobytes()

        return bytes(väljund)

    # võta self.indeks pikslilt õige arv bitte
    def get_bitid(self, bitide_arv=2) -> bitarray:
        piksel = self.get_piksel()
        kanal = self.piksli_kanal()
        bitid = võta_bitid(piksel, kanal, bitide_arv)

        self.indeks += 1

        return bitid
