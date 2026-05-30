# Öğrenci Not Takip Sistemi - Tkinter GUI Versiyonu
# Çalıştırmak için: python3 ogrenci_not_takip_gui.py

import tkinter as tk
from tkinter import ttk, messagebox


BG      = "#f0f4f8"   # pencere arka planı
PANEL   = "#ffffff"   # panel/çerçeve arka planı
FG      = "#1a1a2e"   # yazı rengi
LABEL   = "#2c3e50"   # koyu etiket rengi


class OgrenciNotTakipApp:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Öğrenci Not Takip Sistemi")
        self.pencere.geometry("650x500")
        self.pencere.resizable(False, False)
        self.pencere.configure(bg=BG)

        # ttk stilini koyu moddan bağımsız olarak sabitle
        stil = ttk.Style()
        stil.theme_use("clam")
        stil.configure("TLabelframe",       background=PANEL, foreground=FG)
        stil.configure("TLabelframe.Label", background=PANEL, foreground=LABEL,
                       font=("Helvetica", 10, "bold"))
        stil.configure("TLabel",  background=PANEL, foreground=FG,
                       font=("Helvetica", 10))
        stil.configure("TEntry",  fieldbackground="white", foreground=FG)
        stil.configure("Treeview",
                       background="white", foreground=FG,
                       fieldbackground="white", rowheight=24)
        stil.configure("Treeview.Heading",
                       background="#dce3ea", foreground=FG,
                       font=("Helvetica", 10, "bold"))
        stil.map("Treeview", background=[("selected", "#3498db")],
                 foreground=[("selected", "white")])

        # Öğrenci verileri: {"Ad Soyad": 85}
        self.ogrenciler = {}

        self._arayuz_olustur()

    # ── Arayüz kurulumu ──────────────────────────────────────────────────────

    def _arayuz_olustur(self):
        # Başlık
        baslik = tk.Label(
            self.pencere,
            text="Öğrenci Not Takip Sistemi",
            font=("Helvetica", 18, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=12,
        )
        baslik.pack(fill="x")

        # Ana çerçeve
        ana_cerceve = tk.Frame(self.pencere, bg=BG)
        ana_cerceve.pack(fill="both", expand=True, padx=20, pady=15)

        # Sol panel: giriş alanları ve butonlar
        sol = tk.Frame(ana_cerceve, bg=BG)
        sol.pack(side="left", fill="y", padx=(0, 15))

        self._giris_alanlari_olustur(sol)
        self._butonlar_olustur(sol)

        # Sağ panel: öğrenci tablosu
        sag = tk.Frame(ana_cerceve, bg=BG)
        sag.pack(side="right", fill="both", expand=True)

        self._tablo_olustur(sag)

        # Durum çubuğu
        self.durum_label = tk.Label(
            self.pencere,
            text="Hoş geldiniz!",
            font=("Helvetica", 9),
            bg="#dce3ea",
            fg="#333",
            anchor="w",
            padx=10,
            pady=4,
        )
        self.durum_label.pack(fill="x", side="bottom")

    def _giris_alanlari_olustur(self, ebeveyn):
        cerceve = ttk.LabelFrame(ebeveyn, text="Öğrenci Bilgileri", padding=12)
        cerceve.pack(fill="x", pady=(0, 10))

        tk.Label(cerceve, text="Öğrenci Adı:", bg=PANEL, fg=FG,
                 font=("Helvetica", 10)).grid(row=0, column=0, sticky="w", pady=4)
        self.ad_giris = ttk.Entry(cerceve, width=22)
        self.ad_giris.grid(row=1, column=0, pady=(0, 8))

        tk.Label(cerceve, text="Not (0–100):", bg=PANEL, fg=FG,
                 font=("Helvetica", 10)).grid(row=2, column=0, sticky="w", pady=4)
        self.not_giris = ttk.Entry(cerceve, width=22)
        self.not_giris.grid(row=3, column=0, pady=(0, 4))

    def _renkli_buton(self, ebeveyn, metin, komut, renk, font_bold=True):
        """macOS'ta güvenilir çalışan renkli buton (Frame + Label)."""
        karanlik = self._renk_karart(renk)
        dis = tk.Frame(ebeveyn, bg=renk, cursor="hand2")
        dis.pack(fill="x", pady=4, ipady=1)

        agirlik = "bold" if font_bold else "normal"
        ic = tk.Label(
            dis, text=metin, bg=renk, fg="white",
            font=("Helvetica", 10, agirlik),
            padx=12, pady=8, cursor="hand2",
        )
        ic.pack(expand=True, fill="both")

        for w in (dis, ic):
            w.bind("<Button-1>",  lambda e: komut())
            w.bind("<Enter>",     lambda e, d=dis, i=ic: (d.config(bg=karanlik), i.config(bg=karanlik)))
            w.bind("<Leave>",     lambda e, d=dis, i=ic, r=renk: (d.config(bg=r), i.config(bg=r)))

    @staticmethod
    def _renk_karart(hex_renk):
        """Verilen hex rengi %15 koyulaştırır."""
        r, g, b = int(hex_renk[1:3], 16), int(hex_renk[3:5], 16), int(hex_renk[5:7], 16)
        r, g, b = max(0, int(r * 0.85)), max(0, int(g * 0.85)), max(0, int(b * 0.85))
        return f"#{r:02x}{g:02x}{b:02x}"

    def _butonlar_olustur(self, ebeveyn):
        cerceve = ttk.LabelFrame(ebeveyn, text="İşlemler", padding=12)
        cerceve.pack(fill="x")

        self._renkli_buton(cerceve, "➕  Öğrenci Ekle",  self.ogrenci_ekle,      "#27ae60")
        self._renkli_buton(cerceve, "✏️  Notu Güncelle", self.not_guncelle,      "#2980b9")
        self._renkli_buton(cerceve, "🗑️  Öğrenci Sil",  self.ogrenci_sil,       "#e74c3c")
        self._renkli_buton(cerceve, "🔄  Temizle",       self.girisleri_temizle, "#7f8c8d", font_bold=False)

    def _tablo_olustur(self, ebeveyn):
        cerceve = ttk.LabelFrame(ebeveyn, text="Öğrenci Listesi", padding=8)
        cerceve.pack(fill="both", expand=True)

        sutunlar = ("sira", "ad", "not", "harf")
        self.tablo = ttk.Treeview(
            cerceve, columns=sutunlar, show="headings", height=16
        )

        self.tablo.heading("sira", text="No")
        self.tablo.heading("ad",   text="Öğrenci Adı")
        self.tablo.heading("not",  text="Not")
        self.tablo.heading("harf", text="Harf Notu")

        self.tablo.column("sira", width=40,  anchor="center")
        self.tablo.column("ad",   width=160, anchor="w")
        self.tablo.column("not",  width=60,  anchor="center")
        self.tablo.column("harf", width=80,  anchor="center")

        # Satır renklendirme etiketleri
        self.tablo.tag_configure("basarili",  background="#d5f5e3")
        self.tablo.tag_configure("orta",      background="#fef9e7")
        self.tablo.tag_configure("dusuk",     background="#fadbd8")

        kaydirici = ttk.Scrollbar(cerceve, orient="vertical", command=self.tablo.yview)
        self.tablo.configure(yscrollcommand=kaydirici.set)

        self.tablo.pack(side="left", fill="both", expand=True)
        kaydirici.pack(side="right", fill="y")

        # Tabloda seçim yapılınca giriş alanlarını doldur
        self.tablo.bind("<<TreeviewSelect>>", self._secim_degisti)

    # ── Yardımcı metodlar ────────────────────────────────────────────────────

    def _not_gecerli_mi(self, deger):
        return 0 <= deger <= 100

    def _harf_notu(self, not_degeri):
        if not_degeri >= 90: return "AA"
        if not_degeri >= 80: return "BA"
        if not_degeri >= 70: return "BB"
        if not_degeri >= 60: return "CB"
        if not_degeri >= 50: return "CC"
        return "FF"

    def _tabloyu_guncelle(self):
        for satir in self.tablo.get_children():
            self.tablo.delete(satir)

        for sira, (ad, not_degeri) in enumerate(self.ogrenciler.items(), start=1):
            harf = self._harf_notu(not_degeri)
            if not_degeri >= 70:
                etiket = "basarili"
            elif not_degeri >= 50:
                etiket = "orta"
            else:
                etiket = "dusuk"
            self.tablo.insert("", "end", values=(sira, ad, not_degeri, harf), tags=(etiket,))

        self.durum_label.config(text=f"Toplam {len(self.ogrenciler)} öğrenci kayıtlı.")

    def _durum_goster(self, mesaj, renk="#333"):
        self.durum_label.config(text=mesaj, fg=renk)

    def _secim_degisti(self, _event):
        secili = self.tablo.selection()
        if not secili:
            return
        degerler = self.tablo.item(secili[0], "values")
        ad, not_degeri = degerler[1], degerler[2]

        self.ad_giris.delete(0, "end")
        self.ad_giris.insert(0, ad)

        self.not_giris.delete(0, "end")
        self.not_giris.insert(0, not_degeri)

    def _ad_ve_not_al(self):
        ad = self.ad_giris.get().strip()
        not_str = self.not_giris.get().strip()

        if not ad:
            messagebox.showerror("Hata", "Öğrenci adı boş olamaz.")
            return None, None

        try:
            not_degeri = int(not_str)
        except ValueError:
            messagebox.showerror("Hata", "Not alanına yalnızca tam sayı girin.")
            return None, None

        if not self._not_gecerli_mi(not_degeri):
            messagebox.showerror("Hata", "Not 0 ile 100 arasında olmalıdır.")
            return None, None

        return ad, not_degeri

    def girisleri_temizle(self):
        self.ad_giris.delete(0, "end")
        self.not_giris.delete(0, "end")
        self.tablo.selection_remove(self.tablo.selection())
        self._durum_goster("Giriş alanları temizlendi.")

    # ── Temel işlemler ───────────────────────────────────────────────────────

    def ogrenci_ekle(self):
        ad, not_degeri = self._ad_ve_not_al()
        if ad is None:
            return

        if ad in self.ogrenciler:
            messagebox.showerror("Hata", f"'{ad}' adlı öğrenci zaten kayıtlı.")
            return

        self.ogrenciler[ad] = not_degeri
        self._tabloyu_guncelle()
        self.girisleri_temizle()
        messagebox.showinfo("Başarılı", f"'{ad}' adlı öğrenci {not_degeri} notu ile eklendi.")
        self._durum_goster(f"'{ad}' eklendi.", renk="#27ae60")

    def not_guncelle(self):
        ad, yeni_not = self._ad_ve_not_al()
        if ad is None:
            return

        if ad not in self.ogrenciler:
            messagebox.showerror("Hata", f"'{ad}' adlı öğrenci bulunamadı.\nÖnce listeden seçin veya doğru adı yazın.")
            return

        eski_not = self.ogrenciler[ad]
        self.ogrenciler[ad] = yeni_not
        self._tabloyu_guncelle()
        self.girisleri_temizle()
        messagebox.showinfo("Başarılı", f"'{ad}' adlı öğrencinin notu {eski_not} → {yeni_not} olarak güncellendi.")
        self._durum_goster(f"'{ad}' notu güncellendi.", renk="#2980b9")

    def ogrenci_sil(self):
        ad = self.ad_giris.get().strip()

        if not ad:
            messagebox.showerror("Hata", "Silinecek öğrenciyi listeden seçin veya adını yazın.")
            return

        if ad not in self.ogrenciler:
            messagebox.showerror("Hata", f"'{ad}' adlı öğrenci bulunamadı.")
            return

        onay = messagebox.askyesno(
            "Onay",
            f"'{ad}' adlı öğrenciyi silmek istediğinize emin misiniz?"
        )

        if onay:
            del self.ogrenciler[ad]
            self._tabloyu_guncelle()
            self.girisleri_temizle()
            messagebox.showinfo("Başarılı", f"'{ad}' adlı öğrenci silindi.")
            self._durum_goster(f"'{ad}' silindi.", renk="#e74c3c")


# ── Uygulamayı başlat ────────────────────────────────────────────────────────

if __name__ == "__main__":
    pencere = tk.Tk()
    uygulama = OgrenciNotTakipApp(pencere)
    pencere.mainloop()
