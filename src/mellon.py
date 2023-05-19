from plokkide_haldaja import PlokkideHaldaja
from pilt import PildiHaldaja, DekodeerimisViga
from pathlib import Path
import zipfile
import bz2
import datetime
import os
#from bitarray import bitarray
import argparse

def main():
    # Saame argumendid
    parser = argparse.ArgumentParser(
        prog='MELLON',
        description='Mitme failiga korraga töötav steganograafia programm.')
    parser.add_argument('--saladused', nargs='+')
    parser.add_argument('--seifid', nargs='+')
    parser.add_argument('--dekodeeri_faili', nargs='?', default="")
    args = parser.parse_args()

    saladuse_failid = args.saladused
    seifi_failid = args.seifid
    dekodeerimisfail = args.dekodeeri_faili

    if dekodeerimisfail != "":
        dekodeeri_seifidest(seifi_failid, dekodeerimisfail)
    else:
        kodeeri_seifidesse(seifi_failid, saladuse_failid)

def dekodeeri_seifidest(seifi_failid: list[str], väljund_fail: str, kanal=None):
    plokid = []
    plokkide_arv = 0

    for seifi_nimi in seifi_failid:
        seifi_haldaja = PildiHaldaja(seifi_nimi)
        print(f"{seifi_nimi}:")
        while True:
            try:
                uus_plokk = seifi_haldaja.dekodeeri_plokk()

                if plokkide_arv == 0:
                    plokkide_arv = uus_plokk.plokkide_arv()
                else:
                    if uus_plokk.plokkide_arv() != plokkide_arv:
                        raise DekodeerimisViga("Dekodeeritud plokis öeldud plokkide koguarv ei vasta varasemale arvule.")
                print(f"\tDekodeeritud plokk: number={uus_plokk.järjenumber()}, pikkus={uus_plokk.sisu_pikkus()}")
                plokid.append(uus_plokk)

                if len(plokid) == plokkide_arv:
                    break
            except DekodeerimisViga as e:
                if str(e) == "Kodeeritud info pikkus on suurem kui faili maht.":
                    break
                else:
                    raise e

    if len(plokid) != plokkide_arv:
        raise DekodeerimisViga(f"Kõiki plokke ei suudetud dekodeerida. Dekodeeriti: {len(plokid)} plokki, kokku kodeeritud: {plokkide_arv} plokki.")

    plokid.sort(key=lambda x: x.järjenumber())
    baidid = bytearray()
    for plokk in plokid:
        baidid.extend(plokk.sisu_baidid())

    with open(väljund_fail, "wb") as f:
        f.write(baidid)
        print(f"Loodud fail {väljund_fail}")

    return
    
def kodeeri_seifidesse(seifi_failid: list[str], saladused: list[str], kanal=None):
    saladuse_fail = loo_arhiiv(saladused)
    saladuse_haldaja = PlokkideHaldaja(str(saladuse_fail))
    print(f"Saladus: {saladuse_haldaja.faili_nimi()} ({saladuse_haldaja.saladuse_pikkus} baiti)")
    seifi_haldajad = [PildiHaldaja(faili_nimi) for faili_nimi in seifi_failid]

    summa = 0

    for (seifi_haldaja, plokid) in saladuse_haldaja.jaota_saladus_seifide_vahel(seifi_haldajad):
        print(f"{seifi_haldaja.get_faili_nimi()}:")
        print(f"\tSeifis ruumi: {seifi_haldaja.get_pikslite_arv()} baiti")
        for plokk in plokid:
            print(f"\tPlokk: {plokk.sisu_pikkus()} baiti")
            summa += plokk.sisu_pikkus()
            seifi_haldaja.kodeeri_plokk(plokk)
        print(f"\tKokku: {sum([plokk.sisu_pikkus() for plokk in plokid])}")
        seifi_nimi = seifi_haldaja.get_faili_nimi()
        uus_nimi = os.path.dirname(seifi_nimi) + "/saladusega_" + os.path.basename(seifi_nimi)
        seifi_haldaja.salvesta_pilt(uus_nimi)
    print(f"Kodeeritud: {summa} baiti.")

def loo_arhiiv(failid: list[str]) -> Path:
    arhiivi_nimi = "MELLON_ARHIIV_" + datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S") + ".zip"
    with zipfile.ZipFile(arhiivi_nimi, mode="w") as arhiiv:
        for faili_nimi in failid:
            arhiiv.write(faili_nimi)

    with open(arhiivi_nimi, "rb") as arhiivi_fail:
        baidid = arhiivi_fail.read()

    pakitud_baidid = bz2.compress(baidid)
    pakitud_arhiivi_nimi = arhiivi_nimi + ".bz2"

    with open(pakitud_arhiivi_nimi, "wb") as pakitud_arhiiv:
        pakitud_arhiiv.write(pakitud_baidid)

    # Eemaldame ajutise arhiivi faili
    os.remove(arhiivi_nimi)

    return Path(pakitud_arhiivi_nimi)

if __name__ == "__main__":
    main()
