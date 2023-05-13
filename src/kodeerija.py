from pilt import PildiHaldur

class Kodeerija:
    __pildi_haldur: None | PildiHaldur

    def __init__(self):
        self.__pildi_haldur = None

    def ava_pilt(self, pildi_nimi: str):
        self.__pildi_haldur = PildiHaldur(pildi_nimi)
