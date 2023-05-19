from pathlib import Path
import zipfile
import bz2
import datetime
import os

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
