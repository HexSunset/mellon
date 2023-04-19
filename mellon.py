from bitarray import bitarray
from jagaja import Jagaja

saladus = b"Saladus!"

salabitid = bitarray()
salabitid.frombytes(bytes(saladus))
print(salabitid.to01())

tükid = list(map(bitarray.to01, Jagaja(salabitid.tobytes())))
print("".join(tükid))
