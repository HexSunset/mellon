from jagaja import Jagaja

PLOKI_SUURUS_BAITIDES = 2 ** (4 * 8)

class Saladus:
    __failinimi: str
    __sisu: Jagaja

    def __init__(self, failinimi: str):
        self.__failinimi = failinimi
