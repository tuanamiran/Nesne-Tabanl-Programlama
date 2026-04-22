from datetime import datetime

import kutuphane_db


class Kitap:
    def __init__(self, kitap_id, ad=None, yazar=None, kategori=None, durum=None):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.kategori = kategori
        self.durum = durum

    def kitap_durumu_degistir(self, yeni_durum):
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                "update kitap set durum = ? where kitap_id = ?",
                (yeni_durum, self.kitap_id),
            )
            baglanti.commit()
        self.durum = yeni_durum

    @staticmethod
    def tum_kitaplari_getir():
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                "select kitap_id, ad, yazar, kategori, durum from kitap order by kitap_id"
            )
            return imlec.fetchall()

    @staticmethod
    def kitap_getir(kitap_id):
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                "select kitap_id, ad, yazar, kategori, durum from kitap where kitap_id = ?",
                (kitap_id,),
            )
            kayit = imlec.fetchone()

        if kayit is None:
            return None

        return Kitap(*kayit)

    @staticmethod
    def kitap_ara(sorgu):
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            aranan = f"%{sorgu}%"
            imlec.execute(
                "select kitap_id, ad, yazar, kategori, durum from kitap where ad like ? or yazar like ? order by ad",
                (aranan, aranan),
            )
            return imlec.fetchall()

    @staticmethod
    def kitapligimi_getir():
        # Şimdilik kullanıcı girişi sistemi olmadığı için durum='oduncte' olan tüm kitapları listeliyoruz.
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                "select kitap_id, ad, yazar, kategori, durum from kitap where durum = 'oduncte' order by ad"
            )
            return imlec.fetchall()

    @staticmethod
    def gecmisi_getir():
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                """
                select distinct k.kitap_id, k.ad, k.yazar, k.kategori, k.durum
                from kitap k
                join odunc o on k.kitap_id = o.kitap_id
                where o.iade_tarihi is not null
                order by k.ad
                """
            )
            return imlec.fetchall()

class Odunc:
    def __init__(self, kitap_id, uye_id):
        self.kitap_id = kitap_id
        self.uye_id = uye_id

    def odunc_ver(self):
        odunc_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                """
                insert into odunc (kitap_id, uye_id, odunc_tarihi, iade_tarihi)
                values (?, ?, ?, null)
                """,
                (self.kitap_id, self.uye_id, odunc_tarihi),
            )
            baglanti.commit()
            return imlec.lastrowid

    @staticmethod
    def aktif_odunc_getir(kitap_id):
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                """
                select odunc_id, kitap_id, uye_id, odunc_tarihi, iade_tarihi
                from odunc
                where kitap_id = ? and iade_tarihi is null
                order by odunc_id desc
                limit 1
                """,
                (kitap_id,),
            )
            return imlec.fetchone()

    @staticmethod
    def iade_al(kitap_id):
        iade_tarihi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                """
                update odunc
                set iade_tarihi = ?
                where odunc_id = (
                    select odunc_id
                    from odunc
                    where kitap_id = ? and iade_tarihi is null
                    order by odunc_id desc
                    limit 1
                )
                """,
                (iade_tarihi, kitap_id),
            )
            baglanti.commit()
            return imlec.rowcount


class Uye:
    def __init__(self, uye_id, ad=None, email=None):
        self.uye_id = uye_id
        self.ad = ad
        self.email = email

    def kitap_odunc_al(self, kitap_id):
        kitap = Kitap.kitap_getir(kitap_id)

        if kitap is None:
            raise ValueError("kitap bulunamadi")

        if kitap.durum != "musait":
            raise ValueError("kitap su anda musait degil")

        odunc = Odunc(kitap_id, self.uye_id)
        odunc_id = odunc.odunc_ver()
        kitap.kitap_durumu_degistir("oduncte")
        return odunc_id

    def kitap_iade_et(self, kitap_id):
        kitap = Kitap.kitap_getir(kitap_id)

        if kitap is None:
            raise ValueError("kitap bulunamadi")

        aktif_odunc = Odunc.aktif_odunc_getir(kitap_id)
        if aktif_odunc is None:
            raise ValueError("iade edilecek aktif odunc kaydi yok")

        if aktif_odunc[2] != self.uye_id:
            raise ValueError("bu kitap farkli bir uye tarafindan odunc alinmis")

        guncellenen_satir = Odunc.iade_al(kitap_id)
        if guncellenen_satir == 0:
            raise ValueError("iade islemi tamamlanamadi")

        kitap.kitap_durumu_degistir("musait")

    @staticmethod
    def tum_uyeleri_getir():
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute("select uye_id, ad, email from uye order by uye_id")
            return imlec.fetchall()

    @staticmethod
    def uye_getir(uye_id):
        with kutuphane_db.baglanti_olustur() as baglanti:
            imlec = baglanti.cursor()
            imlec.execute(
                "select uye_id, ad, email from uye where uye_id = ?",
                (uye_id,),
            )
            kayit = imlec.fetchone()

        if kayit is None:
            return None

        return Uye(*kayit)


def sistemi_hazirla():
    kutuphane_db.tablo_olustur()
    kutuphane_db.varsayilan_verileri_ekle()
