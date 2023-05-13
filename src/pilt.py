from PIL import Image
from typing import Tuple
import math

class PildiHaldur:
    __faili_nimi: str
    __fail: Image.Image

    # Sisaldab nii piksli indeksit kui ka värvikanalit
    __indeks: int

    def __init__(self, faili_nimi: str):
        self.__faili_nimi = faili_nimi
        self.__fail = Image.open(faili_nimi)
        self.__indeks = 0

    def get_kõrgus(self) -> int:
        return self.__fail.size[1]

    def get_laius(self) -> int:
        return self.__fail.size[0]

    def get_piksli_indeks(self) -> Tuple[int, int]:
        lineaarne_indeks = math.floor(self.__indeks / 3)
        x = lineaarne_indeks % self.get_laius()
        y = math.floor(lineaarne_indeks / self.get_laius())

        return (x, y)

    def get_värvikanal(self):
        return self.__indeks % 3

    def set_piksel(self, piksel: Tuple[int, int, int]):
        indeks = self.get_piksli_indeks()
        self.__fail.putpixel(indeks, piksel)

    def get_piksel(self) -> Tuple[int, int, int]:
        indeks = self.get_piksli_indeks()

        return self.__fail.getpixel(indeks)
