from jagaja import Jagaja
from lihtnekooder import LihtneKooder
from lihtnedekooder import LihtneDekooder
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("salajane_fail", type=str, help="salajane fail, mille sisu peidetakse pilti")
arg_parser.add_argument("sisend_pilt", type=str, help="pilt, millesse peidetakse info")
arg_parser.add_argument("väljund_pilt", type=str, help="uus nimi, millena infot sisaldav pilt salvestatakse")
args = arg_parser.parse_args()
saladus = open(args.salajane_fail, "rb").read()
sisend_pilt: str = args.sisend_pilt
väljund_pilt: str = args.väljund_pilt

print(f"sisend: {saladus}")
kooder = LihtneKooder(sisend_pilt, väljund_pilt)
sisend = Jagaja(saladus)
kooder.kodeeri_otse(sisend)
del kooder

dekooder = LihtneDekooder(väljund_pilt)
väljund = dekooder.dekodeeri_otse()
del dekooder

print(f"väljund: {väljund}")
