import tkinter as tk
from tkinter import messagebox
from datetime import datetime


# ─── Hesaplama Fonksiyonları ──────────────────────────────────────────────────

def hesapla_vki(kilo_kg, boy_m):
    return kilo_kg / (boy_m ** 2)


def vki_kategorisi(vki):
    if vki < 18.5:
        return "Zayıf", "#7dcfff"        # açık mavi
    elif vki < 25.0:
        return "Normal", "#9ece6a"        # yeşil
    elif vki < 30.0:
        return "Fazla Kilolu", "#ff9e64"  # turuncu
    else:
        return "Obez", "#f7768e"          # kırmızı


def hesapla_bmh(kilo_kg, boy_cm, yas, cinsiyet):
    """Mifflin-St Jeor formülü."""
    temel = 10 * kilo_kg + 6.25 * boy_cm - 5 * yas
    return temel + 5 if cinsiyet == "Erkek" else temel - 161


# ─── Doğrulama ────────────────────────────────────────────────────────────────

def dogrula_girisleri(ad, yas_str, boy_str, kilo_str):
    if not ad.strip():
        raise ValueError("Ad Soyad boş bırakılamaz.")

    try:
        yas = int(yas_str)
    except ValueError:
        raise ValueError("Yaş tam sayı olmalıdır.")
    if not (1 <= yas <= 120):
        raise ValueError("Yaş 1 ile 120 arasında olmalıdır.")

    try:
        boy = float(boy_str)
    except ValueError:
        raise ValueError("Boy sayısal bir değer olmalıdır.")
    if not (50 <= boy <= 300):
        raise ValueError("Boy 50 ile 300 cm arasında olmalıdır.")

    try:
        kilo = float(kilo_str)
    except ValueError:
        raise ValueError("Kilo sayısal bir değer olmalıdır.")
    if not (1 <= kilo <= 500):
        raise ValueError("Kilo 1 ile 500 kg arasında olmalıdır.")

    return yas, boy, kilo


# ─── Ana Uygulama ─────────────────────────────────────────────────────────────

class SaglikHesaplayici(tk.Tk):
    # Tokyo Night renk paleti — hem karanlık hem açık ekranda okunabilir
    BG          = "#1a1b26"   # ana arka plan
    PANEL_BG    = "#24283b"   # panel arka planı
    GIRIS_BG    = "#1f2335"   # giriş kutusu arka planı
    ACCENT      = "#7aa2f7"   # mavi vurgu
    BTN_SIL     = "#f7768e"   # kırmızı — sil butonu
    BTN_TEMIZLE = "#565f89"   # soluk mor — temizle butonu
    METIN       = "#c0caf5"   # ana metin (açık lavanta)
    METIN_DIM   = "#787c99"   # soluk metin, etiketler
    CERCEVE     = "#3b4261"   # kenarlık
    BASLIK_BG   = "#16161e"   # başlık bandı

    def __init__(self):
        super().__init__()
        self.title("Sağlık Hesaplayıcı")
        self.geometry("760x660")
        self.resizable(False, False)
        self.configure(bg=self.BG)
        self._arayuz_olustur()

    # ── Arayüz ────────────────────────────────────────────────────────────────

    def _arayuz_olustur(self):
        self._baslik_olustur()
        icerik = tk.Frame(self, bg=self.BG, padx=20, pady=14)
        icerik.pack(fill=tk.BOTH, expand=True)
        icerik.grid_columnconfigure(0, weight=1)
        icerik.grid_columnconfigure(1, weight=1)
        icerik.grid_rowconfigure(1, weight=1)

        self._giris_paneli_olustur(icerik)
        self._sonuc_paneli_olustur(icerik)
        self._gecmis_paneli_olustur(icerik)

    def _baslik_olustur(self):
        cerceve = tk.Frame(self, bg=self.BASLIK_BG, pady=16)
        cerceve.pack(fill=tk.X)
        tk.Label(
            cerceve,
            text="Sağlık Hesaplayıcı",
            font=("Helvetica", 19, "bold"),
            bg=self.BASLIK_BG, fg=self.ACCENT
        ).pack()
        tk.Label(
            cerceve,
            text="VKİ  ·  Bazal Metabolizma Hızı",
            font=("Helvetica", 9),
            bg=self.BASLIK_BG, fg=self.METIN_DIM
        ).pack()

    def _giris_paneli_olustur(self, ebeveyn):
        panel = self._panel(ebeveyn, "Kişisel Bilgiler")
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 14))

        alanlar = ["Ad Soyad:", "Cinsiyet:", "Yaş:", "Boy (cm):", "Kilo (kg):"]
        for i, etiket in enumerate(alanlar):
            tk.Label(
                panel, text=etiket,
                font=("Helvetica", 10), bg=self.PANEL_BG,
                fg=self.METIN_DIM, anchor="w"
            ).grid(row=i, column=0, sticky="w", padx=(0, 12), pady=7)

        self.ad_giris   = self._giris(panel, 0)
        self.yas_giris  = self._giris(panel, 2)
        self.boy_giris  = self._giris(panel, 3)
        self.kilo_giris = self._giris(panel, 4)

        # Cinsiyet radio butonları
        self.cinsiyet_var = tk.StringVar(value="Erkek")
        cin = tk.Frame(panel, bg=self.PANEL_BG)
        cin.grid(row=1, column=1, sticky="w", pady=7)
        for deger in ("Erkek", "Kadın"):
            tk.Radiobutton(
                cin, text=deger, variable=self.cinsiyet_var, value=deger,
                bg=self.PANEL_BG, fg=self.METIN,
                selectcolor=self.GIRIS_BG, activebackground=self.PANEL_BG,
                activeforeground=self.ACCENT,
                font=("Helvetica", 10)
            ).pack(side=tk.LEFT, padx=(0, 12))

        # Hesapla butonu
        tk.Button(
            panel, text="Hesapla",
            command=self._hesapla,
            bg=self.ACCENT, fg=self.BASLIK_BG,
            font=("Helvetica", 11, "bold"),
            relief="flat", cursor="hand2", pady=8,
            activebackground="#92b4f8", activeforeground=self.BASLIK_BG
        ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(16, 2))

    def _sonuc_paneli_olustur(self, ebeveyn):
        panel = self._panel(ebeveyn, "Sonuçlar")
        panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 14))

        self.sonuc_metin = tk.Text(
            panel,
            font=("Courier", 11),
            width=27, height=13,
            state=tk.DISABLED,
            bg=self.GIRIS_BG, relief="flat",
            wrap=tk.WORD, pady=10, padx=10,
            fg=self.METIN,
            insertbackground=self.ACCENT,
            selectbackground=self.CERCEVE,
            bd=0, highlightthickness=0
        )
        self.sonuc_metin.pack(fill=tk.BOTH, expand=True)

        # Kategori renklerini Text tag'lerine bağla
        for tag, renk in [("Zayıf", "#7dcfff"), ("Normal", "#9ece6a"),
                           ("Fazla Kilolu", "#ff9e64"), ("Obez", "#f7768e")]:
            self.sonuc_metin.tag_config(tag, foreground=renk, font=("Courier", 11, "bold"))

    def _gecmis_paneli_olustur(self, ebeveyn):
        panel = self._panel(ebeveyn, "Hesaplama Geçmişi")
        panel.grid(row=1, column=0, columnspan=2, sticky="nsew")

        liste_cerceve = tk.Frame(panel, bg=self.PANEL_BG)
        liste_cerceve.pack(fill=tk.BOTH, expand=True)

        sb = tk.Scrollbar(liste_cerceve, bg=self.CERCEVE, troughcolor=self.GIRIS_BG)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        self.gecmis_listesi = tk.Listbox(
            liste_cerceve,
            yscrollcommand=sb.set,
            font=("Courier", 9),
            height=7,
            bg=self.GIRIS_BG, relief="flat",
            selectbackground=self.CERCEVE, selectforeground=self.METIN,
            fg=self.METIN_DIM, bd=0, highlightthickness=0,
            activestyle="none"
        )
        self.gecmis_listesi.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.config(command=self.gecmis_listesi.yview)

        btn_cerceve = tk.Frame(panel, bg=self.PANEL_BG)
        btn_cerceve.pack(pady=(12, 0), anchor="w")

        tk.Button(
            btn_cerceve, text="Seçili Kaydı Sil",
            command=self._secili_sil,
            bg=self.BTN_SIL, fg=self.BASLIK_BG,
            font=("Helvetica", 9, "bold"),
            relief="flat", cursor="hand2", padx=12, pady=6,
            activebackground="#f98ca0", activeforeground=self.BASLIK_BG
        ).pack(side=tk.LEFT, padx=(0, 8))

        tk.Button(
            btn_cerceve, text="Tümünü Temizle",
            command=self._tumunu_temizle,
            bg=self.BTN_TEMIZLE, fg=self.METIN,
            font=("Helvetica", 9, "bold"),
            relief="flat", cursor="hand2", padx=12, pady=6,
            activebackground="#6b7299", activeforeground=self.METIN
        ).pack(side=tk.LEFT)

    # ── Yardımcı Widget Oluşturucular ─────────────────────────────────────────

    def _panel(self, ebeveyn, baslik):
        return tk.LabelFrame(
            ebeveyn, text=f"  {baslik}  ",
            font=("Helvetica", 10, "bold"),
            bg=self.PANEL_BG, fg=self.METIN_DIM,
            relief="flat", bd=1,
            highlightbackground=self.CERCEVE,
            highlightthickness=1,
            padx=14, pady=12
        )

    def _giris(self, ebeveyn, satir):
        giris = tk.Entry(
            ebeveyn,
            font=("Helvetica", 10),
            width=20,
            relief="flat", bd=0,
            bg=self.GIRIS_BG, fg=self.METIN,
            insertbackground=self.ACCENT,        # imleç rengi
            selectbackground=self.CERCEVE,
            highlightthickness=1,
            highlightbackground=self.CERCEVE,
            highlightcolor=self.ACCENT           # odaklanınca kenarlık rengi
        )
        giris.grid(row=satir, column=1, sticky="w", pady=7, ipady=4)
        return giris

    # ── İş Mantığı ────────────────────────────────────────────────────────────

    def _hesapla(self):
        ad       = self.ad_giris.get()
        cinsiyet = self.cinsiyet_var.get()
        yas_str  = self.yas_giris.get()
        boy_str  = self.boy_giris.get()
        kilo_str = self.kilo_giris.get()

        try:
            yas, boy, kilo = dogrula_girisleri(ad, yas_str, boy_str, kilo_str)
        except ValueError as hata:
            messagebox.showerror("Hatalı Giriş", str(hata))
            return

        vki           = hesapla_vki(kilo, boy / 100)
        kategori, _   = vki_kategorisi(vki)
        bmh           = hesapla_bmh(kilo, boy, yas, cinsiyet)

        self._sonuclari_goster(ad, cinsiyet, yas, boy, kilo, vki, kategori, bmh)
        self._gecmise_kaydet(ad, vki, kategori, bmh)

    def _sonuclari_goster(self, ad, cinsiyet, yas, boy, kilo, vki, kategori, bmh):
        self.sonuc_metin.config(state=tk.NORMAL)
        self.sonuc_metin.delete("1.0", tk.END)

        satirlar = [
            (f"  {ad}\n",                    None),
            (f"  {cinsiyet} · {yas} yaş\n",  None),
            (f"  {'─' * 23}\n\n",             None),
            (f"  Boy  : {boy:.1f} cm\n",      None),
            (f"  Kilo : {kilo:.1f} kg\n\n",   None),
            (f"  VKİ  : {vki:.2f}\n",         None),
            (f"  Durum: ",                    None),
            (f"{kategori}\n\n",               kategori),   # ← renkli tag
            (f"  BMH  : {bmh:.0f} kcal/gün\n", None),
        ]

        for metin, tag in satirlar:
            if tag:
                self.sonuc_metin.insert(tk.END, metin, tag)
            else:
                self.sonuc_metin.insert(tk.END, metin)

        self.sonuc_metin.config(state=tk.DISABLED)

    def _gecmise_kaydet(self, ad, vki, kategori, bmh):
        zaman = datetime.now().strftime("%H:%M:%S")
        kayit = f"[{zaman}]  {ad:<16} VKİ:{vki:5.2f} ({kategori:<12})  BMH:{bmh:.0f} kcal"
        self.gecmis_listesi.insert(tk.END, kayit)
        self.gecmis_listesi.see(tk.END)

    def _secili_sil(self):
        secim = self.gecmis_listesi.curselection()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen silmek için bir kayıt seçin.")
            return
        self.gecmis_listesi.delete(secim[0])

    def _tumunu_temizle(self):
        if self.gecmis_listesi.size() == 0:
            messagebox.showinfo("Bilgi", "Geçmiş zaten boş.")
            return
        if messagebox.askyesno("Onay", "Tüm geçmiş silinecek. Emin misiniz?"):
            self.gecmis_listesi.delete(0, tk.END)
            self.sonuc_metin.config(state=tk.NORMAL)
            self.sonuc_metin.delete("1.0", tk.END)
            self.sonuc_metin.config(state=tk.DISABLED)


# ─── Başlat ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uygulama = SaglikHesaplayici()
    uygulama.mainloop()
