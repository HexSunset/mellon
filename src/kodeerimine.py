from plokkide_haldaja import PlokkideHaldaja
from pilt import PildiHaldaja, DekodeerimisViga
from failid import *

def dekodeeri_seifidest(seifi_failid: list[str], väljund_fail: str, kanal=None):
    plokid = []
    plokkide_arv = 0

    for seifi_nimi in seifi_failid:
        seifi_haldaja = PildiHaldaja(seifi_nimi)
        print(f"Seif {seifi_nimi}:")
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

    if len(plokid) == 0:
        raise DekodeerimisViga(f"Seifidest ei leitud ühtegi kodeeritud plokki.")

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

def kodeeri_seifidesse(seifi_failid: list[str], saladused: list[str], seifide_uus_kaust: str):
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
        seifi_nimi = os.path.basename(seifi_haldaja.get_faili_nimi())
        if not (os.path.exists(seifide_uus_kaust) and os.path.isdir(seifide_uus_kaust)):
            os.mkdir(seifide_uus_kaust)

        uus_nimi = Path(seifide_uus_kaust, seifi_nimi)
        seifi_haldaja.salvesta_pilt(str(uus_nimi))

    del saladuse_haldaja
    print(f"Kodeeritud: {summa} baiti.")
    print(f"Kodeerimine tehtud!")
