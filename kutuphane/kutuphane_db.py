import sqlite3


DB_NAME = "kutuphane_sistemi.db"


def baglanti_olustur():
    return sqlite3.connect(DB_NAME)


def tablo_olustur():
    with baglanti_olustur() as baglanti:
        imlec = baglanti.cursor()

        imlec.execute(
            """
            create table if not exists kitap (
                kitap_id integer primary key autoincrement,
                ad text not null,
                yazar text not null,
                kategori text not null,
                durum text not null default 'musait'
            )
            """
        )

        imlec.execute(
            """
            create table if not exists uye (
                uye_id integer primary key autoincrement,
                ad text not null,
                email text not null unique
            )
            """
        )

        imlec.execute(
            """
            create table if not exists odunc (
                odunc_id integer primary key autoincrement,
                kitap_id integer not null,
                uye_id integer not null,
                odunc_tarihi text not null,
                iade_tarihi text,
                foreign key (kitap_id) references kitap (kitap_id),
                foreign key (uye_id) references uye (uye_id)
            )
            """
        )

        baglanti.commit()


def kitap_ekle(ad, yazar, kategori, durum="musait"):
    with baglanti_olustur() as baglanti:
        imlec = baglanti.cursor()
        imlec.execute(
            "insert into kitap (ad, yazar, kategori, durum) values (?, ?, ?, ?)",
            (ad, yazar, kategori, durum),
        )
        baglanti.commit()
        return imlec.lastrowid


def uye_ekle(ad, email):
    with baglanti_olustur() as baglanti:
        imlec = baglanti.cursor()
        imlec.execute(
            "insert into uye (ad, email) values (?, ?)",
            (ad, email),
        )
        baglanti.commit()
        return imlec.lastrowid


def varsayilan_verileri_ekle():
    with baglanti_olustur() as baglanti:
        imlec = baglanti.cursor()

        imlec.execute("select count(*) from kitap")
        kitap_sayisi = imlec.fetchone()[0]

        if kitap_sayisi == 0:
            kitaplar = [
                ("suc ve ceza", "fyodor dostoyevski", "roman", "musait"),
                ("ince memed", "yasar kemal", "roman", "musait"),
                ("sefiller", "victor hugo", "klasik", "musait"),
                ("simyaci", "paulo coelho", "kurgu", "musait"),
            ]
            imlec.executemany(
                "insert into kitap (ad, yazar, kategori, durum) values (?, ?, ?, ?)",
                kitaplar,
            )

        imlec.execute("select count(*) from uye")
        uye_sayisi = imlec.fetchone()[0]

        if uye_sayisi == 0:
            uyeler = [
                ("ali veli", "ali@example.com"),
                ("ayse demir", "ayse@example.com"),
            ]
            imlec.executemany(
                "insert into uye (ad, email) values (?, ?)",
                uyeler,
            )

        baglanti.commit()


if __name__ == "__main__":
    tablo_olustur()
    varsayilan_verileri_ekle()
