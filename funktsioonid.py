from bitarray import bitarray

def bitideks(number: int) -> bitarray:
    """Muudab numbri bitarray objektiks, kõige väiksema väärtusega bitt kõige paremal."""

    biti_string = (bin(number)[2:]).rjust(8, '0')
    väljund = bitarray(biti_string)
    return väljund

def bitidest(bitid: bitarray) -> int:
    """Bitarray objekt int objektiks. Kõige väiksema väärtusega bitt kõige paremal."""

    return int(bitid.to01(), 2)
