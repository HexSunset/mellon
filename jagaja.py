from bitarray import bitarray

class Jagaja:
    # TODO: toeta erinevaid sisendi variante?
    def __init__(self, sisend: bytes, tüki_suurus=2):
        self.tüki_suurus: int = tüki_suurus
        self.baidid = bitarray()
        self.baidid.frombytes(sisend)
        self.indeks = 0
        self.pikkus = len(self.baidid)
        self.tükkide_arv = self.pikkus / self.tüki_suurus

    def __iter__(self):
        return self

    def __next__(self):
        if not self.indeks < self.pikkus:
            raise StopIteration

        algus = self.indeks
        lõpp = self.indeks + self.tüki_suurus
        tükk = self.baidid[algus:lõpp]
        tükk = bitarray(tükk.to01().rjust(8, '0'))
        #print(f"algus = {algus}; lõpp = {lõpp}; tükk = {tükk.to01()}")
        self.indeks += self.tüki_suurus
        return tükk
