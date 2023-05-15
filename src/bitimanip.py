from bitarray import bitarray
from typing import Tuple

"""Bittide ja baitidega töötamise abifunktsioonid."""

def bitideks(number: int, pikkus=8) -> bitarray:
    """Muudab numbri bitarray objektiks, kõige väiksema väärtusega bitt kõige paremal."""

    biti_string = (bin(number)[2:]).rjust(pikkus, '0')
    väljund = bitarray(biti_string)
    return väljund

def joonda_bitid(bitid: bitarray, pikkus=8) -> bitarray:
    """Teeb kindlaks, et antud bitarray oleks õige pikkusega."""

    if len(bitid) < pikkus:
        bitid = bitarray(bitid.to01().rjust(pikkus, '0'))
    if len(bitid) > pikkus:
        bitid = bitid[-pikkus:]

    return bitid

def bitidest(bitid: bitarray) -> int:
    """Bitarray objekt int objektiks. Kõige väiksema väärtusega bitt kõige paremal."""

    return int(bitid.to01(), 2)

def bitimask(maskeeritud_bitte=2) -> bitarray:
    bitid = bitarray("11111111")
    bitid <<= maskeeritud_bitte
    bitid = joonda_bitid(bitid)

    return bitid
