class Musteri:
    def __init__(self, id: int, ad: str, telefon: str, eposta: str):
        self.id = id
        self.ad = ad
        self.telefon = telefon
        self.eposta = eposta

    def __str__(self):
        return f"{self.id:<5} {self.ad:<25} {self.telefon:<15} {self.eposta}"
