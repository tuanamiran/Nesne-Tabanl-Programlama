import tkinter as tk
from tkinter import messagebox, ttk

# --- 1. MANTIK KATMANI (OOP) ---
class SeyahatPlan:
    def __init__(self, rota, gun, otel_fiyat, arac_fiyat):
        self.rota = rota
        self.gun = gun
        self.otel_fiyat = otel_fiyat
        self.arac_fiyat = arac_fiyat

    def butce_hesapla(self):
        # 4 gün gezen biri 3 gece otelde kalır kuralı:
        gece_sayisi = self.gun - 1 if self.gun > 0 else 0
        
        toplam_konaklama = gece_sayisi * self.otel_fiyat
        toplam_ulasim = self.gun * self.arac_fiyat
        genel_toplam = toplam_konaklama + toplam_ulasim
        
        return gece_sayisi, toplam_konaklama, toplam_ulasim, genel_toplam

# --- 2. ŞATAFATLI GUI TASARIMI ---
class SeyahatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Master Pro v2.1")
        self.root.geometry("450x600")
        self.root.configure(bg="#f8f9fa")

        # Üst Başlık
        header = tk.Frame(self.root, bg="#1a5f7a", height=100)
        header.pack(fill="x", side="top")
        tk.Label(header, text="🌍 TRAVEL MASTER PRO", font=("Trebuchet MS", 18, "bold"), 
                 bg="#1a5f7a", fg="white").pack(pady=25)

        # 📍 ROTA BİLGİLERİ KUTUSU
        self.rota_frame = tk.LabelFrame(self.root, text=" 📍 Rota ve Süre ", font=("Arial", 10, "bold"),
                                        bg="white", padx=15, pady=10, relief="flat", bd=2)
        self.rota_frame.pack(pady=15, padx=20, fill="x")

        tk.Label(self.rota_frame, text="Rota (Nereden -> Nereye):", bg="white").pack(anchor="w")
        self.ent_rota = tk.Entry(self.rota_frame, font=("Arial", 10), bd=1, relief="solid")
        self.ent_rota.pack(fill="x", pady=5)
        self.ent_rota.insert(0, "İstanbul -> Trabzon") # VARSAYILAN ROTA

        tk.Label(self.rota_frame, text="Toplam Kaç Gün?:", bg="white").pack(anchor="w")
        self.ent_gun = tk.Entry(self.rota_frame, font=("Arial", 10), bd=1, relief="solid")
        self.ent_gun.pack(fill="x", pady=5)
        self.ent_gun.insert(0, "4") # VARSAYILAN GÜN

        # 💸 MALİYET AYARLARI KUTUSU
        self.maliyet_frame = tk.LabelFrame(self.root, text=" 💸 Günlük Birim Fiyatlar ", font=("Arial", 10, "bold"),
                                           bg="white", padx=15, pady=10, relief="flat", bd=2)
        self.maliyet_frame.pack(pady=10, padx=20, fill="x")

        # Yan yana dizilim için iç frame
        m_inner = tk.Frame(self.maliyet_frame, bg="white")
        m_inner.pack()

        # Otel Fiyatı
        otel_box = tk.Frame(m_inner, bg="white")
        otel_box.pack(side="left", padx=10)
        tk.Label(otel_box, text="Otel (Gecelik ₺):", bg="white").pack()
        self.ent_otel = tk.Entry(otel_box, width=12, font=("Arial", 10, "bold"), bd=1, relief="solid", fg="#2980b9")
        self.ent_otel.pack()
        self.ent_otel.insert(0, "6600") # ESKİ KODDAKİ OTEL FİYATI

        # Araç Fiyatı
        arac_box = tk.Frame(m_inner, bg="white")
        arac_box.pack(side="left", padx=10)
        tk.Label(arac_box, text="Araç (Günlük ₺):", bg="white").pack()
        self.ent_arac = tk.Entry(arac_box, width=12, font=("Arial", 10, "bold"), bd=1, relief="solid", fg="#27ae60")
        self.ent_arac.pack()
        self.ent_arac.insert(0, "1500") # ESKİ KODDAKİ ARAÇ FİYATI

        # 🚀 HESAPLA BUTONU
        self.btn_hesapla = tk.Button(self.root, text="PLAN ÖZETİNİ GÖSTER", command=self.plan_hesapla,
                                     bg="#1a5f7a", fg="white", font=("Arial", 12, "bold"),
                                     relief="flat", pady=12, cursor="hand2")
        self.btn_hesapla.pack(pady=30, padx=20, fill="x")

    def plan_hesapla(self):
        try:
            # Kullanıcının girdiği verilerle Plan nesnesini oluştur
            rota = self.ent_rota.get()
            gun = int(self.ent_gun.get())
            otel = float(self.ent_otel.get())
            arac = float(self.ent_arac.get())

            plan_nesnesi = SeyahatPlan(rota, gun, otel, arac)
            
            # Hesaplamayı yap
            gece, otel_toplam, ulasim_toplam, genel_toplam = plan_nesnesi.butce_hesapla()
            
            # --- SONUÇ PENCERESİ ---
            result_win = tk.Toplevel(self.root)
            result_win.title("Seyahat Analiz Raporu")
            result_win.geometry("380x450")
            result_win.configure(bg="white")

            tk.Label(result_win, text="📊 TAHMİNİ BÜTÇE ANALİZİ", font=("Arial", 14, "bold"), 
                     bg="white", pady=20, fg="#1a5f7a").pack()
            
            detay_metni = (
                f"📍 Rota: {rota}\n\n"
                f"📅 Süre: {gun} Gün / {gece} Gece\n"
                f"───────────────────────────\n"
                f"🏨 Otel Masrafı ({gece} Gece): {otel_toplam:,.2f} ₺\n"
                f"🚗 Araç Masrafı ({gun} Gün): {ulasim_toplam:,.2f} ₺\n"
                f"───────────────────────────\n"
            )
            
            tk.Label(result_win, text=detay_metni, justify="left", bg="white", 
                     font=("Courier New", 10), padx=20).pack()
            
            tk.Label(result_win, text=f"TOPLAM BÜTÇE: {genel_toplam:,.2f} ₺", 
                     font=("Arial", 14, "bold"), fg="#e67e22", bg="white").pack(pady=20)
            
            tk.Button(result_win, text="ANLADIM", command=result_win.destroy, 
                      bg="#34495e", fg="white", width=15).pack(pady=10)

        except ValueError:
            messagebox.showerror("Hata", "Lütfen kutucuklara sadece rakam girin!")

# Programı Çalıştır
if __name__ == "__main__":
    root = tk.Tk()
    app = SeyahatApp(root)
    root.mainloop()