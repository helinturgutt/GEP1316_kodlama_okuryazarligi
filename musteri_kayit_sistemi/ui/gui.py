import tkinter as tk
from tkinter import ttk, messagebox
import re
from services.musteri_servisi import MusteriServisi

SURUM = "v1.0"

# ─────────────────────────────────────────────────────────────────────────────
# Renk paleti
# Kural: TÜM butonlar KOYU ARKAPLAN + BEYAZ METİN
# → hem açık hem koyu sistem temasında hiç hover gerekmeden okunur
# ─────────────────────────────────────────────────────────────────────────────
C = {
    # Kenar çubuğu
    "sb":        "#1A252F",   # ana arkaplan
    "sb_hvr":    "#2C3E50",   # hover
    "sb_aktif":  "#21618C",   # seçili öğe
    "sb_txt":    "#FFFFFF",   # metin (saf beyaz, max kontrast)
    "sb_div":    "#2C3E50",   # bölücü çizgi

    # İçerik alanı
    "bg":        "#EBF5FB",
    "kart":      "#FFFFFF",
    "sinir":     "#AED6F1",
    "baslik_t":  "#1B2631",
    "etiket_t":  "#1B2631",
    "ipucu_t":   "#5D6D7E",

    # Butonlar — hepsinde KOYU ARKAPLAN + BEYAZ METİN
    "b_y":    "#1D8348",   # yeşil  → ekle / kaydet
    "b_y_h":  "#239B56",
    "b_m":    "#1A5276",   # mavi   → yenile / ara
    "b_m_h":  "#2471A3",
    "b_t":    "#9A7D0A",   # amber  → güncelle
    "b_t_h":  "#B7950B",
    "b_k":    "#922B21",   # kırmızı→ sil
    "b_k_h":  "#C0392B",
    "b_g":    "#4D5656",   # gri    → ikincil (temizle, iptal)
    "b_g_h":  "#5D6D7E",
    "b_txt":  "#FFFFFF",   # HER butonun metni beyaz

    # Tablo
    "t_head":   "#1A5276",
    "t_head_t": "#FFFFFF",
    "t_cift":   "#D6EAF8",
    "t_tek":    "#FFFFFF",
    "t_sec":    "#1A5276",
    "t_sec_t":  "#FFFFFF",

    # Giriş alanları
    "g_bg":    "#FDFDFD",
    "g_sinir": "#85929E",
    "g_odak":  "#1A5276",
    "g_txt":   "#1B2631",

    # Durum çubuğu
    "d_bg":  "#1A252F",
    "d_txt": "#7F8C8D",

    # Hata / başarı
    "hata": "#C0392B",
    "ok":   "#1D8348",
}

F = {
    "baslik": ("Helvetica", 16, "bold"),
    "et":     ("Helvetica", 10, "bold"),
    "nr":     ("Helvetica", 10),
    "kk":     ("Helvetica", 9),
    "btn":    ("Helvetica", 10, "bold"),
    "btn_n":  ("Helvetica", 10),
    "sb":     ("Helvetica", 11),
    "logo":   ("Helvetica", 12, "bold"),
    "d":      ("Helvetica", 9),
}

# Sütun tanımları (tüm treeview'larda aynı)
SUTUNLAR = [
    ("id",      "ID",       58,  "center"),
    ("ad",      "Ad Soyad", 210, "w"),
    ("telefon", "Telefon",  150, "w"),
    ("eposta",  "E-posta",  228, "w"),
]


class Buton(tk.Label):
    """
    tk.Label tabanlı buton.

    macOS'ta tk.Button native Aqua temasıyla çizilir ve özel bg/fg renklerini
    yoksayar — metin hover olmadan okunamaz. tk.Label ise bg/fg'yi her zaman
    doğrudan uygular; bu sınıf onun üzerine hover + disabled desteği ekler.
    """

    def __init__(self, parent, text: str, bg: str, bg_h: str, cmd,
                 fg: str = "#FFFFFF", font=None, px: int = 18, py: int = 8):
        super().__init__(
            parent, text=text,
            bg=bg, fg=fg,
            font=font or F["btn"],
            padx=px, pady=py,
            cursor="hand2",
        )
        self._bg = bg
        self._bg_h = bg_h
        self._fg = fg
        self._aktif = True
        self._cmd = cmd

        self.bind("<Enter>",    self._gir)
        self.bind("<Leave>",    self._cik)
        self.bind("<Button-1>", self._tiklandi)

    def _gir(self, _e):
        if self._aktif:
            tk.Label.configure(self, bg=self._bg_h)

    def _cik(self, _e):
        tk.Label.configure(self, bg=self._bg if self._aktif else "#95A5A6")

    def _tiklandi(self, _e):
        if self._aktif:
            self._cmd()

    def configure(self, **kw):
        if "state" in kw:
            state = kw.pop("state")
            self._aktif = (state == "normal")
            tk.Label.configure(
                self,
                bg=self._bg if self._aktif else "#95A5A6",
                fg=self._fg if self._aktif else "#BDC3C7",
                cursor="hand2" if self._aktif else "arrow",
            )
        if kw:
            tk.Label.configure(self, **kw)

    config = configure


class GUI:
    def __init__(self):
        self._servis = MusteriServisi()
        self._aktif_idx: int = 1
        self._tv_sirala: dict[int, dict[str, str]] = {}  # {id(tv): {col: "asc"/"desc"}}

        # tk.Tk() her şeyden ÖNCE oluşturulmalı
        self._root = tk.Tk()
        self._root.title(f"Müşteri Kayıt Sistemi  {SURUM}")
        self._root.geometry("990x690")
        self._root.resizable(False, False)
        self._root.configure(bg=C["sb"])

        # StringVar ancak Tk() sonrası yaratılabilir
        self._durum_var = tk.StringVar(value="Hazır")

        self._stil_ayarla()

        self._aktif_frame: tk.Frame | None = None
        self._nav_butonlar: list[tk.Button] = []
        self._ui_kur()

    # ── Stil ─────────────────────────────────────────────────────────────────

    def _stil_ayarla(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("M.Treeview",
                    background=C["t_tek"], foreground=C["etiket_t"],
                    rowheight=34, fieldbackground=C["t_tek"],
                    font=F["nr"], borderwidth=0)
        s.configure("M.Treeview.Heading",
                    background=C["t_head"], foreground=C["t_head_t"],
                    font=F["et"], relief="flat", borderwidth=0)
        s.map("M.Treeview.Heading",
              background=[("active", C["b_m_h"])])
        s.map("M.Treeview",
              background=[("selected", C["t_sec"])],
              foreground=[("selected", C["t_sec_t"])])

    # ── Ana Yerleşim ──────────────────────────────────────────────────────────

    def _ui_kur(self):
        self._sb_kur()

        sag = tk.Frame(self._root, bg=C["bg"])
        sag.pack(side="right", fill="both", expand=True)

        self._icerik = tk.Frame(sag, bg=C["bg"])
        self._icerik.pack(side="top", fill="both", expand=True)

        self._durum_bar_kur(sag)

        # Ekranları oluştur (sıra önemli: self._a_deg gibi değişkenler burada doğar)
        self._fr_ekle     = self._ekle_ekrani()
        self._fr_liste    = self._liste_ekrani()
        self._fr_ara      = self._ara_ekrani()
        self._fr_guncelle = self._guncelle_ekrani()
        self._fr_sil      = self._sil_ekrani()

        self._goster(self._fr_liste, 1)

    # ── Kenar Çubuğu ─────────────────────────────────────────────────────────

    def _sb_kur(self):
        sb = tk.Frame(self._root, bg=C["sb"], width=200)
        sb.pack(side="left", fill="y")
        sb.pack_propagate(False)

        tk.Frame(sb, bg=C["sb"], height=22).pack()
        tk.Label(sb, text="MÜŞTERİ\nKAYIT SİSTEMİ",
                 bg=C["sb"], fg=C["sb_txt"],
                 font=F["logo"], justify="center").pack()
        tk.Frame(sb, bg=C["sb_div"], height=1).pack(fill="x", padx=16, pady=10)

        nav = [
            ("  +  Müşteri Ekle",     self._goster_ekle),
            ("  ≡  Müşteri Listesi",  self._goster_liste),
            ("  ⌕  Ara & Filtrele",  self._goster_ara),
            ("  ✎  Güncelle",         self._goster_guncelle),
            ("  ✕  Sil",              self._goster_sil),
        ]
        for i, (etiket, komut) in enumerate(nav):
            b = tk.Label(
                sb, text=etiket, anchor="w",
                bg=C["sb"], fg=C["sb_txt"],
                font=F["sb"],
                padx=18, pady=12, cursor="hand2",
            )
            b.pack(fill="x")
            b.bind("<Button-1>", lambda e, fn=komut: fn())
            b.bind("<Enter>", lambda e, x=b: x.configure(bg=C["sb_hvr"]))
            b.bind("<Leave>", lambda e, x=b, idx=i:
                   x.configure(bg=C["sb_aktif"] if self._aktif_idx == idx else C["sb"]))
            self._nav_butonlar.append(b)

        tk.Frame(sb, bg=C["sb_div"], height=1).pack(fill="x", padx=16, pady=10)
        tk.Label(sb, text=f"Sürüm  {SURUM}",
                 bg=C["sb"], fg=C["sb_div"], font=F["kk"]).pack(side="bottom", pady=8)

    # ── Durum Çubuğu ─────────────────────────────────────────────────────────

    def _durum_bar_kur(self, ebeveyn: tk.Frame):
        bar = tk.Frame(ebeveyn, bg=C["d_bg"], height=26)
        bar.pack(side="bottom", fill="x")
        bar.pack_propagate(False)
        tk.Label(bar, textvariable=self._durum_var,
                 bg=C["d_bg"], fg=C["d_txt"], font=F["d"]).pack(side="left", padx=10)
        self._durum_sag = tk.Label(bar, text="",
                                    bg=C["d_bg"], fg=C["d_txt"], font=F["d"])
        self._durum_sag.pack(side="right", padx=10)
        self._durum_guncelle()

    def _durum_guncelle(self, mesaj: str = "Hazır"):
        self._durum_var.set(f"  {mesaj}")
        n = len(self._servis.hepsini_getir())
        self._durum_sag.configure(text=f"Toplam: {n} müşteri  |  {SURUM}  ")

    # ── Navigasyon ───────────────────────────────────────────────────────────

    def _goster(self, frame: tk.Frame, indeks: int):
        if self._aktif_frame:
            self._aktif_frame.pack_forget()
        frame.pack(fill="both", expand=True, padx=28, pady=22)
        self._aktif_frame = frame
        self._aktif_idx = indeks
        for i, b in enumerate(self._nav_butonlar):
            b.configure(bg=C["sb_aktif"] if i == indeks else C["sb"])

    def _goster_ekle(self):
        self._goster(self._fr_ekle, 0)

    def _goster_liste(self):
        self._goster(self._fr_liste, 1)
        self._liste_yenile()

    def _goster_ara(self):
        self._goster(self._fr_ara, 2)
        self._a_deg.set("")
        self._a_alan.set("Tüm Alanlar")

    def _goster_guncelle(self):
        self._goster(self._fr_guncelle, 3)
        self._guncelle_liste_yenile()

    def _goster_sil(self):
        self._goster(self._fr_sil, 4)
        self._sil_liste_yenile()

    # ── Yardımcı Widget Üreticiler ────────────────────────────────────────────

    def _baslik(self, ebeveyn: tk.Frame, metin: str):
        tk.Label(ebeveyn, text=metin, bg=C["bg"],
                 fg=C["baslik_t"], font=F["baslik"]).pack(anchor="w")
        tk.Frame(ebeveyn, bg=C["sinir"], height=2).pack(fill="x", pady=(5, 16))

    def _kart_ic(self, ebeveyn: tk.Frame) -> tk.Frame:
        d = tk.Frame(ebeveyn, bg=C["kart"],
                     highlightbackground=C["sinir"], highlightthickness=1)
        d.pack(fill="x")
        ic = tk.Frame(d, bg=C["kart"], padx=22, pady=16)
        ic.pack(fill="x")
        return ic

    def _treeview_olustur(self, ebeveyn: tk.Frame, satirsay: int = 0) -> ttk.Treeview:
        cerceve = tk.Frame(ebeveyn, bg=C["kart"],
                           highlightbackground=C["sinir"], highlightthickness=1)
        if satirsay:
            cerceve.pack(fill="x")
        else:
            cerceve.pack(fill="both", expand=True)

        kw: dict = dict(style="M.Treeview",
                        columns=("id", "ad", "telefon", "eposta"),
                        show="headings", selectmode="browse")
        if satirsay:
            kw["height"] = satirsay

        tv = ttk.Treeview(cerceve, **kw)
        for col, baslik, gen, hiza in SUTUNLAR:
            tv.heading(col, text=baslik,
                       command=lambda c=col, t=tv: self._sutun_sirala(t, c))
            tv.column(col, width=gen, anchor=hiza, minwidth=gen)

        sb_y = ttk.Scrollbar(cerceve, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=sb_y.set)
        tv.pack(side="left", fill="both", expand=True)
        sb_y.pack(side="right", fill="y")

        tv.tag_configure("cift", background=C["t_cift"])
        tv.tag_configure("tek",  background=C["t_tek"])
        self._tv_sirala[id(tv)] = {}
        return tv

    def _tv_doldur(self, tv: ttk.Treeview, liste: list):
        tv.delete(*tv.get_children())
        for i, m in enumerate(liste):
            tv.insert("", "end", iid=str(m.id),
                      values=(m.id, m.ad, m.telefon, m.eposta),
                      tags=("cift" if i % 2 == 0 else "tek",))

    def _sutun_sirala(self, tv: ttk.Treeview, sutun: str):
        """Sütun başlığına tıklanınca artan/azalan sıra — ok göstergesi ile."""
        durum = self._tv_sirala.get(id(tv), {})
        ters = durum.get(sutun) == "asc"

        satirlar = [(tv.set(k, sutun), k) for k in tv.get_children()]
        if sutun == "id":
            satirlar.sort(key=lambda x: int(x[0]) if x[0].isdigit() else 0,
                          reverse=ters)
        else:
            satirlar.sort(key=lambda x: x[0].casefold(), reverse=ters)

        for idx, (_, k) in enumerate(satirlar):
            tv.move(k, "", idx)
            tv.item(k, tags=("cift" if idx % 2 == 0 else "tek",))

        durum[sutun] = "desc" if ters else "asc"
        self._tv_sirala[id(tv)] = durum

        basliklar = {col: bas for col, bas, _, _ in SUTUNLAR}
        for col, bas in basliklar.items():
            ok = (" ▲" if not ters else " ▼") if col == sutun else ""
            tv.heading(col, text=bas + ok,
                       command=lambda c=col, t=tv: self._sutun_sirala(t, c))

    def _form_satiri(self, ebeveyn: tk.Frame, etiket: str,
                     degisken: tk.StringVar, satir: int) -> tk.Entry:
        tk.Label(ebeveyn, text=etiket, bg=C["kart"],
                 fg=C["etiket_t"], font=F["et"]).grid(
                     row=satir, column=0, sticky="w", pady=(10, 2))
        e = tk.Entry(ebeveyn, textvariable=degisken,
                     font=("Helvetica", 11),
                     bg=C["g_bg"], fg=C["g_txt"],
                     relief="flat",
                     highlightbackground=C["g_sinir"],
                     highlightthickness=1,
                     highlightcolor=C["g_odak"],
                     insertbackground=C["g_txt"])
        e.grid(row=satir, column=1, sticky="ew", ipady=8, padx=(10, 0))
        return e

    # ── Doğrulama ─────────────────────────────────────────────────────────────

    def _tel_gecerli(self, tel: str) -> bool:
        return 10 <= len(re.sub(r"\D", "", tel)) <= 11

    def _ep_gecerli(self, ep: str) -> bool:
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$", ep))

    def _dogrula(self, ad: str, tel: str, ep: str) -> bool:
        """Girişleri kontrol eder; hata varsa açıklayıcı mesajla False döner."""
        if len(ad) < 2:
            messagebox.showerror("Geçersiz Ad",
                "Ad Soyad en az 2 karakter olmalıdır.\n\n"
                "Örnek: Ali Yılmaz")
            return False
        if len(ad) > 60:
            messagebox.showerror("Geçersiz Ad",
                "Ad Soyad en fazla 60 karakter olabilir.")
            return False
        if not self._tel_gecerli(tel):
            messagebox.showerror("Geçersiz Telefon",
                "Telefon numarası hatalı.\n\n"
                "• 10 veya 11 haneli olmalıdır\n"
                "• Başında 0 olabilir (05...) ya da olmayabilir (5...)\n"
                "• Boşluk ve tire kabul edilir\n\n"
                "Doğru örnek:  5551234567  veya  0555 123 45 67")
            return False
        if ep and not self._ep_gecerli(ep):
            messagebox.showerror("Geçersiz E-posta",
                "E-posta adresi tanınmıyor.\n\n"
                "• @ işareti bulunmalıdır\n"
                "• Alan adı en az iki karakterli uzantı içermelidir\n\n"
                "Doğru örnek:  kullanici@ornek.com")
            return False
        return True

    # ── Ekle Ekranı ──────────────────────────────────────────────────────────

    def _ekle_ekrani(self) -> tk.Frame:
        f = tk.Frame(self._icerik, bg=C["bg"])
        self._baslik(f, "Yeni Müşteri Ekle")

        ic = self._kart_ic(f)
        ic.columnconfigure(1, weight=1)

        tk.Label(ic, text="  ★ ile işaretli alanlar zorunludur.",
                 bg=C["kart"], fg=C["ipucu_t"], font=F["kk"]).grid(
                     row=0, column=0, columnspan=2, sticky="w", pady=(0, 4))

        self._e_d = {k: tk.StringVar() for k in ("ad", "tel", "ep")}

        for satir, (etiket, key) in enumerate([
            ("Ad Soyad  ★", "ad"),
            ("Telefon   ★", "tel"),
            ("E-posta",     "ep"),
        ], start=1):
            self._form_satiri(ic, etiket, self._e_d[key], satir)

        tk.Label(ic,
                 text="  Telefon formatı: 5XXXXXXXXX veya 05XXXXXXXXX",
                 bg=C["kart"], fg=C["ipucu_t"], font=F["kk"]).grid(
                     row=4, column=0, columnspan=2, sticky="w", pady=(6, 0))

        bc = tk.Frame(ic, bg=C["kart"])
        bc.grid(row=5, column=0, columnspan=2, sticky="w", pady=(16, 0))

        Buton(bc, "  ✓  Kaydet  ",
               C["b_y"], C["b_y_h"], self._musteri_ekle).pack(side="left", padx=(0, 8))
        Buton(bc, "Temizle",
               C["b_g"], C["b_g_h"], self._ekle_temizle,
               font=F["btn_n"]).pack(side="left")
        return f

    # ── Liste Ekranı ──────────────────────────────────────────────────────────

    def _liste_ekrani(self) -> tk.Frame:
        f = tk.Frame(self._icerik, bg=C["bg"])
        self._baslik(f, "Müşteri Listesi")

        ust = tk.Frame(f, bg=C["bg"])
        ust.pack(fill="x", pady=(0, 8))

        self._l_sayac = tk.Label(ust, text="", bg=C["bg"],
                                  fg=C["ipucu_t"], font=F["nr"])
        self._l_sayac.pack(side="left")

        tk.Label(ust, text="  ·  Sütun başlığına tıklayarak sıralayabilirsiniz.",
                 bg=C["bg"], fg=C["ipucu_t"], font=F["kk"]).pack(side="left")

        Buton(ust, " ↺  Yenile ", C["b_m"], C["b_m_h"],
               self._liste_yenile, font=F["btn_n"], py=5).pack(side="right")

        self._l_tv = self._treeview_olustur(f)
        return f

    # ── Ara & Filtrele Ekranı ─────────────────────────────────────────────────

    def _ara_ekrani(self) -> tk.Frame:
        f = tk.Frame(self._icerik, bg=C["bg"])
        self._baslik(f, "Ara & Filtrele")

        ic = self._kart_ic(f)

        # ── Arama satırı ──
        sat = tk.Frame(ic, bg=C["kart"])
        sat.pack(fill="x")

        tk.Label(sat, text="Metin:", bg=C["kart"],
                 fg=C["etiket_t"], font=F["et"]).pack(side="left", padx=(0, 6))

        self._a_deg = tk.StringVar()
        self._a_deg.trace_add("write", lambda *_: self._musteri_ara())

        tk.Entry(sat, textvariable=self._a_deg,
                 font=("Helvetica", 11),
                 bg=C["g_bg"], fg=C["g_txt"],
                 relief="flat",
                 highlightbackground=C["g_sinir"],
                 highlightthickness=1,
                 highlightcolor=C["g_odak"],
                 insertbackground=C["g_txt"]).pack(
                     side="left", fill="x", expand=True, ipady=8, padx=(0, 14))

        # ── Alan filtresi ──
        tk.Label(sat, text="Alan:", bg=C["kart"],
                 fg=C["etiket_t"], font=F["et"]).pack(side="left", padx=(0, 6))

        self._a_alan = tk.StringVar(value="Tüm Alanlar")
        cb = ttk.Combobox(sat, textvariable=self._a_alan,
                          values=["Tüm Alanlar", "Ad Soyad", "Telefon", "E-posta"],
                          state="readonly", width=14, font=F["nr"])
        cb.pack(side="left", ipady=5, padx=(0, 10))
        cb.bind("<<ComboboxSelected>>", lambda *_: self._musteri_ara())

        Buton(sat, " Ara ", C["b_m"], C["b_m_h"],
               self._musteri_ara, font=F["btn_n"], py=6, px=14).pack(side="left", padx=(0, 6))
        Buton(sat, "Temizle", C["b_g"], C["b_g_h"],
               self._ara_temizle, font=F["btn_n"], py=6, px=10).pack(side="left")

        # ── Sonuç etiketi ──
        self._a_sonuc = tk.Label(f, text="Arama yapmak için metin girin.",
                                  bg=C["bg"], fg=C["ipucu_t"], font=F["nr"])
        self._a_sonuc.pack(anchor="w", pady=(10, 6))

        self._a_tv = self._treeview_olustur(f)
        return f

    # ── Güncelle Ekranı ───────────────────────────────────────────────────────

    def _guncelle_ekrani(self) -> tk.Frame:
        f = tk.Frame(self._icerik, bg=C["bg"])
        self._baslik(f, "Müşteri Güncelle")

        tk.Label(f,
                 text="1 — Listeden müşteriyi seçin   "
                      "2 — Bilgileri düzenleyin   "
                      "3 — Güncelle butonuna basın",
                 bg=C["bg"], fg=C["ipucu_t"], font=F["kk"]).pack(
                     anchor="w", pady=(0, 8))

        self._g_tv = self._treeview_olustur(f, satirsay=5)
        self._g_tv.bind("<<TreeviewSelect>>", self._guncelle_secim_degisti)

        tk.Frame(f, bg=C["sinir"], height=2).pack(fill="x", pady=(12, 0))

        # Form kartı
        d = tk.Frame(f, bg=C["kart"],
                     highlightbackground=C["sinir"], highlightthickness=1)
        d.pack(fill="x")
        ic = tk.Frame(d, bg=C["kart"], padx=22, pady=14)
        ic.pack(fill="x")
        ic.columnconfigure(1, weight=1)

        self._g_secid: int = 0
        self._g_d = {k: tk.StringVar() for k in ("ad", "tel", "ep")}

        for satir, (etiket, key) in enumerate([
            ("Ad Soyad  ★", "ad"),
            ("Telefon   ★", "tel"),
            ("E-posta",     "ep"),
        ]):
            self._form_satiri(ic, etiket, self._g_d[key], satir)

        alt = tk.Frame(ic, bg=C["kart"])
        alt.grid(row=3, column=0, columnspan=2, sticky="w", pady=(14, 0))

        self._g_durum = tk.Label(alt,
                                  text="  ↑  Listeden bir müşteri seçilmedi.",
                                  bg=C["kart"], fg=C["ipucu_t"], font=F["kk"])
        self._g_durum.pack(anchor="w", pady=(0, 8))

        bc = tk.Frame(alt, bg=C["kart"])
        bc.pack(anchor="w")

        self._g_btn = Buton(bc, "  ✓  Güncelle  ",
                              C["b_t"], C["b_t_h"], self._musteri_guncelle)
        self._g_btn.pack(side="left", padx=(0, 8))
        self._g_btn.configure(state="disabled")

        Buton(bc, "Seçimi Temizle",
               C["b_g"], C["b_g_h"], self._guncelle_temizle,
               font=F["btn_n"]).pack(side="left")

        return f

    # ── Sil Ekranı ────────────────────────────────────────────────────────────

    def _sil_ekrani(self) -> tk.Frame:
        f = tk.Frame(self._icerik, bg=C["bg"])
        self._baslik(f, "Müşteri Sil")

        tk.Label(f,
                 text="Listeden bir müşteri seçin ve ardından 'Sil' butonuna basın.  "
                      "⚠  Bu işlem geri alınamaz.",
                 bg=C["bg"], fg=C["ipucu_t"], font=F["kk"]).pack(
                     anchor="w", pady=(0, 8))

        self._s_tv = self._treeview_olustur(f)

        alt = tk.Frame(f, bg=C["bg"])
        alt.pack(fill="x", pady=(12, 0))

        Buton(alt, "  ✕  Seçili Müşteriyi Sil  ",
               C["b_k"], C["b_k_h"], self._musteri_sil).pack(side="left")
        Buton(alt, " ↺  Listeyi Yenile ",
               C["b_g"], C["b_g_h"], self._sil_liste_yenile,
               font=F["btn_n"]).pack(side="left", padx=(10, 0))

        return f

    # ── İşlem Metotları ───────────────────────────────────────────────────────

    # --- Ekle ---
    def _musteri_ekle(self):
        ad  = self._e_d["ad"].get().strip()
        tel = self._e_d["tel"].get().strip()
        ep  = self._e_d["ep"].get().strip()
        if not self._dogrula(ad, tel, ep):
            return
        m = self._servis.ekle(ad, tel, ep)
        messagebox.showinfo("Müşteri Eklendi",
                            f"Kayıt başarıyla oluşturuldu.\n\nID: {m.id}\nAd: {m.ad}")
        self._ekle_temizle()
        self._durum_guncelle(f"Yeni müşteri eklendi  →  ID: {m.id}")

    def _ekle_temizle(self):
        for v in self._e_d.values():
            v.set("")

    # --- Listele ---
    def _liste_yenile(self):
        ms = self._servis.hepsini_getir()
        self._l_sayac.configure(text=f"Toplam  {len(ms)}  müşteri")
        self._tv_doldur(self._l_tv, ms)
        self._durum_guncelle("Liste güncellendi")

    # --- Ara & Filtrele ---
    def _musteri_ara(self):
        aranan = self._a_deg.get().strip()
        self._tv_doldur(self._a_tv, [])

        if not aranan:
            self._a_sonuc.configure(
                text="Arama yapmak için metin girin.", fg=C["ipucu_t"])
            return

        alan_map = {
            "Tüm Alanlar": "hepsi",
            "Ad Soyad":    "ad",
            "Telefon":     "telefon",
            "E-posta":     "eposta",
        }
        alan = alan_map.get(self._a_alan.get(), "hepsi")
        bulunanlar = self._servis.filtrele(aranan, alan)

        if bulunanlar:
            self._a_sonuc.configure(
                text=f"  ✓  {len(bulunanlar)} sonuç bulundu.", fg=C["ok"])
        else:
            self._a_sonuc.configure(
                text="  ✕  Eşleşen kayıt bulunamadı.", fg=C["hata"])

        self._tv_doldur(self._a_tv, bulunanlar)
        self._durum_guncelle(
            f"Arama: '{aranan}' [{self._a_alan.get()}]  →  {len(bulunanlar)} sonuç")

    def _ara_temizle(self):
        self._a_deg.set("")
        self._a_alan.set("Tüm Alanlar")
        self._tv_doldur(self._a_tv, [])
        self._a_sonuc.configure(text="Arama yapılmadı.", fg=C["ipucu_t"])

    # --- Güncelle ---
    def _guncelle_liste_yenile(self):
        self._guncelle_temizle()
        self._tv_doldur(self._g_tv, self._servis.hepsini_getir())

    def _guncelle_secim_degisti(self, _event=None):
        sec = self._g_tv.selection()
        if not sec:
            return
        m = self._servis.id_ile_getir(int(sec[0]))
        if not m:
            return
        self._g_secid = m.id
        self._g_d["ad"].set(m.ad)
        self._g_d["tel"].set(m.telefon)
        self._g_d["ep"].set(m.eposta)
        self._g_durum.configure(
            text=f"  ✎  Düzenleniyor: {m.ad}  (ID: {m.id})",
            fg=C["b_t"])
        self._g_btn.configure(state="normal")

    def _guncelle_temizle(self):
        self._g_secid = 0
        for v in self._g_d.values():
            v.set("")
        self._g_durum.configure(
            text="  ↑  Listeden bir müşteri seçilmedi.", fg=C["ipucu_t"])
        self._g_btn.configure(state="disabled")
        for k in self._g_tv.selection():
            self._g_tv.selection_remove(k)

    def _musteri_guncelle(self):
        if not self._g_secid:
            messagebox.showwarning("Seçim Yapılmadı",
                "Lütfen önce listeden güncellenecek müşteriyi seçin.")
            return
        ad  = self._g_d["ad"].get().strip()
        tel = self._g_d["tel"].get().strip()
        ep  = self._g_d["ep"].get().strip()
        if not self._dogrula(ad, tel, ep):
            return
        self._servis.guncelle(self._g_secid, ad, tel, ep)
        messagebox.showinfo("Güncellendi",
                            f"Müşteri bilgileri başarıyla güncellendi.\nID: {self._g_secid}")
        self._durum_guncelle(f"Güncellendi  →  ID: {self._g_secid}")
        self._guncelle_liste_yenile()

    # --- Sil ---
    def _sil_liste_yenile(self):
        self._tv_doldur(self._s_tv, self._servis.hepsini_getir())

    def _musteri_sil(self):
        sec = self._s_tv.selection()
        if not sec:
            messagebox.showwarning("Seçim Yapılmadı",
                "Lütfen listeden silmek istediğiniz müşteriyi seçin.\n"
                "(Bir satıra tıklayarak seçebilirsiniz.)")
            return
        m = self._servis.id_ile_getir(int(sec[0]))
        if not m:
            return
        onay = messagebox.askyesno(
            "Silme Onayı",
            f"Aşağıdaki müşteri kalıcı olarak silinecek:\n\n"
            f"  Ad   : {m.ad}\n"
            f"  Tel  : {m.telefon}\n"
            f"  ID   : {m.id}\n\n"
            "Bu işlem geri alınamaz. Devam etmek istiyor musunuz?",
        )
        if onay:
            self._servis.sil(m.id)
            messagebox.showinfo("Silindi", f"'{m.ad}' adlı müşteri silindi.")
            self._durum_guncelle(f"Silindi  →  {m.ad}  (ID: {m.id})")
            self._sil_liste_yenile()
            self._durum_guncelle()

    # ── Çalıştır ──────────────────────────────────────────────────────────────

    def baslat(self):
        self._root.mainloop()
