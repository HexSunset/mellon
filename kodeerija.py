from PIL import Image
from bitarray import bitarray
from jagaja import Jagaja

class Kodeerija:
    """Avab pildi ja kodeerib sinna kasutaja poolt antud sisendi(d)"""
    
    def __init__(self, pildi_nimi: str):
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
        
    def kodeeri(self, sisend: Jagaja):
        if not sisend.tükkide_arv <= self.maht - self.indeks:
            raise ValueError("Sisend on liiga suur")

        # Kodeeritud info paigutus failis
        # -------------------------------
        # Info pikkus baitides (16-bitine arv, 8 2-bitist tükki)
        # Mitu bitti on igas tükis (1-8)
        # Tükk
        # ...
        # Tükk
        # Mingi väärtus vigade kontrolli jaoks (parity check?)
