from services.musteri_servisi import MusteriServisi


class Menu:
    BASLIK = f"{'ID':<5} {'Ad Soyad':<25} {'Telefon':<15} {'E-posta'}"
    AYRAC = "-" * 65

    def __init__(self):
        self._servis = MusteriServisi()

    def baslat(self):
        print("Hoş geldiniz! Mini Müşteri Kayıt Sistemine bağlandınız.")
        while True:
            self._menu_goster()
            secim = input("Seçiminiz: ").strip()
            self._islemi_isle(secim)

    def _menu_goster(self):
        print("\n=============================")
        print("   MİNİ MÜŞTERİ KAYIT SİSTEMİ")
        print("=============================")
        print("1. Müşteri Ekle")
        print("2. Müşterileri Listele")
        print("3. Müşteri Ara")
        print("4. Müşteri Sil")
        print("0. Çıkış")
        print("-----------------------------")

    def _islemi_isle(self, secim: str):
        islemler = {
            "1": self._musteri_ekle,
            "2": self._musterileri_listele,
            "3": self._musteri_ara,
            "4": self._musteri_sil,
            "0": self._cikis,
        }
        islem = islemler.get(secim)
        if islem:
            islem()
        else:
            print("Hata: Geçersiz seçim. Lütfen menüdeki seçeneklerden birini girin.")

    def _musteri_ekle(self):
        print("\n--- YENİ MÜŞTERİ EKLE ---")
        ad = input("Ad Soyad: ").strip()
        if not ad:
            print("Hata: Ad Soyad boş bırakılamaz.")
            return
        telefon = input("Telefon: ").strip()
        if not telefon:
            print("Hata: Telefon boş bırakılamaz.")
            return
        eposta = input("E-posta: ").strip()

        musteri = self._servis.ekle(ad, telefon, eposta)
        print(f"Müşteri başarıyla eklendi. (ID: {musteri.id})")

    def _musterileri_listele(self):
        print("\n--- MÜŞTERİ LİSTESİ ---")
        musteriler = self._servis.hepsini_getir()
        if not musteriler:
            print("Kayıtlı müşteri bulunamadı.")
            return
        print(self.BASLIK)
        print(self.AYRAC)
        for m in musteriler:
            print(m)

    def _musteri_ara(self):
        print("\n--- MÜŞTERİ ARA ---")
        aranan = input("Aranacak isim: ").strip()
        if not aranan:
            print("Hata: Arama terimi boş bırakılamaz.")
            return
        bulunanlar = self._servis.isimle_ara(aranan)
        if not bulunanlar:
            print(f"'{aranan}' ile eşleşen müşteri bulunamadı.")
            return
        print(f"{len(bulunanlar)} müşteri bulundu:")
        print(self.BASLIK)
        print(self.AYRAC)
        for m in bulunanlar:
            print(m)

    def _musteri_sil(self):
        print("\n--- MÜŞTERİ SİL ---")
        girdi = input("Silinecek müşterinin ID'sini girin: ").strip()
        if not girdi.isdigit():
            print("Hata: Geçerli bir ID giriniz (sayı olmalı).")
            return
        musteri = self._servis.id_ile_getir(int(girdi))
        if not musteri:
            print(f"ID {girdi} ile eşleşen müşteri bulunamadı.")
            return
        onay = input(f"'{musteri.ad}' adlı müşteriyi silmek istediğinize emin misiniz? (e/h): ").strip().lower()
        if onay == "e":
            self._servis.sil(musteri.id)
            print("Müşteri başarıyla silindi.")
        else:
            print("Silme işlemi iptal edildi.")

    def _cikis(self):
        print("Programdan çıkılıyor. Görüşürüz!")
        raise SystemExit
