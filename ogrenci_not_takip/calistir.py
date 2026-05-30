# Öğrenci Not Takip Sistemi - Başlatıcı
# Çalıştırmak için: python3 calistir.py

import subprocess
import sys

print("=" * 40)
print("  Öğrenci Not Takip Sistemi")
print("=" * 40)
print("1. GUI Uygulamasını Aç")
print("2. Terminal Uygulamasını Aç")
print("3. Testleri Çalıştır")
print("4. Çıkış")
print("=" * 40)

secim = input("Seçiminiz (1-4): ").strip()

if secim == "1":
    subprocess.run([sys.executable, "ogrenci_not_takip_gui.py"])
elif secim == "2":
    subprocess.run([sys.executable, "ogrenci_not_takip.py"])
elif secim == "3":
    subprocess.run([sys.executable, "test_ogrenci_not_takip.py"])
elif secim == "4":
    print("Çıkılıyor...")
else:
    print("Geçersiz seçim.")
