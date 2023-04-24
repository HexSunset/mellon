from typing import Tuple
from bitarray import bitarray

def bitideks(number: int) -> bitarray:
    """Muudab numbri bitarray objektiks, kõige väiksema väärtusega bitt kõige paremal."""

    biti_string = (bin(number)[2:]).rjust(8, '0')
    väljund = bitarray(biti_string)
    return väljund

def bitidest(bitid: bitarray) -> int:
    """Bitarray objekt int objektiks. Kõige väiksema väärtusega bitt kõige paremal."""

    return int(bitid.to01(), 2)

def uus_piksel(algne_px: Tuple[int, int, int], sisend: bitarray, kanal: int):
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
