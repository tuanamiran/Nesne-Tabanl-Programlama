import datetime

# --- İstenen Sınıflar ---
class Arac:
    def __init__(self, arac_id, marka, model, kilometre):
        self.arac_id = arac_id
        self.marka = marka
        self.model = model
        self.kilometre = kilometre
        self.musait_mi = True

    def arac_durumu_guncelle(self, durum):
        self.musait_mi = durum

    def kilometre_guncelle(self, yeni_km):
        if yeni_km > self.kilometre:
            self.kilometre = yeni_km

class Kullanici:
    def __init__(self, kullanici_id, ad, ehliyet_no):
        self.kullanici_id = kullanici_id
        self.ad = ad
        self.ehliyet_no = ehliyet_no
        self.gecmis = []

    def kiralama_gecmisi(self):
        if not self.gecmis:
            return "Geçmiş kiralama bulunmuyor."
        return "\n".join([k.kiralama_bilgisi() for k in self.gecmis])

class Kiralama:
    def __init__(self, kiralama_id, arac, kullanici):
        self.kiralama_id = kiralama_id
        self.arac = arac
        self.kullanici = kullanici
        self.baslangic_saati = None  # İstenen özellik
        self.bitis_saati = None      # İstenen özellik

    def kiralama_baslat(self):
        self.arac.arac_durumu_guncelle(False)
        self.baslangic_saati = datetime.datetime.now() # O anki saati alır

    def kiralama_bitir(self, guncel_km):
        self.arac.arac_durumu_guncelle(True)
        self.arac.kilometre_guncelle(guncel_km)
        self.bitis_saati = datetime.datetime.now() # İade anındaki saati alır
        self.kullanici.gecmis.append(self)

    def kiralama_bilgisi(self):
        bas = self.baslangic_saati.strftime("%d.%m.%Y %H:%M") if self.baslangic_saati else "-"
        bit = self.bitis_saati.strftime("%d.%m.%Y %H:%M") if self.bitis_saati else "Devam Ediyor"
        return f"ID: {self.kiralama_id} | Araç: {self.arac.marka} | Müşteri: {self.kullanici.ad} | Başlangıç: {bas} | Bitiş: {bit}"

# --- Sistem Yöneticisi ---
class SistemYoneticisi:
    def __init__(self):
        self.araclar = {
            1: Arac(1, "Peugeot", "308 1.6 BlueHDi", 120000)
        }
        self.kullanicilar = {
            101: Kullanici(101, "Ali Emre Ünal", "TR-EHL-1234")
        }
        self.kiralamalar = []
        self.kiralama_sayaci = 1000

    def yeni_arac_ekle(self, arac_id, marka, model, km):
        if arac_id in self.araclar:
            return False, "Bu ID'ye sahip bir araç zaten var!"
        self.araclar[arac_id] = Arac(arac_id, marka, model, km)
        return True, f"{marka} {model} Sisteme eklendi."

    def yeni_kullanici_ekle(self, k_id, ad, ehliyet_no):
        if k_id in self.kullanicilar:
            return False, "Bu ID'ye sahip bir müşteri zaten var!"
        self.kullanicilar[k_id] = Kullanici(k_id, ad, ehliyet_no)
        return True, f"Müşteri {ad} sisteme kaydedildi."

    def arac_cikisi_yap(self, a_id, k_id):
        if a_id in self.araclar and k_id in self.kullanicilar:
            arac = self.araclar[a_id]
            kul = self.kullanicilar[k_id]
            if arac.musait_mi:
                yeni = Kiralama(self.kiralama_sayaci, arac, kul)
                yeni.kiralama_baslat()
                self.kiralamalar.append(yeni)
                self.kiralama_sayaci += 1
                return True, f"Başarılı: {arac.marka} aracı {kul.ad} müşterisine verildi. Başlangıç saati işlendi."
            return False, "Hata: Araç şu anda başka müşteride."
        return False, "Hata: Geçersiz Araç veya Müşteri ID."

    def arac_donusu_al(self, kiralama_id, guncel_km):
        for k in self.kiralamalar:
            if k.kiralama_id == kiralama_id and k.bitis_saati is None:
                k.kiralama_bitir(guncel_km)
                return True, "Araç iade alındı. Bitiş saati ve yeni KM sisteme işlendi."
        return False, "Hata: Aktif kiralama bulunamadı."