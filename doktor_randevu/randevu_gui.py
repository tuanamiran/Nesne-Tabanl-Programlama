import tkinter as tk
from tkinter import messagebox, ttk

from randevu_db import tablolari_olustur, varsayilan_doktorlari_ekle
from randevu_system import Doktor, Hasta, Randevu


class RandevuArayuzu:
    def __init__(self, root):
        self.root = root
        self.root.title("online doktor randevu sistemi")
        self.root.geometry("900x600")

        tablolari_olustur()
        varsayilan_doktorlari_ekle()

        self._arayuzu_hazirla()
        self._doktor_listesini_yukle()

    def _arayuzu_hazirla(self):
        ana_cerceve = ttk.Frame(self.root, padding=16)
        ana_cerceve.pack(fill="both", expand=True)

        form_cerceve = ttk.LabelFrame(ana_cerceve, text="hasta kayit ve randevu alma", padding=12)
        form_cerceve.pack(fill="x", pady=(0, 16))

        ttk.Label(form_cerceve, text="ad soyad").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ad_entry = ttk.Entry(form_cerceve, width=30)
        self.ad_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_cerceve, text="tc").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.tc_entry = ttk.Entry(form_cerceve, width=30)
        self.tc_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_cerceve, text="telefon").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.telefon_entry = ttk.Entry(form_cerceve, width=30)
        self.telefon_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_cerceve, text="tarih").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.tarih_entry = ttk.Entry(form_cerceve, width=30)
        self.tarih_entry.insert(0, "2026-04-18")
        self.tarih_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_cerceve, text="saat").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.saat_entry = ttk.Entry(form_cerceve, width=30)
        self.saat_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(form_cerceve, text="doktor").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.doktor_combobox = ttk.Combobox(form_cerceve, state="readonly", width=27)
        self.doktor_combobox.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        buton_cerceve = ttk.Frame(form_cerceve)
        buton_cerceve.grid(row=6, column=0, columnspan=2, sticky="w", padx=5, pady=(10, 0))

        ttk.Button(buton_cerceve, text="randevu al", command=self.randevu_al).pack(side="left", padx=(0, 10))
        ttk.Button(buton_cerceve, text="randevularimi getir", command=self.randevulari_listele).pack(side="left")

        form_cerceve.columnconfigure(1, weight=1)

        liste_cerceve = ttk.LabelFrame(ana_cerceve, text="doktor uygunluk listesi", padding=12)
        liste_cerceve.pack(fill="both", expand=True)

        self.doktor_listesi = ttk.Treeview(
            liste_cerceve,
            columns=("id", "ad", "uzmanlik", "uygun_saatler"),
            show="headings",
            height=8,
        )
        self.doktor_listesi.heading("id", text="id")
        self.doktor_listesi.heading("ad", text="doktor")
        self.doktor_listesi.heading("uzmanlik", text="uzmanlik")
        self.doktor_listesi.heading("uygun_saatler", text="uygun saatler")
        self.doktor_listesi.column("id", width=50, anchor="center")
        self.doktor_listesi.column("ad", width=180)
        self.doktor_listesi.column("uzmanlik", width=160)
        self.doktor_listesi.column("uygun_saatler", width=250)
        self.doktor_listesi.pack(fill="both", expand=True)

        ttk.Label(liste_cerceve, text="hasta tc ile randevulari gosterilir; saat bilgisini uygun saatlerden giriniz.").pack(
            anchor="w", pady=(10, 0)
        )

        randevu_cerceve = ttk.LabelFrame(ana_cerceve, text="hasta randevulari", padding=12)
        randevu_cerceve.pack(fill="both", expand=True, pady=(16, 0))

        self.randevu_listesi = ttk.Treeview(
            randevu_cerceve,
            columns=("randevu_id", "doktor", "uzmanlik", "tarih", "saat"),
            show="headings",
            height=8,
        )
        self.randevu_listesi.heading("randevu_id", text="randevu id")
        self.randevu_listesi.heading("doktor", text="doktor")
        self.randevu_listesi.heading("uzmanlik", text="uzmanlik")
        self.randevu_listesi.heading("tarih", text="tarih")
        self.randevu_listesi.heading("saat", text="saat")
        self.randevu_listesi.column("randevu_id", width=90, anchor="center")
        self.randevu_listesi.pack(fill="both", expand=True)

        ttk.Button(ana_cerceve, text="secili randevuyu iptal et", command=self.randevu_iptal).pack(anchor="e", pady=(12, 0))

    def _doktor_listesini_yukle(self):
        for item in self.doktor_listesi.get_children():
            self.doktor_listesi.delete(item)

        doktorlar = Doktor.tum_doktorlari_getir()
        combobox_degerleri = []

        for doktor_id, ad, uzmanlik, uygun_saatler in doktorlar:
            self.doktor_listesi.insert("", "end", values=(doktor_id, ad, uzmanlik, uygun_saatler))
            combobox_degerleri.append(f"{doktor_id} - {ad} - {uzmanlik}")

        self.doktor_combobox["values"] = combobox_degerleri
        if combobox_degerleri:
            self.doktor_combobox.current(0)

    def randevu_al(self):
        ad = self.ad_entry.get().strip()
        tc = self.tc_entry.get().strip()
        telefon = self.telefon_entry.get().strip()
        tarih = self.tarih_entry.get().strip()
        saat = self.saat_entry.get().strip()
        doktor_secimi = self.doktor_combobox.get().strip()

        if not all([ad, tc, telefon, tarih, saat, doktor_secimi]):
            messagebox.showwarning("uyari", "lutfen tum alanlari doldurun")
            return

        doktor_id = int(doktor_secimi.split(" - ")[0])
        hasta = Hasta(ad, tc, telefon)
        basarili, mesaj = hasta.randevu_al(doktor_id, tarih, saat)

        if basarili:
            messagebox.showinfo("bilgi", mesaj)
            self.randevulari_listele()
        else:
            messagebox.showerror("hata", mesaj)

    def randevulari_listele(self):
        tc = self.tc_entry.get().strip()
        if not tc:
            messagebox.showwarning("uyari", "randevulari listelemek icin tc giriniz")
            return

        for item in self.randevu_listesi.get_children():
            self.randevu_listesi.delete(item)

        randevular = Randevu.hastanin_randevularini_getir(tc)
        for randevu in randevular:
            self.randevu_listesi.insert("", "end", values=randevu)

    def randevu_iptal(self):
        secili_oge = self.randevu_listesi.selection()
        if not secili_oge:
            messagebox.showwarning("uyari", "iptal icin once bir randevu seciniz")
            return

        randevu_id = self.randevu_listesi.item(secili_oge[0], "values")[0]
        basarili, mesaj = Randevu.randevu_iptal(randevu_id)

        if basarili:
            messagebox.showinfo("bilgi", mesaj)
            self.randevulari_listele()
        else:
            messagebox.showerror("hata", mesaj)


def uygulamayi_baslat():
    root = tk.Tk()
    RandevuArayuzu(root)
    root.mainloop()


if __name__ == "__main__":
    uygulamayi_baslat()
