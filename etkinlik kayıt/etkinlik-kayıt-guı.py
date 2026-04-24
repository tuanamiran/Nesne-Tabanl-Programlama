import tkinter as tk
from tkinter import messagebox, ttk

# --- MANTIK KATMANI (OOP) ---
class Katilimci:
    def __init__(self, ad, yas):
        self.ad = ad
        self.yas = yas

class Etkinlik:
    def __init__(self, ad, kapasite, yas_siniri, fiyat_s, fiyat_v, min_kat):
        self.ad = ad
        self.kapasite = kapasite
        self.yas_siniri = yas_siniri
        self.fiyat_s = fiyat_s
        self.fiyat_v = fiyat_v
        self.min_kat = min_kat
        self.katilimcilar = []
        self.gelir = 0

    def ekle(self, k, tur):
        if k.yas < self.yas_siniri:
            return False, f"🚫 Yaş sınırı +{self.yas_siniri}!"
        if len(self.katilimcilar) >= self.kapasite:
            return False, "❌ Kapasite dolu!"
        self.katilimcilar.append(k)
        self.gelir += self.fiyat_v if tur == "VIP" else self.fiyat_s
        return True, f"✅ {k.ad} kaydedildi!"

# --- ŞATAFATLI GUI TASARIMI ---
class EtkinlikApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Premium Event Management v2.0")
        self.root.geometry("450x650")
        self.root.configure(bg="#f0f2f5") # Modern hafif gri arka plan

        # Üst Başlık Paneli
        header = tk.Frame(self.root, bg="#2c3e50", height=80)
        header.pack(fill="x", side="top")
        tk.Label(header, text="🌟 EVENT PRO MANAGER", font=("Helvetica", 16, "bold"), 
                 bg="#2c3e50", fg="white").pack(pady=20)

        # 1. BÖLÜM: ETKİNLİK AYARLARI (ADMIN)
        self.setup_frame = tk.LabelFrame(self.root, text=" ⚙️ Etkinlik Kurulumu ", font=("Arial", 10, "bold"),
                                         bg="white", padx=20, pady=15, relief="flat", bd=2)
        self.setup_frame.pack(pady=20, padx=20, fill="x")

        tk.Label(self.setup_frame, text="Etkinlik Adı:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.ent_ad = tk.Entry(self.setup_frame, font=("Arial", 10), bd=1, relief="solid")
        self.ent_ad.grid(row=0, column=1, columnspan=2, sticky="ew", pady=5)

        tk.Label(self.setup_frame, text="Kapasite:", bg="white").grid(row=1, column=0, sticky="w")
        self.ent_kap = tk.Entry(self.setup_frame, width=8, font=("Arial", 10), bd=1, relief="solid")
        self.ent_kap.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(self.setup_frame, text="Yaş Sınırı:", bg="white").grid(row=1, column=2, sticky="e")
        self.ent_yas = tk.Entry(self.setup_frame, width=8, font=("Arial", 10), bd=1, relief="solid")
        self.ent_yas.grid(row=1, column=3, sticky="w", pady=5)

        self.btn_start = tk.Button(self.setup_frame, text="SİSTEMİ AKTİF ET", command=self.sistemi_kur, 
                                   bg="#27ae60", fg="white", font=("Arial", 10, "bold"), 
                                   relief="flat", cursor="hand2", pady=5)
        self.btn_start.grid(row=2, column=0, columnspan=4, sticky="ew", pady=10)

        # 2. BÖLÜM: BİLET SATIŞ (MÜŞTERİ) - Başlangıçta pasif durabilir
        self.sale_frame = tk.LabelFrame(self.root, text=" 🎫 Bilet Satış Noktası ", font=("Arial", 10, "bold"),
                                        bg="white", padx=20, pady=15, relief="flat", bd=2)
        
        # Stil Ayarları
        style = ttk.Style()
        style.theme_use('clam')

    def sistemi_kur(self):
        try:
            self.etkinlik = Etkinlik(self.ent_ad.get(), int(self.ent_kap.get()), 
                                     int(self.ent_yas.get()), 500, 1500, 12)
            messagebox.showinfo("Sistem", f"🚀 {self.etkinlik.ad} için satışlar başladı!")
            self.btn_start.config(state="disabled", bg="#bdc3c7")
            self.bilet_ekrani()
        except:
            messagebox.showerror("Hata", "Lütfen tüm alanları rakamla doldurun!")

    def bilet_ekrani(self):
        self.sale_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(self.sale_frame, text="Müşteri Adı:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.m_ad = tk.Entry(self.sale_frame, font=("Arial", 10), bd=1, relief="solid")
        self.m_ad.grid(row=0, column=1, sticky="ew", pady=5)

        tk.Label(self.sale_frame, text="Yaşı:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.m_yas = tk.Entry(self.sale_frame, font=("Arial", 10), bd=1, relief="solid")
        self.m_yas.grid(row=1, column=1, sticky="w", pady=5)

        tk.Label(self.sale_frame, text="Bilet Tipi:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.tur = ttk.Combobox(self.sale_frame, values=["Standart", "VIP"], state="readonly")
        self.tur.set("Standart")
        self.tur.grid(row=2, column=1, sticky="ew", pady=5)

        # Aksiyon Butonları
        btn_box = tk.Frame(self.sale_frame, bg="white")
        btn_box.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(btn_box, text="BİLET KES", command=self.bilet_kes, bg="#2980b9", fg="white", 
                  font=("Arial", 10, "bold"), width=12, relief="flat").pack(side="left", padx=5)
        
        tk.Button(btn_box, text="DURUM RAPORU", command=self.rapor, bg="#8e44ad", fg="white", 
                  font=("Arial", 10, "bold"), width=12, relief="flat").pack(side="left", padx=5)

    def bilet_kes(self):
        try:
            k = Katilimci(self.m_ad.get(), int(self.m_yas.get()))
            basari, mesaj = self.etkinlik.ekle(k, self.tur.get())
            if basari:
                messagebox.showinfo("Onay", mesaj)
                self.m_ad.delete(0, tk.END)
                self.m_yas.delete(0, tk.END)
            else:
                messagebox.showwarning("Red", mesaj)
        except:
            messagebox.showerror("Hata", "Bilgileri kontrol edin!")

    def rapor(self):
        kalan = self.etkinlik.kapasite - len(self.etkinlik.katilimcilar)
        status = "✅ GÜVENLİ" if len(self.etkinlik.katilimcilar) >= 12 else "⚠️ RİSKLİ (İPTAL OLABİLİR)"
        
        report_window = tk.Toplevel(self.root)
        report_window.title("Etkinlik Analiz Raporu")
        report_window.geometry("300x250")
        report_window.configure(bg="white")

        tk.Label(report_window, text="📊 SATIŞ ANALİZİ", font=("Arial", 12, "bold"), bg="white", pady=10).pack()
        tk.Label(report_window, text=f"Etkinlik: {self.etkinlik.ad}", bg="white").pack()
        tk.Label(report_window, text=f"Toplam Katılımcı: {len(self.etkinlik.katilimcilar)}", bg="white").pack()
        tk.Label(report_window, text=f"Kalan Kontenjan: {kalan}", bg="white").pack()
        tk.Label(report_window, text=f"Toplam Hasılat: {self.etkinlik.gelir} TL", font=("Arial", 10, "bold"), fg="#27ae60", bg="white").pack(pady=10)
        tk.Label(report_window, text=status, font=("Arial", 9, "italic"), fg="red" if "RİSKLİ" in status else "green", bg="white").pack()

root = tk.Tk()
app = EtkinlikApp(root)
root.mainloop()