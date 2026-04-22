import sqlite3


database_adi = "randevu_sistemi.db"


def baglanti_olustur():
    return sqlite3.connect(database_adi)


def tablolari_olustur():
    connection = baglanti_olustur()
    cursor = connection.cursor()

    cursor.execute(
        """
        create table if not exists hasta (
            hasta_id integer primary key autoincrement,
            ad text not null,
            tc text not null unique,
            telefon text not null
        )
        """
    )

    cursor.execute(
        """
        create table if not exists doktor (
            doktor_id integer primary key autoincrement,
            ad text not null,
            uzmanlik text not null,
            uygun_saatler text not null
        )
        """
    )

    cursor.execute(
        """
        create table if not exists randevu (
            randevu_id integer primary key autoincrement,
            tarih text not null,
            saat text not null,
            doktor_id integer not null,
            hasta_id integer not null,
            foreign key (doktor_id) references doktor (doktor_id),
            foreign key (hasta_id) references hasta (hasta_id)
        )
        """
    )

    connection.commit()
    connection.close()


def kayit_ekle(sorgu, parametreler=()):
    connection = baglanti_olustur()
    cursor = connection.cursor()
    cursor.execute(sorgu, parametreler)
    connection.commit()
    son_id = cursor.lastrowid
    connection.close()
    return son_id


def tek_kayit_getir(sorgu, parametreler=()):
    connection = baglanti_olustur()
    cursor = connection.cursor()
    cursor.execute(sorgu, parametreler)
    sonuc = cursor.fetchone()
    connection.close()
    return sonuc


def coklu_kayit_getir(sorgu, parametreler=()):
    connection = baglanti_olustur()
    cursor = connection.cursor()
    cursor.execute(sorgu, parametreler)
    sonuclar = cursor.fetchall()
    connection.close()
    return sonuclar


def kayit_guncelle_veya_sil(sorgu, parametreler=()):
    connection = baglanti_olustur()
    cursor = connection.cursor()
    cursor.execute(sorgu, parametreler)
    connection.commit()
    etkilenen_satir = cursor.rowcount
    connection.close()
    return etkilenen_satir


def varsayilan_doktorlari_ekle():
    doktor_sayisi = tek_kayit_getir("select count(*) from doktor")
    if doktor_sayisi and doktor_sayisi[0] > 0:
        return

    doktorlar = [
        ("dr. ayse demir", "kardiyoloji", "09:00,10:00,11:00,14:00"),
        ("dr. mehmet kaya", "dahiliye", "10:00,11:00,13:00,15:00"),
        ("dr. selin aksoy", "cildiye", "09:30,10:30,14:30,16:00"),
    ]

    for doktor in doktorlar:
        kayit_ekle(
            "insert into doktor (ad, uzmanlik, uygun_saatler) values (?, ?, ?)",
            doktor,
        )
