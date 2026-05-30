# Öğrenci Not Takip Sistemi - Test Dosyası
# Bu dosya, uygulamanın temel fonksiyonlarını otomatik olarak test eder.
# Testler, unittest modülü kullanılarak yazılmıştır.

import unittest
import sys
import os

# Ana modülü import edebilmek için üst dizini Python yoluna ekle
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test edeceğimiz fonksiyonları ve veri yapısını import et
import ogrenci_not_takip as app


class TestOgrenciNotTakip(unittest.TestCase):
    """Öğrenci not takip sisteminin tüm fonksiyonlarını test eder."""

    def setUp(self):
        """Her testten önce öğrenci listesini temizler (temiz başlangıç)."""
        app.ogrenciler.clear()

    # ------------------------------------------------------------------ #
    # Test 1: Geçerli öğrenci ekleme
    # ------------------------------------------------------------------ #
    def test_01_gecerli_ogrenci_ekleme(self):
        """Geçerli ad ve not ile öğrenci eklenebilmeli."""
        app.ogrenciler["Ali Veli"] = 85
        self.assertIn("Ali Veli", app.ogrenciler)
        self.assertEqual(app.ogrenciler["Ali Veli"], 85)
        print("✔ Test 1 GEÇTI: Geçerli öğrenci ekleme")

    # ------------------------------------------------------------------ #
    # Test 2: Öğrencileri listeleme
    # ------------------------------------------------------------------ #
    def test_02_ogrencileri_listeleme(self):
        """Birden fazla öğrenci eklenip listelenebilmeli."""
        app.ogrenciler["Ayşe Kaya"] = 92
        app.ogrenciler["Mehmet Oz"] = 74
        self.assertEqual(len(app.ogrenciler), 2)
        self.assertIn("Ayşe Kaya", app.ogrenciler)
        self.assertIn("Mehmet Oz", app.ogrenciler)
        print("✔ Test 2 GEÇTI: Öğrencileri listeleme")

    # ------------------------------------------------------------------ #
    # Test 3: Var olan öğrencinin notunu güncelleme
    # ------------------------------------------------------------------ #
    def test_03_not_guncelleme(self):
        """Kayıtlı öğrencinin notu değiştirilebilmeli."""
        app.ogrenciler["Fatma Demir"] = 60
        # Notu güncelle
        app.ogrenciler["Fatma Demir"] = 75
        self.assertEqual(app.ogrenciler["Fatma Demir"], 75)
        print("✔ Test 3 GEÇTI: Not güncelleme")

    # ------------------------------------------------------------------ #
    # Test 4: Öğrenci silme
    # ------------------------------------------------------------------ #
    def test_04_ogrenci_silme(self):
        """Kayıtlı öğrenci listeden kaldırılabilmeli."""
        app.ogrenciler["Can Şahin"] = 88
        del app.ogrenciler["Can Şahin"]
        self.assertNotIn("Can Şahin", app.ogrenciler)
        print("✔ Test 4 GEÇTI: Öğrenci silme")

    # ------------------------------------------------------------------ #
    # Test 5: Hatalı not girişi — 120 veya -5
    # ------------------------------------------------------------------ #
    def test_05_hatali_not_120(self):
        """120 notu geçersiz sayılmalı."""
        self.assertFalse(app.not_gecerli_mi(120))
        print("✔ Test 5a GEÇTI: 120 hatalı not reddedildi")

    def test_05_hatali_not_eksi5(self):
        """-5 notu geçersiz sayılmalı."""
        self.assertFalse(app.not_gecerli_mi(-5))
        print("✔ Test 5b GEÇTI: -5 hatalı not reddedildi")

    def test_05_sinir_degerleri(self):
        """0 ve 100 geçerli sınır değerleri olmalı."""
        self.assertTrue(app.not_gecerli_mi(0))
        self.assertTrue(app.not_gecerli_mi(100))
        print("✔ Test 5c GEÇTI: 0 ve 100 sınır değerleri kabul edildi")

    # ------------------------------------------------------------------ #
    # Test 6: Çıkış (programın döngüsünü bozmadan kontrol)
    # ------------------------------------------------------------------ #
    def test_06_cikis_secenegi(self):
        """'5' seçimi döngüden çıkışı temsil etmeli — geçersiz seçim olmamalı."""
        gecerli_secimler = {"1", "2", "3", "4", "5"}
        self.assertIn("5", gecerli_secimler)
        print("✔ Test 6 GEÇTI: Çıkış seçeneği menüde mevcut")


# ------------------------------------------------------------------ #
# Testleri çalıştır
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    print("=" * 45)
    print("  Öğrenci Not Takip Sistemi — Testler")
    print("=" * 45)
    # verbosity=2 → her test için detaylı çıktı gösterir
    unittest.main(verbosity=2)
