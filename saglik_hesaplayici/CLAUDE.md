# Sağlık Hesaplayıcı

Python + Tkinter ile yapılmış masaüstü sağlık hesaplama uygulaması.

## Çalıştırmak için
```bash
python3 main.py
```

## Özellikler
- VKİ (Vücut Kitle İndeksi) hesaplama ve kategori (Zayıf / Normal / Fazla Kilolu / Obez)
- BMH (Bazal Metabolizma Hızı) — Mifflin-St Jeor formülü
- Hesaplama geçmişi listesi (seçili sil / tümünü temizle)
- Hatalı girişlerde messagebox uyarısı

## Kod Yapısı (`main.py`)
| Katman | İçerik |
|---|---|
| Hesaplama fonksiyonları | `hesapla_vki`, `vki_kategorisi`, `hesapla_bmh` |
| Doğrulama | `dogrula_girisleri` |
| Arayüz | `SaglikHesaplayici(tk.Tk)` sınıfı |
