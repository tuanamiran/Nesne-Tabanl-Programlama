from randevu_db import (
    coklu_kayit_getir,
    kayit_ekle,
    kayit_guncelle_veya_sil,
    tek_kayit_getir,
)


class Hasta:
    def __init__(self, ad, tc, telefon):
        self.ad = ad
        self.tc = tc
        self.telefon = telefon

    def kaydet(self):
        mevcut_hasta = tek_kayit_getir(
            "select hasta_id from hasta where tc = ?",
            (self.tc,),
        )
        if mevcut_hasta:
            return mevcut_hasta[0]

        return kayit_ekle(
            "insert into hasta (ad, tc, telefon) values (?, ?, ?)",
            (self.ad, self.tc, self.telefon),
        )

    def randevu_al(self, doktor_id, tarih, saat):
        hasta_id = self.kaydet()
        return Randevu.randevu_olustur(tarih, saat, doktor_id, hasta_id)


class Doktor:
    @staticmethod
    def tum_doktorlari_getir():
        return coklu_kayit_getir(
            "select doktor_id, ad, uzmanlik, uygun_saatler from doktor order by ad"
        )

    @staticmethod
    def uygunluk_kontrol(doktor_id, tarih, saat):
        doktor = tek_kayit_getir(
            "select uygun_saatler from doktor where doktor_id = ?",
            (doktor_id,),
        )
        if not doktor:
            return False, "doktor bulunamadi"

        uygun_saatler = [deger.strip() for deger in doktor[0].split(",") if deger.strip()]
        if saat not in uygun_saatler:
            return False, "secilen saat doktorun uygun saatleri arasinda degil"

        mevcut_randevu = tek_kayit_getir(
            "select randevu_id from randevu where doktor_id = ? and tarih = ? and saat = ?",
            (doktor_id, tarih, saat),
        )
        if mevcut_randevu:
            return False, "bu saat icin zaten randevu alinmis"

        return True, "doktor uygun"


class Randevu:
    @staticmethod
    def randevu_olustur(tarih, saat, doktor_id, hasta_id):
        uygun_mu, mesaj = Doktor.uygunluk_kontrol(doktor_id, tarih, saat)
        if not uygun_mu:
            return False, mesaj

        kayit_ekle(
            "insert into randevu (tarih, saat, doktor_id, hasta_id) values (?, ?, ?, ?)",
            (tarih, saat, doktor_id, hasta_id),
        )
        return True, "randevu basariyla olusturuldu"

    @staticmethod
    def randevu_iptal(randevu_id):
        etkilenen_satir = kayit_guncelle_veya_sil(
            "delete from randevu where randevu_id = ?",
            (randevu_id,),
        )
        if etkilenen_satir == 0:
            return False, "iptal edilecek randevu bulunamadi"
        return True, "randevu iptal edildi"

    @staticmethod
    def hastanin_randevularini_getir(tc):
        return coklu_kayit_getir(
            """
            select r.randevu_id, d.ad, d.uzmanlik, r.tarih, r.saat
            from randevu r
            join hasta h on h.hasta_id = r.hasta_id
            join doktor d on d.doktor_id = r.doktor_id
            where h.tc = ?
            order by r.tarih, r.saat
            """,
            (tc,),
        )
