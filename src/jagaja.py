from typing import Tuple
from bitarray import bitarray

class Jagaja:
    """Tükeldab sisendbaidid 3 osaks, üks tükk iga värvikanali jaoks. Punane kanal saab 2-bitise tüki, sinine ja roheline 3-bitised tükid, niimoodi saab ühte pikslisse kodeerida terve baidi. Tükke saab ühildada algsete värvikanali väärtustega & operatsiooni abil."""

    # TODO: toeta erinevaid sisendi variante?
    def __init__(self, sisend: bytes):
        self.baidid = bitarray()
        self.baidid.frombytes(sisend)
        self.indeks = 0
        self.pikkus = len(self.baidid)

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[bitarray, bitarray, bitarray]:
        if self.indeks >= self.pikkus:
            raise StopIteration

        algus = self.indeks
        lõpp = algus + 8
        bait = self.baidid[algus:lõpp]
        
        punane = bait[0:2]
        roheline = bait[2:5]
        sinine = bait[5:8]

        return (punane, roheline, sinine)
