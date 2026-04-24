# --- İstenen Sınıflar ---
class Musteri:
    def __init__(self, musteri_id, ad, telefon):
        self.musteri_id = musteri_id
        self.ad = ad
        self.telefon = telefon

    # İstenen METOT
    def musteri_ekle(self, musteri_sozlugu):
        musteri_sozlugu[self.musteri_id] = self
        return True, f"Müşteri '{self.ad}' sisteme eklendi."

class Satis:
    def __init__(self, satis_id, urun, fiyat, musteri):
        self.satis_id = satis_id
        self.urun = urun
        self.fiyat = fiyat
        self.musteri = musteri # Hangi müşteriye satıldığını bilmek için ekledik

class DestekTalebi:
    def __init__(self, talep_id, aciklama, musteri):
        self.talep_id = talep_id
        self.aciklama = aciklama
        self.musteri = musteri # Hangi müşterinin talebi olduğunu bilmek için ekledik
        self.durum = "Açık"

# --- Sistemi Yönetecek Ana Sınıf ---
class CRMYoneticisi:
    def __init__(self):
        self.musteriler = {}
        self.satislar = []
        self.destek_talepleri = []

    def yeni_musteri_kaydi(self, m_id, ad, telefon):
        if m_id in self.musteriler:
            return False, "Bu ID'ye sahip bir müşteri zaten var!"
        
        yeni_musteri = Musteri(m_id, ad, telefon)
        # Sınıf içindeki metodu çağırarak listeye ekliyoruz
        return yeni_musteri.musteri_ekle(self.musteriler)

    def yeni_satis_yap(self, satis_id, m_id, urun, fiyat):
        if m_id not in self.musteriler:
            return False, "Hata: Müşteri bulunamadı!"
        
        # Satış ID kontrolü (Aynı ID'den iki satış olmasın)
        for s in self.satislar:
            if s.satis_id == satis_id:
                return False, "Hata: Bu Satış ID zaten kullanılmış!"

        musteri = self.musteriler[m_id]
        yeni_satis = Satis(satis_id, urun, fiyat, musteri)
        self.satislar.append(yeni_satis)
        return True, f"Başarılı: '{urun}' satışı kaydedildi."

    def destek_talebi_olustur(self, talep_id, m_id, aciklama):
        if m_id not in self.musteriler:
            return False, "Hata: Müşteri bulunamadı!"
            
        for t in self.destek_talepleri:
            if t.talep_id == talep_id:
                return False, "Hata: Bu Talep ID zaten kullanılmış!"

        musteri = self.musteriler[m_id]
        yeni_talep = DestekTalebi(talep_id, aciklama, musteri)
        self.destek_talepleri.append(yeni_talep)
        return True, "Başarılı: Destek talebi oluşturuldu."