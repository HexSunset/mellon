from jagaja import Jagaja
from kooder import Kooder
from dekooder import Dekooder

saladus = b"Supersalajane"
print(f"sisend: {saladus}")
kooder = Kooder("rott.png")
sisend = Jagaja(saladus)
kooder.kodeeri_otse(sisend)
del kooder

dekooder = Dekooder("rott.png")
väljund = dekooder.dekodeeri_otse()
del dekooder

print(f"väljund: {väljund}")
