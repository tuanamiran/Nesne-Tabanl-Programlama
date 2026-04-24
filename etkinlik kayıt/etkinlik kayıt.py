# ==========================================
# SINIF TANIMLAMALARI (Tüm Özellikler Dahil)
# ==========================================

class Katilimci:
    def __init__(self, katilimci_id, ad, email, yas):
        self.katilimci_id = katilimci_id
        self.ad = ad
        self.email = email
        self.yas = yas

    def __str__(self):
        return f"{self.ad} ({self.yas} yaşında)"


class Etkinlik:
    def __init__(self, etkinlik_id, ad, tarih, kapasite, yas_siniri, standart_fiyat, vip_fiyat, minimum_katilimci):
        self.etkinlik_id = etkinlik_id
        self.ad = ad
        self.tarih = tarih
        self.kapasite = kapasite
        self.yas_siniri = yas_siniri
        self.standart_fiyat = standart_fiyat
        self.vip_fiyat = vip_fiyat
        self.minimum_katilimci = minimum_katilimci
        self.katilimcilar = []
        self.toplam_gelir = 0 

    def katilimci_ekle(self, katilimci, bilet_turu):
        # Güvenlik Kontrolü (Yaş Sınırı)
        if katilimci.yas < self.yas_siniri:
            print(f"🚫 Reddedildi: {katilimci.ad} ({katilimci.yas} yaş), bu etkinlik için çok genç! (Kural: +{self.yas_siniri})")
            return False

        # Kapasite Kontrolü
        if len(self.katilimcilar) < self.kapasite:
            self.katilimcilar.append(katilimci)
            
            # Finans Kontrolü (Kasaya para ekleme)
            if bilet_turu == "VIP":
                self.toplam_gelir += self.vip_fiyat
            else:
                self.toplam_gelir += self.standart_fiyat
                
            print(f"✅ Başarılı: {katilimci.ad}, etkinliğe kaydedildi. (+{bilet_turu} Bilet Ücreti Kasaya Eklendi)")
            return True
        else:
            print(f"❌ Hata: '{self.ad}' kapasitesi dolu! {katilimci.ad} eklenemedi.")
            return False

    def katilim_raporu(self):
        print(f"\n===============================================")
        print(f"📊 '{self.ad.upper()}' FİNANS VE KATILIM RAPORU")
        print(f"===============================================")
        
        # İPTAL VE İADE KONTROLÜ
        if len(self.katilimcilar) < self.minimum_katilimci:
            print("🚨 DİKKAT: ETKİNLİK İPTAL EDİLDİ!")
            print(f"Sebep: Minimum {self.minimum_katilimci} katılımcı şartı sağlanamadı (Sadece {len(self.katilimcilar)} kişi kayıt oldu).")
            print(f"💸 İade İşlemi Başlatıldı: Kasadaki {self.toplam_gelir} ₺ tüm müşterilere iade ediliyor...")
            self.toplam_gelir = 0  # İade yapıldığı için kasa sıfırlandı
            print("===============================================\n")
            return  

        # Etkinlik iptal olmadıysa normal raporu yazdırmaya devam et:
        print(f"Tarih: {self.tarih}")
        print(f"Kapasite: {self.kapasite} kişi | Yaş Sınırı: +{self.yas_siniri} | Baraj: {self.minimum_katilimci} kişi")
        print(f"Kayıtlı: {len(self.katilimcilar)} kişi | Boş Yer: {self.kapasite - len(self.katilimcilar)}")
        print(f"💰 Toplam Hasılat (Kasa): {self.toplam_gelir} ₺")
        print("-----------------------------------------------")
        
        if len(self.katilimcilar) == 0:
            print("Katılımcılar: Yok")
        else:
            print("Katılımcılar Listesi:")
            for i, k in enumerate(self.katilimcilar, 1):
                print(f"  {i}. {k.ad} - Yaş: {k.yas} ({k.email})")
        print("===============================================\n")


class Bilet:
    def __init__(self, bilet_id, etkinlik, katilimci):
        self.bilet_id = bilet_id
        self.etkinlik = etkinlik
        self.katilimci = katilimci

    @staticmethod
    def bilet_olustur(bilet_id, etkinlik, katilimci):
        eklendi_mi = etkinlik.katilimci_ekle(katilimci, bilet_turu="Standart")
        if eklendi_mi:
            yeni_bilet = Bilet(bilet_id, etkinlik, katilimci)
            print(f"🎫 Standart Bilet kesildi -> Bilet ID: {bilet_id}")
            return yeni_bilet
        return None


class VipBilet(Bilet):
    def __init__(self, bilet_id, etkinlik, katilimci, vip_ayricalik):
        super().__init__(bilet_id, etkinlik, katilimci)
        self.vip_ayricalik = vip_ayricalik

    @staticmethod
    def vip_bilet_olustur(bilet_id, etkinlik, katilimci, vip_ayricalik):
        eklendi_mi = etkinlik.katilimci_ekle(katilimci, bilet_turu="VIP")
        if eklendi_mi:
            yeni_bilet = VipBilet(bilet_id, etkinlik, katilimci, vip_ayricalik)
            print(f"🌟 VIP Bilet kesildi -> Bilet ID: {bilet_id} | Ayrıcalık: {vip_ayricalik}")
            return yeni_bilet
        return None


# ==========================================
# BÖLÜM 1: STATİK TEST (KOD İÇİNDEN)
# ==========================================
print("\n>>> BÖLÜM 1: OTOMATİK (STATİK) SİSTEM TESTİ BAŞLIYOR <<<")

# Otomatik test için barajı 2 kişi yaptık ki iptal olmasın, başarıyla raporu görelim.
etkinlik_statik = Etkinlik("E-001", "Gece Yarısı Konseri", "20 Kasım", kapasite=5, yas_siniri=18, standart_fiyat=500, vip_fiyat=1500, minimum_katilimci=2)

kisi1 = Katilimci(101, "Ali Yılmaz", "ali@gmail.com", yas=16) 
kisi2 = Katilimci(102, "Zeynep Demir", "zeynep@gmail.com", yas=25)
kisi3 = Katilimci(103, "Can Kaya", "can@gmail.com", yas=30)

print("\n--- BİLET SATIŞLARI ---")
bilet1 = Bilet.bilet_olustur("B-1001", etkinlik_statik, kisi1) # Ali 16 yaşında, reddedilecek
bilet2 = VipBilet.vip_bilet_olustur("VIP-1002", etkinlik_statik, kisi2, vip_ayricalik="Kulis Erişimi")
bilet3 = Bilet.bilet_olustur("B-1003", etkinlik_statik, kisi3) 

etkinlik_statik.katilim_raporu()

input(">>> Bölüm 2 (İnteraktif Sistem)'ye geçmek için ENTER tuşuna basın...\n")


# ==========================================
# BÖLÜM 2: İNTERAKTİF VE ÇÖKMEYE KARŞI KORUMALI GİŞE
# ==========================================
print(">>> BÖLÜM 2: İNTERAKTİF GİŞE SİSTEMİ BAŞLIYOR <<<")
print("Önce etkinliğinizin kurallarını belirleyelim.\n")

# --- KURULUMDA BOŞ GEÇİLMESİNİ ENGELLEME ---
while True:
    etkinlik_adi = input("1. Etkinliğin Adı Nedir?: ").strip()
    if etkinlik_adi != "":
        break
    print("⚠️ Hata: Etkinlik adı boş bırakılamaz!")

etkinlik_tarihi = input("2. Etkinlik Tarihi (Örn: 20 Kasım): ").strip()

# --- SAYI GİRİLMESİ GEREKEN YERLERDE ÇÖKME KORUMASI ---
while True:
    try:
        kapasite_siniri = int(input("3. Maksimum Kapasite Kaç Kişi Olacak?: "))
        yas_kurali = int(input("4. Yaş Sınırı Kaç Olmalı? (Sınır yoksa 0 yazın): "))
        fiyat_standart = float(input("5. Standart Bilet Fiyatı (₺): "))
        fiyat_vip = float(input("6. VIP Bilet Fiyatı (₺): "))
        baraj_kisi = int(input("7. Minimum Katılımcı Barajı Kaç Olsun?: "))
        break # Doğru girildiyse döngüden çık
    except ValueError:
        print("⛔ HATA: Lütfen bu alanları boş bırakmayın ve sadece RAKAM girin!\n")


aktif_etkinlik = Etkinlik(
    etkinlik_id="E-100", 
    ad=etkinlik_adi, 
    tarih=etkinlik_tarihi, 
    kapasite=kapasite_siniri, 
    yas_siniri=yas_kurali, 
    standart_fiyat=fiyat_standart, 
    vip_fiyat=fiyat_vip,
    minimum_katilimci=baraj_kisi
)

print(f"\n✅ Harika! '{etkinlik_adi}' oluşturuldu. Unutmayın, en az {baraj_kisi} bilet satılmazsa etkinlik iptal olacaktır!")
print("-" * 50)

sayac = 1000 

while True:
    print(f"\n--- YENİ MÜŞTERİ (Mevcut Kayıt: {len(aktif_etkinlik.katilimcilar)} / {aktif_etkinlik.kapasite}) ---")
    
    # İSİM KONTROLÜ
    isim = input("Katılımcı Adı Soyadı (Gişeyi kapatmak için 'q' yazın): ").strip()
    
    if isim == "":
        print("⚠️ Hata: İsim alanı boş geçilemez!")
        continue
        
    if isim.lower() in ['q', 'bitti', 'bitir']:
        break
        
    if len(aktif_etkinlik.katilimcilar) >= aktif_etkinlik.kapasite:
        print("⚠️ DİKKAT: Etkinlik kapasitesi tamamen doldu! Daha fazla bilet kesemezsiniz.")
        devam = input("Yine de başka işlem denemek istiyor musunuz? (e/h): ").strip()
        if devam.lower() != 'e':
            break

    email = input("E-posta Adresi (İsteğe bağlı): ").strip()
    if email == "":
        email = "Belirtilmedi"

    # YAŞ KONTROLÜ
    while True:
        try:
            yas = int(input("Yaşı: "))
            break
        except ValueError:
            print("⚠️ Hata: Lütfen geçerli bir yaş rakamı girin (Boş bırakılamaz)!")
    
    musteri = Katilimci(katilimci_id=sayac, ad=isim, email=email, yas=yas)
    
    bilet_secimi = input("Bilet Türü Seçin [1: Standart, 2: VIP]: ").strip()
    
    bilet_kodu = f"B-{sayac}"
    
    if bilet_secimi == "2":
        VipBilet.vip_bilet_olustur(bilet_kodu, aktif_etkinlik, musteri, vip_ayricalik="Kulis Erişimi ve Ön Sıra")
    else:
        Bilet.bilet_olustur(bilet_kodu, aktif_etkinlik, musteri)
        
    sayac += 1 

print("\n🎟️ GİŞELER KAPANDI. SONUÇLAR HESAPLANIYOR...")
aktif_etkinlik.katilim_raporu()