from models.musteri import Musteri


class MusteriServisi:
    def __init__(self):
        self._musteriler: list[Musteri] = []
        self._siradaki_id = 1

    def ekle(self, ad: str, telefon: str, eposta: str) -> Musteri:
        musteri = Musteri(self._siradaki_id, ad, telefon, eposta)
        self._musteriler.append(musteri)
        self._siradaki_id += 1
        return musteri

    def hepsini_getir(self) -> list[Musteri]:
        return list(self._musteriler)

    def isimle_ara(self, aranan: str) -> list[Musteri]:
        return [m for m in self._musteriler if aranan.lower() in m.ad.lower()]

    def id_ile_getir(self, id: int) -> Musteri | None:
        return next((m for m in self._musteriler if m.id == id), None)

    def guncelle(self, id: int, ad: str, telefon: str, eposta: str) -> bool:
        musteri = self.id_ile_getir(id)
        if not musteri:
            return False
        musteri.ad = ad
        musteri.telefon = telefon
        musteri.eposta = eposta
        return True

    def filtrele(self, deger: str, alan: str = "hepsi") -> list[Musteri]:
        if not deger:
            return list(self._musteriler)
        d = deger.lower()
        if alan == "ad":
            return [m for m in self._musteriler if d in m.ad.lower()]
        elif alan == "telefon":
            return [m for m in self._musteriler if d in m.telefon.lower()]
        elif alan == "eposta":
            return [m for m in self._musteriler if d in m.eposta.lower()]
        return [m for m in self._musteriler if
                d in m.ad.lower() or d in m.telefon.lower() or d in m.eposta.lower()]

    def sil(self, id: int) -> bool:
        musteri = self.id_ile_getir(id)
        if musteri:
            self._musteriler.remove(musteri)
            return True
        return False
