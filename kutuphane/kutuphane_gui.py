import tkinter as tk
from tkinter import messagebox, ttk

import kutuphane_db
from kutuphane_system import Kitap, Uye, sistemi_hazirla


class KutuphaneGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("dijital kutuphane sistemi")
        self.root.geometry("1180x720")
        self.root.minsize(1024, 640)

        sistemi_hazirla()
        self.renkler = {
            "arka_plan": "#eef4f8",
            "kart": "#ffffff",
            "vurgu": "#2da6d7",
            "vurgu_koyu": "#15739a",
            "metin": "#213547",
            "ikincil_metin": "#6e8193",
            "cizgi": "#d7e4ee",
            "durum_musait": "#dff6ea",
            "durum_musait_metin": "#16784c",
            "durum_oduncte": "#ffe8d8",
            "durum_oduncte_metin": "#a85b21",
        }
        self.stil_olustur()
        self.arayuzu_olustur()
        self.uyeleri_yukle()
        self.kitaplari_yukle()

    def stil_olustur(self):
        style = ttk.Style()
        style.theme_use("clam")

        self.root.configure(bg=self.renkler["arka_plan"])

        style.configure("App.TFrame", background=self.renkler["arka_plan"])
        style.configure("Card.TFrame", background=self.renkler["kart"])
        style.configure(
            "Header.TLabel",
            background=self.renkler["arka_plan"],
            foreground=self.renkler["metin"],
            font=("Segoe UI", 24, "bold"),
        )
        style.configure(
            "SubHeader.TLabel",
            background=self.renkler["arka_plan"],
            foreground=self.renkler["ikincil_metin"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "CardTitle.TLabel",
            background=self.renkler["kart"],
            foreground=self.renkler["metin"],
            font=("Segoe UI", 14, "bold"),
        )
        style.configure(
            "CardText.TLabel",
            background=self.renkler["kart"],
            foreground=self.renkler["ikincil_metin"],
            font=("Segoe UI", 10),
        )
        style.configure(
            "Highlight.TLabel",
            background=self.renkler["kart"],
            foreground=self.renkler["vurgu_koyu"],
            font=("Segoe UI", 12, "bold"),
        )
        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="#ffffff",
            background=self.renkler["vurgu"],
            borderwidth=0,
            focusthickness=0,
            padding=(14, 10),
        )
        style.map(
            "Primary.TButton",
            background=[
                ("active", self.renkler["vurgu_koyu"]),
                ("pressed", self.renkler["vurgu_koyu"]),
            ],
        )
        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground=self.renkler["vurgu_koyu"],
            background="#dff2fa",
            borderwidth=0,
            focusthickness=0,
            padding=(14, 10),
        )
        style.map(
            "Secondary.TButton",
            background=[
                ("active", "#c4e8f7"),
                ("pressed", "#c4e8f7"),
            ],
        )
        style.configure(
            "Light.TButton",
            font=("Segoe UI", 10),
            foreground=self.renkler["metin"],
            background=self.renkler["kart"],
            borderwidth=1,
            relief="solid",
            padding=(12, 9),
        )
        style.map(
            "Light.TButton",
            background=[("active", "#f4f8fb"), ("pressed", "#f4f8fb")],
            bordercolor=[("!disabled", self.renkler["cizgi"])],
        )
        style.configure(
            "Search.TEntry",
            fieldbackground="#f7fafc",
            background="#f7fafc",
            foreground=self.renkler["metin"],
            bordercolor=self.renkler["cizgi"],
            lightcolor=self.renkler["cizgi"],
            darkcolor=self.renkler["cizgi"],
            padding=8,
        )
        style.configure(
            "Library.Treeview",
            background=self.renkler["kart"],
            fieldbackground=self.renkler["kart"],
            foreground=self.renkler["metin"],
            rowheight=34,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Library.Treeview.Heading",
            background="#f4f8fb",
            foreground=self.renkler["metin"],
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
            padding=8,
        )
        style.map(
            "Library.Treeview",
            background=[("selected", "#d9eef8")],
            foreground=[("selected", self.renkler["metin"])],
        )
        style.configure(
            "Library.TCombobox",
            fieldbackground="#f7fafc",
            background="#f7fafc",
            foreground=self.renkler["metin"],
            bordercolor=self.renkler["cizgi"],
            lightcolor=self.renkler["cizgi"],
            darkcolor=self.renkler["cizgi"],
            padding=6,
        )

    def arayuzu_olustur(self):
        ana_cerceve = ttk.Frame(self.root, style="App.TFrame", padding=20)
        ana_cerceve.pack(fill="both", expand=True)

        self.ust_bar_olustur(ana_cerceve)
        self.ozet_kartlari_olustur(ana_cerceve)
        self.icerik_alani_olustur(ana_cerceve)
        self.alt_aksiyonlar_olustur(ana_cerceve)

    def ust_bar_olustur(self, parent):
        ust = ttk.Frame(parent, style="App.TFrame")
        ust.pack(fill="x")
        ust.columnconfigure(0, weight=1)

        sol = ttk.Frame(ust, style="App.TFrame")
        sol.grid(row=0, column=0, sticky="w")

        ttk.Label(sol, text="Dijital Kutuphane", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            sol,
            text="Kitaplari yonetin, odunc hareketlerini takip edin ve kutuphane akisina hiz kazandirin.",
            style="SubHeader.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        sag = ttk.Frame(ust, style="App.TFrame")
        sag.grid(row=0, column=1, sticky="e")

        self.ara_var = tk.StringVar()
        ara_girisi = ttk.Entry(sag, textvariable=self.ara_var, width=28, style="Search.TEntry")
        ara_girisi.pack(side="left", padx=(0, 8))
        ara_girisi.bind("<KeyRelease>", self.kitaplari_yukle)

        ttk.Button(
            sag,
            text="Listeyi Yenile",
            style="Light.TButton",
            command=self.kitaplari_yukle,
        ).pack(side="left")

    def ozet_kartlari_olustur(self, parent):
        ozet = ttk.Frame(parent, style="App.TFrame")
        ozet.pack(fill="x", pady=(18, 18))

        self.toplam_kitap_var = tk.StringVar(value="0")
        self.musait_kitap_var = tk.StringVar(value="0")
        self.oduncteki_kitap_var = tk.StringVar(value="0")

        self.ozet_karti_olustur(
            ozet,
            "Toplam Kitap",
            self.toplam_kitap_var,
            "Sistemdeki tum kayitli eserler",
        ).pack(side="left", fill="x", expand=True)
        self.ozet_karti_olustur(
            ozet,
            "Musait Kitap",
            self.musait_kitap_var,
            "Hemen odunc verilebilecek kitaplar",
        ).pack(side="left", fill="x", expand=True, padx=12)
        self.ozet_karti_olustur(
            ozet,
            "Oduncteki Kitap",
            self.oduncteki_kitap_var,
            "Uyelerde bulunan aktif oduncler",
        ).pack(side="left", fill="x", expand=True)

    def ozet_karti_olustur(self, parent, baslik, degisken, aciklama):
        kart = ttk.Frame(parent, style="Card.TFrame", padding=16)

        ttk.Label(kart, text=baslik, style="CardText.TLabel").pack(anchor="w")
        ttk.Label(kart, textvariable=degisken, style="Header.TLabel").pack(anchor="w", pady=(4, 2))
        ttk.Label(kart, text=aciklama, style="CardText.TLabel").pack(anchor="w")

        return kart

    def icerik_alani_olustur(self, parent):
        icerik = ttk.Frame(parent, style="App.TFrame")
        icerik.pack(fill="both", expand=True)

        sol = ttk.Frame(icerik, style="Card.TFrame", padding=16)
        sol.pack(side="left", fill="both", expand=True)

        sag = ttk.Frame(icerik, style="Card.TFrame", padding=18)
        sag.pack(side="left", fill="y", padx=(16, 0))

        self.kitap_tablosu_olustur(sol)
        self.detay_paneli_olustur(sag)

    def kitap_tablosu_olustur(self, parent):
        ust_satir = ttk.Frame(parent, style="Card.TFrame")
        ust_satir.pack(fill="x", pady=(0, 12))
        ust_satir.columnconfigure(0, weight=1)

        ttk.Label(ust_satir, text="Kitap Koleksiyonu", style="CardTitle.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            ust_satir,
            text="Secili kitap bilgisi sag panelde gorunur.",
            style="CardText.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        tablo_kapsayici = ttk.Frame(parent, style="Card.TFrame")
        tablo_kapsayici.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            tablo_kapsayici,
            columns=("kitap_id", "ad", "yazar", "kategori", "durum"),
            show="headings",
            height=14,
            style="Library.Treeview",
        )
        self.tree.heading("kitap_id", text="id")
        self.tree.heading("ad", text="kitap adi")
        self.tree.heading("yazar", text="yazar")
        self.tree.heading("kategori", text="kategori")
        self.tree.heading("durum", text="durum")

        self.tree.column("kitap_id", width=60, anchor="center")
        self.tree.column("ad", width=250)
        self.tree.column("yazar", width=180)
        self.tree.column("kategori", width=150)
        self.tree.column("durum", width=110, anchor="center")

        kaydirma = ttk.Scrollbar(tablo_kapsayici, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=kaydirma.set)
        self.tree.bind("<<TreeviewSelect>>", self.detay_guncelle)

        self.tree.pack(side="left", fill="both", expand=True)
        kaydirma.pack(side="right", fill="y")

    def detay_paneli_olustur(self, parent):
        parent.configure(width=300)
        parent.pack_propagate(False)

        ttk.Label(parent, text="Kitap Detayi", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(
            parent,
            text="Tablodan bir kitap sectiginizde temel bilgiler burada guncellenir.",
            style="CardText.TLabel",
            wraplength=250,
        ).pack(anchor="w", pady=(4, 18))

        self.detay_ad = self.detay_satiri_olustur(parent, "Ad")
        self.detay_yazar = self.detay_satiri_olustur(parent, "Yazar")
        self.detay_kategori = self.detay_satiri_olustur(parent, "Kategori")
        self.detay_durum = self.detay_satiri_olustur(parent, "Durum")

        ttk.Separator(parent).pack(fill="x", pady=16)

        ttk.Label(parent, text="Durum Gosterimi", style="CardTitle.TLabel").pack(anchor="w")
        self.durum_etiketi = tk.Label(
            parent,
            text="Secim yok",
            bg=self.renkler["durum_musait"],
            fg=self.renkler["durum_musait_metin"],
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
        )
        self.durum_etiketi.pack(anchor="w", pady=(10, 16))

        ttk.Label(parent, text="Secili Uye", style="CardTitle.TLabel").pack(anchor="w")
        self.uye_combobox = ttk.Combobox(
            parent,
            state="readonly",
            width=32,
            style="Library.TCombobox",
        )
        self.uye_combobox.pack(fill="x", pady=(10, 18))

        ttk.Label(parent, text="Hizli Islemler", style="CardTitle.TLabel").pack(anchor="w")
        ttk.Button(
            parent,
            text="Kitap Odunc Al",
            style="Primary.TButton",
            command=self.kitap_odunc_al,
        ).pack(fill="x", pady=(10, 8))
        ttk.Button(
            parent,
            text="Kitap Iade Et",
            style="Secondary.TButton",
            command=self.kitap_iade_et,
        ).pack(fill="x")

    def detay_satiri_olustur(self, parent, etiket):
        kapsayici = ttk.Frame(parent, style="Card.TFrame")
        kapsayici.pack(fill="x", pady=4)

        ttk.Label(kapsayici, text=etiket, style="CardText.TLabel").pack(anchor="w")
        deger = ttk.Label(kapsayici, text="-", style="Highlight.TLabel")
        deger.pack(anchor="w", pady=(2, 6))
        return deger

    def alt_aksiyonlar_olustur(self, parent):
        alt = ttk.Frame(parent, style="App.TFrame")
        alt.pack(fill="x", pady=(16, 0))

        ttk.Label(
            alt,
            text="Ipuclari: arama kutusuyla kitap adi, yazar veya kategoriye gore filtreleme yapabilirsin.",
            style="SubHeader.TLabel",
        ).pack(side="left")

        ttk.Button(
            alt,
            text="Tum Kayitlari Goster",
            style="Light.TButton",
            command=self.aramayi_temizle,
        ).pack(side="right")

    def aramayi_temizle(self):
        self.ara_var.set("")
        self.kitaplari_yukle()

    def kitaplari_yukle(self):
        arama_metni = self.ara_var.get().strip().lower() if hasattr(self, "ara_var") else ""
        for satir in self.tree.get_children():
            self.tree.delete(satir)

        kitaplar = Kitap.tum_kitaplari_getir()

        for kitap in kitaplar:
            if arama_metni and not any(
                arama_metni in str(deger).lower() for deger in kitap[1:4]
            ):
                continue
            self.tree.insert("", "end", values=kitap)

        self.ozetleri_guncelle(kitaplar)
        self.detay_secimini_koru_veya_sifirla()

    def ozetleri_guncelle(self, kitaplar):
        toplam = len(kitaplar)
        musait = sum(1 for kitap in kitaplar if kitap[4] == "musait")
        oduncte = sum(1 for kitap in kitaplar if kitap[4] != "musait")

        self.toplam_kitap_var.set(str(toplam))
        self.musait_kitap_var.set(str(musait))
        self.oduncteki_kitap_var.set(str(oduncte))

    def detay_secimini_koru_veya_sifirla(self):
        cocuklar = self.tree.get_children()
        if not cocuklar:
            self.detay_alanlarini_temizle()
            return

        mevcut_secim = self.tree.selection()
        if mevcut_secim:
            self.detay_guncelle()
            return

        ilk = cocuklar[0]
        self.tree.selection_set(ilk)
        self.tree.focus(ilk)
        self.detay_guncelle()

    def uyeleri_yukle(self):
        self.uye_haritasi = {}
        gorunen_degerler = []

        for uye_id, ad, email in Uye.tum_uyeleri_getir():
            etiket = f"{uye_id} - {ad} ({email})"
            self.uye_haritasi[etiket] = uye_id
            gorunen_degerler.append(etiket)

        self.uye_combobox["values"] = gorunen_degerler
        if gorunen_degerler:
            self.uye_combobox.current(0)

    def detay_alanlarini_temizle(self):
        self.detay_ad.configure(text="-")
        self.detay_yazar.configure(text="-")
        self.detay_kategori.configure(text="-")
        self.detay_durum.configure(text="-")
        self.durum_etiketi.configure(
            text="Secim yok",
            bg=self.renkler["durum_musait"],
            fg=self.renkler["durum_musait_metin"],
        )

    def detay_guncelle(self, event=None):
        secim = self.tree.selection()
        if not secim:
            self.detay_alanlarini_temizle()
            return

        kitap = self.tree.item(secim[0], "values")
        durum = kitap[4]

        self.detay_ad.configure(text=kitap[1])
        self.detay_yazar.configure(text=kitap[2])
        self.detay_kategori.configure(text=kitap[3])
        self.detay_durum.configure(text=durum)

        if durum == "musait":
            arka_plan = self.renkler["durum_musait"]
            yazi = self.renkler["durum_musait_metin"]
        else:
            arka_plan = self.renkler["durum_oduncte"]
            yazi = self.renkler["durum_oduncte_metin"]

        self.durum_etiketi.configure(
            text=durum.upper(),
            bg=arka_plan,
            fg=yazi,
        )

    def secili_kitap_id(self):
        secim = self.tree.selection()
        if not secim:
            raise ValueError("lutfen listeden bir kitap secin")

        return int(self.tree.item(secim[0], "values")[0])

    def secili_uye(self):
        secili_etiket = self.uye_combobox.get()
        if not secili_etiket:
            raise ValueError("lutfen bir uye secin")

        uye_id = self.uye_haritasi[secili_etiket]
        uye = Uye.uye_getir(uye_id)
        if uye is None:
            raise ValueError("uye bulunamadi")

        return uye

    def kitap_odunc_al(self):
        try:
            kitap_id = self.secili_kitap_id()
            uye = self.secili_uye()
            uye.kitap_odunc_al(kitap_id)
            self.kitaplari_yukle()
            self.detay_guncelle()
            messagebox.showinfo("basarili", "kitap odunc verildi")
        except Exception as hata:
            messagebox.showerror("hata", str(hata))

    def kitap_iade_et(self):
        try:
            kitap_id = self.secili_kitap_id()
            uye = self.secili_uye()
            uye.kitap_iade_et(kitap_id)
            self.kitaplari_yukle()
            self.detay_guncelle()
            messagebox.showinfo("basarili", "kitap iade alindi")
        except Exception as hata:
            messagebox.showerror("hata", str(hata))


def uygulamayi_baslat():
    kutuphane_db.tablo_olustur()
    kutuphane_db.varsayilan_verileri_ekle()

    root = tk.Tk()
    uygulama = KutuphaneGUI(root)
    uygulama.kitaplari_yukle()
    root.mainloop()


if __name__ == "__main__":
    uygulamayi_baslat()
