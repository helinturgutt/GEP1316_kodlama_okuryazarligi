# Öğrenci Not Takip Sistemi
# Bu program terminalde çalışan basit bir not yönetim uygulamasıdır.

# Öğrencilerin adını ve notunu tutacağımız sözlük (dictionary)
# Örnek yapı: {"Ali Veli": 85, "Ayşe Kaya": 92}
ogrenciler = {}


def not_gecerli_mi(not_degeri):
    """Notun 0-100 arasında olup olmadığını kontrol eder."""
    return 0 <= not_degeri <= 100


def ogrenci_ekle():
    """Yeni bir öğrenci ve notu sözlüğe ekler."""
    print("\n--- Öğrenci Ekle ---")

    ad = input("Öğrenci adı: ").strip()

    # Boş isim kontrolü
    if not ad:
        print("Hata: Öğrenci adı boş olamaz.")
        return

    # Aynı isimde öğrenci var mı kontrolü
    if ad in ogrenciler:
        print(f"Hata: '{ad}' adlı öğrenci zaten kayıtlı.")
        return

    # Not girişi ve doğrulaması
    try:
        not_degeri = int(input("Not (0-100): "))
    except ValueError:
        print("Hata: Lütfen geçerli bir sayı girin.")
        return

    if not not_gecerli_mi(not_degeri):
        print("Hata: Not 0 ile 100 arasında olmalıdır.")
        return

    # Öğrenciyi ekle
    ogrenciler[ad] = not_degeri
    print(f"Başarılı: '{ad}' adlı öğrenci {not_degeri} notu ile eklendi.")


def ogrencileri_listele():
    """Kayıtlı tüm öğrencileri ve notlarını ekrana yazar."""
    print("\n--- Öğrenci Listesi ---")

    if not ogrenciler:
        print("Henüz kayıtlı öğrenci bulunmuyor.")
        return

    # Başlık satırı
    print(f"{'Sıra':<6} {'Öğrenci Adı':<25} {'Not':<5}")
    print("-" * 38)

    # Her öğrenciyi sırayla yazdır
    for sira, (ad, not_degeri) in enumerate(ogrenciler.items(), start=1):
        print(f"{sira:<6} {ad:<25} {not_degeri:<5}")

    print(f"\nToplam {len(ogrenciler)} öğrenci kayıtlı.")


def not_guncelle():
    """Var olan bir öğrencinin notunu günceller."""
    print("\n--- Not Güncelle ---")

    if not ogrenciler:
        print("Henüz kayıtlı öğrenci bulunmuyor.")
        return

    ad = input("Güncellenecek öğrencinin adı: ").strip()

    # Öğrenci kayıtlı mı kontrolü
    if ad not in ogrenciler:
        print(f"Hata: '{ad}' adlı öğrenci bulunamadı.")
        return

    print(f"Mevcut not: {ogrenciler[ad]}")

    # Yeni not girişi ve doğrulaması
    try:
        yeni_not = int(input("Yeni not (0-100): "))
    except ValueError:
        print("Hata: Lütfen geçerli bir sayı girin.")
        return

    if not not_gecerli_mi(yeni_not):
        print("Hata: Not 0 ile 100 arasında olmalıdır.")
        return

    eski_not = ogrenciler[ad]
    ogrenciler[ad] = yeni_not
    print(f"Başarılı: '{ad}' adlı öğrencinin notu {eski_not} → {yeni_not} olarak güncellendi.")


def ogrenci_sil():
    """Kayıtlı bir öğrenciyi sözlükten siler."""
    print("\n--- Öğrenci Sil ---")

    if not ogrenciler:
        print("Henüz kayıtlı öğrenci bulunmuyor.")
        return

    ad = input("Silinecek öğrencinin adı: ").strip()

    # Öğrenci kayıtlı mı kontrolü
    if ad not in ogrenciler:
        print(f"Hata: '{ad}' adlı öğrenci bulunamadı.")
        return

    # Silmeden önce onay al
    onay = input(f"'{ad}' adlı öğrenciyi silmek istediğinize emin misiniz? (e/h): ").strip().lower()

    if onay == "e":
        del ogrenciler[ad]
        print(f"Başarılı: '{ad}' adlı öğrenci silindi.")
    else:
        print("İşlem iptal edildi.")


def menu_goster():
    """Ana menüyü ekrana yazdırır."""
    print("\n" + "=" * 35)
    print("   Öğrenci Not Takip Sistemi")
    print("=" * 35)
    print("1. Öğrenci Ekle")
    print("2. Öğrencileri Listele")
    print("3. Not Güncelle")
    print("4. Öğrenci Sil")
    print("5. Çıkış")
    print("=" * 35)


def main():
    """Uygulamanın ana döngüsü. Menüyü gösterir ve seçime göre işlem yapar."""
    print("Öğrenci Not Takip Sistemine Hoşgeldiniz!")

    while True:
        menu_goster()

        secim = input("Seçiminiz (1-5): ").strip()

        if secim == "1":
            ogrenci_ekle()
        elif secim == "2":
            ogrencileri_listele()
        elif secim == "3":
            not_guncelle()
        elif secim == "4":
            ogrenci_sil()
        elif secim == "5":
            print("\nProgram kapatılıyor. Hoşçakalın!")
            break
        else:
            print("Hata: Lütfen 1 ile 5 arasında bir seçim yapın.")


# Programı başlat
if __name__ == "__main__":
    main()
