from plokk import Plokk
from pilt import PildiHaldaja
from bitimanip import bitideks
from bitarray import bitarray
import sys

def main():
    saladus = sys.argv[1]
    seif = sys.argv[2]
    seifi_nimi = sys.argv[3]
    
    baidid = None
    with open(saladus, "rb") as f:
        baidid = f.read()

    salajane_plokk = Plokk(1, 1, baidid)

    seifi_haldaja = PildiHaldaja(seif)
    seifi_haldaja.kodeeri_plokk(salajane_plokk)
    seifi_haldaja.salvesta_pilt(seifi_nimi)

    seifi_avaja = PildiHaldaja(seifi_nimi)
    plokk = seifi_avaja.dekodeeri_plokk()
    print(f"dekodeeritud:")
    print(f"\tkontrollsumma: {plokk.kontroll_summa()}")
    print(f"\tploki_number: {plokk.järjenumber()[0]}/{plokk.järjenumber()[1]}")
    print(f"\tsisu_pikkus: {plokk.sisu_pikkus()}")
    print(f"\tploki_sisu:")
    for bait in plokk.sisu_baidid():
        print(f"\t\t{bitideks(bait)}")

main()
