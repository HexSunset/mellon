from bitarray import bitarray
from typing import Tuple

"""Bittide ja baitidega töötamise abifunktsioonid."""

def bitideks(number: int, pikkus=8) -> bitarray:
    """Muudab numbri bitarray objektiks, kõige väiksema väärtusega bitt kõige paremal."""

    biti_string = (bin(number)[2:]).rjust(pikkus, '0')
    väljund = bitarray(biti_string)
    return väljund

def bitidest(bitid: bitarray) -> int:
    """Bitarray objekt int objektiks. Kõige väiksema väärtusega bitt kõige paremal."""

    return int(bitid.to01(), 2)


