from pathlib import Path
import zipfile
import bz2
import datetime
import os

def lühenda_faili_nimed(failid: list[str]) -> list[str]:
    if len(failid) == 1:
        return [os.path.basename(failid[0])]
    ühine_nimi = os.path.commonprefix(failid)
    return [fail[len(ühine_nimi):] for fail in failid]

def loo_arhiiv(failid: list[str]) -> Path:
    lühendatud_failid = lühenda_faili_nimed(failid)
    arhiivi_nimi = "MELLON_ARHIIV_" + datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S") + ".zip"
    with zipfile.ZipFile(arhiivi_nimi, mode="w") as arhiiv:
        for (i, faili_nimi) in enumerate(failid):
            print(f"Lisame {faili_nimi} arhiivi")
            arhiiv.write(faili_nimi, arcname=lühendatud_failid[i])

    with open(arhiivi_nimi, "rb") as arhiivi_fail:
        baidid = arhiivi_fail.read()

    pakitud_baidid = bz2.compress(baidid)

    # Eemaldame ajutise arhiivi faili
    os.remove(arhiivi_nimi)
    pakitud_arhiivi_nimi = arhiivi_nimi + ".bz2"

    with open(pakitud_arhiivi_nimi, "wb") as pakitud_arhiiv:
        pakitud_arhiiv.write(pakitud_baidid)

    return Path(pakitud_arhiivi_nimi)
