from plokk import Plokk, PlokkideHaldaja
from pilt import PildiHaldaja
from bitimanip import bitideks
from typing import Tuple
#from bitarray import bitarray
import sys
import argparse

def main():
    # Saame argumendid
    parser = argparse.ArgumentParser(
        prog='MELLON',
        description='Mitme faili põhine steganograafia programm.')
    parser.add_argument('saladuse_fail')
    parser.add_argument('seifi_failid', nargs='+')
    args = parser.parse_args()

    saladuse_fail = args.saladuse_fail
    seifi_failid = args.seifi_failid

    # Teeme asju
    saladuse_haldaja = PlokkideHaldaja(saladuse_fail)
    pildi_haldajad = [PildiHaldaja(nimi) for nimi in seifi_failid]
    pildi_nimed = seifi_failid
    pildi_suurused = [pilt.get_pikslite_arv() for pilt in pildi_haldajad]
    pildid_nimi_suurus = list(zip(pildi_nimed, pildi_suurused))

    plokid_piltides = saladuse_haldaja.jaota_saladus_seifide_vahel(pildid_nimi_suurus)
    for (pildi_nimi, plokk) in plokid_piltides.items():
        indeks = pildi_nimed.index(pildi_nimi)
        haldaja = pildi_haldajad[indeks]
        haldaja.kodeeri_plokk(plokk)
        haldaja.salvesta_pilt("secret_" + pildi_nimi)


if __name__ == "__main__":
    main()
