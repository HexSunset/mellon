from bitarray import bitarray
from typing import Tuple

def bitideks(number: int, pikkus=8) -> bitarray:
    """Muudab numbri bitarray objektiks, kõige väiksema väärtusega bitt kõige paremal."""

    biti_string = (bin(number)[2:]).rjust(pikkus, '0')
    väljund = bitarray(biti_string)
    return väljund

def bitidest(bitid: bitarray) -> int:
    """Bitarray objekt int objektiks. Kõige väiksema väärtusega bitt kõige paremal."""

    return int(bitid.to01(), 2)

def võta_bitid_pikslilt(piksel: Tuple[int, int, int], kanal: int, bitide_arv=2) -> bitarray:
    if bitide_arv < 0 or bitide_arv > 8:
        raise ValueError("bitide_arv peab olema vahemikus 0..8")
    
    a = bitideks(piksel[kanal])
    mask = bitarray("11111111") >> (8 - bitide_arv)

    väljund = (a & mask)[-2:]

    return väljund

def uus_piksel_algsest(algne_px: Tuple[int, int, int], sisend: bitarray, kanal: int):
    if kanal not in range(0, 3):
        raise ValueError("Kanal peab olema vahemikus range(0, 3)")

    algne = bitideks(algne_px[kanal])
    uus = algne
    uus[-2:] = False # Viimased kaks bitti nulliks, et sinna sisend asendada
    uus |= sisend
    # Peame alguses looma selle listina, sest tupleit pole võimalik peale loomist muuta
    uus_px = [algne_px[0], algne_px[1], algne_px[2]]
    uus_px[kanal] = bitidest(uus)
    return tuple(uus_px)

