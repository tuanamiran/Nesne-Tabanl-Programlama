class Seyahat:
    def __init__(self, seyahat_id, gidis_yeri, tarih, gun_sayisi):
        self.seyahat_id = seyahat_id
        self.gidis_yeri = gidis_yeri
        self.tarih = tarih
        self.gun_sayisi = gun_sayisi

    def __str__(self):
        return f"{self.gidis_yeri} ({self.tarih})"


class Konaklama:
    def __init__(self, otel_adi, gecelik_fiyat):
        self.otel_adi = otel_adi
        self.gecelik_fiyat = gecelik_fiyat

    def __str__(self):
        return f"{self.otel_adi} - Gecelik: {self.gecelik_fiyat} ₺"


class Ulasim:
    def __init__(self, ulasim_turu, firma, gunluk_fiyat):
        self.ulasim_turu = ulasim_turu
        self.firma = firma
        self.gunluk_fiyat = gunluk_fiyat


class Plan:
    def __init__(self, rota, seyahat, konaklama, ulasim):
        self.rota = rota
        self.seyahat = seyahat
        self.konaklama = konaklama
        self.ulasim = ulasim
        self.aktiviteler = []

    def aktivite_ekle(self, aktivite):
        self.aktiviteler.append(aktivite)
        print(f"✅ Başarılı: '{aktivite}' plana eklendi.")

    def plan_ozeti(self):
        # Maliyet Hesaplamaları
        gece_sayisi = self.seyahat.gun_sayisi - 1
        konaklama_maliyeti = self.konaklama.gecelik_fiyat * gece_sayisi
        ulasim_maliyeti = self.ulasim.gunluk_fiyat * self.seyahat.gun_sayisi
        toplam_butce = konaklama_maliyeti + ulasim_maliyeti

        # Çıktı Ekranı
        print(f"\n--- ✈️ {self.seyahat.gidis_yeri.upper()} SEYAHAT PLANI ÖZETİ ---")
        print(f"Rota: {self.rota}")
        print(f"Tarih: {self.seyahat.tarih} ({self.seyahat.gun_sayisi} Gün / {gece_sayisi} Gece)")
        print(f"Otel: {self.konaklama.otel_adi}")
        print(f"Ulaşım: {self.ulasim.firma} ({self.ulasim.ulasim_turu})")
        print("--------------------------------")
        
        # Aktivite Kontrolü
        if len(self.aktiviteler) == 0:
            print("Aktiviteler: Şu anda Yok")
        else:
            print("Aktiviteler:")
            for i, aktivite in enumerate(self.aktiviteler, 1):
                print(f"  {i}. {aktivite}")
        
        print("--------------------------------")
        # Bütçe Ekranı
        print("💰 TAHMİNİ BÜTÇE HESAPLAMASI:")
        print(f" - Konaklama ({gece_sayisi} Gece): {konaklama_maliyeti} ₺")
        print(f" - Ulaşım ({self.seyahat.gun_sayisi} Gün): {ulasim_maliyeti} ₺")
        print(f" 👉 TOPLAM MALİYET: {toplam_butce} ₺")
        print("========================================\n")


# ==========================================
# 1. BÖLÜM: TRABZON PLANI (DOLU PLAN)
# ==========================================
print(">>> BÖLÜM 1: TRABZON SEYAHATİ HAZIRLANIYOR...")
seyahat1 = Seyahat(seyahat_id="T-101", gidis_yeri="Trabzon", tarih="15-18 Ağustos 2026", gun_sayisi=4)
otel1 = Konaklama(otel_adi="Radisson Blu Hotel, Trabzon(Boztepe)", gecelik_fiyat=6600)
araba_kiralama = Ulasim(ulasim_turu="SUV Araç Kiralama", firma="Avis", gunluk_fiyat=1500)

plan1 = Plan(rota="İstanbul -> Trabzon", seyahat=seyahat1, konaklama=otel1, ulasim=araba_kiralama)

plan1.aktivite_ekle("Sabah Kahvaltı için Çıtır Hamurlu Trabzon Pidesi")
plan1.aktivite_ekle("Sümela Manastırı ve Uzungöl ziyareti")
plan1.aktivite_ekle("Ayasofya Müzesi, Trabzon Botanik Bahçesi, Atatürk köşkü ve Boztepe Seyir Terası")

plan1.plan_ozeti()


# ==========================================
# 2. BÖLÜM: RİZE PLANI (BOŞ PLAN TESTİ)
# ==========================================
print(">>> BÖLÜM 2: RİZE SEYAHATİ HAZIRLANIYOR...")
# Trabzon'dan Rize'ye geçiş (2 Gün)
seyahat2 = Seyahat(seyahat_id="R-102", gidis_yeri="Rize", tarih="19-20 Ağustos 2026", gun_sayisi=2)
otel2 = Konaklama(otel_adi="Ayder Doğa Resort", gecelik_fiyat=4500)
# Aynı aracı kullanmaya devam ediyoruz:
plan2 = Plan(rota="Trabzon -> Rize", seyahat=seyahat2, konaklama=otel2, ulasim=araba_kiralama)

#plan2.aktivite_ekle("Ayder yaylasına çıkmak")  # Aktivite eklemiyoruz, direkt rapor alıyoruz.

plan2.plan_ozeti()
class Seyahat:
    def __init__(self, seyahat_id, gidis_yeri, tarih, gun_sayisi):
        self.seyahat_id = seyahat_id
        self.gidis_yeri = gidis_yeri
        self.tarih = tarih
        self.gun_sayisi = gun_sayisi

class Konaklama:
    def __init__(self, otel_adi, gecelik_fiyat):
        self.otel_adi = otel_adi
        self.gecelik_fiyat = gecelik_fiyat

class Ulasim:
    def __init__(self, ulasim_turu, firma, gunluk_fiyat):
        self.ulasim_turu = ulasim_turu
        self.firma = firma
        self.gunluk_fiyat = gunluk_fiyat

class Plan:
    def __init__(self, rota, seyahat, konaklama, ulasim):
        self.rota = rota
        self.seyahat = seyahat
        self.konaklama = konaklama
        self.ulasim = ulasim
        self.aktiviteler = []

    def aktivite_ekle(self, aktivite):
        self.aktiviteler.append(aktivite)
        print(f"✅ '{aktivite}' plana eklendi.")

    def plan_ozeti(self):
        gece_sayisi = self.seyahat.gun_sayisi - 1
        konaklama_maliyeti = self.konaklama.gecelik_fiyat * gece_sayisi
        ulasim_maliyeti = self.ulasim.gunluk_fiyat * self.seyahat.gun_sayisi
        toplam_butce = konaklama_maliyeti + ulasim_maliyeti

        print(f"\n========================================")
        print(f"✈️ {self.seyahat.gidis_yeri.upper()} SEYAHAT PLANI ÖZETİ")
        print(f"========================================")
        print(f"Rota: {self.rota}")
        print(f"Tarih: {self.seyahat.tarih} ({self.seyahat.gun_sayisi} Gün / {gece_sayisi} Gece)")
        print(f"Otel: {self.konaklama.otel_adi}")
        print(f"Ulaşım: {self.ulasim.firma} ({self.ulasim.ulasim_turu})")
        print("----------------------------------------")
        
        if len(self.aktiviteler) == 0:
            print("Aktiviteler: Yok")
        else:
            print("Aktiviteler:")
            for i, aktivite in enumerate(self.aktiviteler, 1):
                print(f"  {i}. {aktivite}")
        
        print("----------------------------------------")
        print("💰 TAHMİNİ BÜTÇE HESAPLAMASI:")
        print(f" - Konaklama ({gece_sayisi} Gece): {konaklama_maliyeti} ₺")
        print(f" - Ulaşım/Araç Kiralama ({self.seyahat.gun_sayisi} Gün): {ulasim_maliyeti} ₺")
        print(f" 👉 TOPLAM MALİYET: {toplam_butce} ₺")
        print("========================================\n")


# ==========================================
# İNTERAKTİF KULLANICI ARAYÜZÜ
# ==========================================

print("\n🌍 SEYAHAT PLANLAMA ASİSTANINA HOŞ GELDİNİZ 🌍")
print("Lütfen seyahat detaylarınızı adım adım girin.\n")

# 1. Temel Seyahat Bilgileri
nereden = input("1. Nereden yola çıkacaksınız? (Örn: İstanbul): ")
nereye = input("2. Nereye gidiyorsunuz? (Örn: Trabzon): ")
tarih = input("3. Hangi tarihlerde? (Örn: 15-18 Ağustos): ")
gun = int(input("4. Toplam kaç gün sürecek? (Örn: 4): "))

rota_bilgisi = f"{nereden} -> {nereye}"
yeni_seyahat = Seyahat(seyahat_id="S-001", gidis_yeri=nereye, tarih=tarih, gun_sayisi=gun)

print("\n--- Konaklama Bilgileri ---")
otel = input("5. Kalacağınız otelin adı nedir?: ")
otel_fiyat = float(input("6. Otelin gecelik fiyatı ne kadar? (₺): "))
yeni_konaklama = Konaklama(otel_adi=otel, gecelik_fiyat=otel_fiyat)

print("\n--- Ulaşım Bilgileri ---")
ulasim_tur = input("7. Ulaşım türü nedir? (Örn: Araç Kiralama): ")
firma_adi = input("8. Hangi firma ile çalışacaksınız?: ")
ulasim_fiyat = float(input("9. Ulaşımın günlük maliyeti nedir? (₺): "))
yeni_ulasim = Ulasim(ulasim_turu=ulasim_tur, firma=firma_adi, gunluk_fiyat=ulasim_fiyat)

# 2. Plan Nesnesini Oluşturma
aktif_plan = Plan(rota=rota_bilgisi, seyahat=yeni_seyahat, konaklama=yeni_konaklama, ulasim=yeni_ulasim)

# 3. Aktiviteleri Ekleme (Döngü ile)
print("\n--- Aktiviteler ---")
print("Yapmak istediğiniz aktiviteleri sırayla girin.")
print("(Bitirmek ve raporu görmek için 'q' veya 'bitti' yazıp Enter'a basın)")

while True:
    girilen_aktivite = input("Aktivite Ekle: ")
    
    # Kullanıcı çıkmak isterse döngüyü kır
    if girilen_aktivite.lower() in ['q', 'bitti', 'bitir', 'tamam']:
        break
    
    # Boş bir şey girilmediyse plana ekle
    if girilen_aktivite.strip() != "":
        aktif_plan.aktivite_ekle(girilen_aktivite)

# 4. Final Raporunu Gösterme
print("\nHarika! Seyahat planınız hazırlandı. İşte özetiniz:")
aktif_plan.plan_ozeti()