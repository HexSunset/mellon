from io import BytesIO
from typing import Dict, Tuple
from plokk import Plokk, MAX_PLOKI_PIKKUS
from pilt import PildiHaldaja
import os

class PlokkideHaldaja:
    def __init__(self, saladuse_fail: str):
        self.__faili_nimi = saladuse_fail
        with open(saladuse_fail, "rb") as f:
            salajased_baidid = f.read()
            self.saladuse_pikkus = len(salajased_baidid)
            self.saladus = BytesIO(salajased_baidid)

    def __del__(self):
        # Me tohime seda teha, sest saladuse fail on alati meie poolt enne loodud arhiiv.
        os.remove(self.__faili_nimi)

    def faili_nimi(self) -> str:
        return self.__faili_nimi

    def jaota_saladus_seifide_vahel(self, seifi_haldajad: list[PildiHaldaja]) -> list[Tuple[PildiHaldaja, list[Plokk]]]:
        seifi_haldajad.sort(key=lambda x: x.get_pikslite_arv())
        seifide_mahud = [seif.get_pikslite_arv() for seif in seifi_haldajad]
        if sum(seifide_mahud) < self.saladuse_pikkus:
            raise ValueError(f"Antud seif-failide kogumaht on: {sum(seifide_mahud)} baiti, salajaste failide suurus on {self.saladuse_pikkus} baiti.")
        saladuse_indeks = 0

        # Ilma päiseta
        võrdse_ploki_pikkus = (self.saladuse_pikkus // len(seifi_haldajad)) - 8

        plokid: list[Tuple[PildiHaldaja, list[Plokk]]] = list()
        for seif in seifi_haldajad:
            plokid.append((seif, list()))

        plokkide_arv = 0
            
        while saladuse_indeks < self.saladuse_pikkus:
            for (i, maht) in enumerate(seifide_mahud):
                baitide_arv = min(MAX_PLOKI_PIKKUS - 8, võrdse_ploki_pikkus, maht - 8)
                baidid = self.saladus.read(baitide_arv)
                if len(baidid) == 0:
                    break
                saladuse_indeks += len(baidid)
                järg = plokkide_arv + 1
                plokk = Plokk(järg, plokkide_arv, baidid)
                plokkide_arv += 1

                seifide_mahud[i] -= len(baidid)
                plokid[i][1].append(plokk)
                #print(f"Uus plokk: {plokid[i][0].get_faili_nimi()}, ploki suurus: {plokk.sisu_pikkus()}")
        #print(f"plokke_kokku: {plokkide_arv}")
        for (seif, seifi_plokid) in plokid:
            for plokk in seifi_plokid:
                plokk.set_plokkide_arv(plokkide_arv)

        return plokid
