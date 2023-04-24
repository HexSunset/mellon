from PIL import Image
import math
from typing import Tuple

class PildiMuutja:
    """Pildi muutmise algklass, implementeerib põhifunktsioonid"""
    
    def __init__(self, pildi_nimi: str):
        self.pildi_nimi = pildi_nimi
        self.fail = Image.open(pildi_nimi)

        if self.fail.mode not in ["RGB", "RGBA"]:
            raise ValueError(f"Program toetab ainult pilte, mis on RGB või RGBA formaadis, antud pilt on: {self.fail.mode}")

        # pikslite arv
        self.maht = self.fail.width * self.fail.height
        
        # Igal pikslil kolm kasutatavat kanalit
        self.maht *= 3

        # See indeks sisaldab nii piksli indeksit kui ka värvikanalit
        # Värvikanali kätte saamiseks: self.indeks % 3
        # Piksli indeksi kätte saamiseks: math.floor(self.indeks / 3)
        self.indeks = 0

    # Destruktor
    def __del__(self):
        self.fail.save("muudetud_" + self.pildi_nimi)
        self.fail.close()
        
    def piksli_indeks(self) -> Tuple[int, int]:
        lineaarne_indeks = math.floor(self.indeks / 3)
        y = math.floor(lineaarne_indeks / self.fail.width)
        x = lineaarne_indeks % self.fail.width
        return (x, y)

    def piksli_kanal(self) -> int:
        return self.indeks % 3
