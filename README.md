# Nesne-Tabanl-Programlama

# Kütüphane Yönetim Sistemi (Library Management System)
Bu proje, Nesne Tabanlı Programlama (OOP) prensipleri kullanılarak geliştirilmiş bir kütüphane yönetim uygulamasıdır. Proje kapsamında kitap ekleme, listeleme, silme ve kullanıcı yönetimi gibi temel işlevler gerçekleştirilmektedir.

🛠 Kullanılan Teknolojiler
Dil: Python

Arayüz: Flask / Django (HTML şablonlarından anlaşıldığı üzere)

Veritabanı: SQLite / MySQL (Hangisini kullandıysan ekle)

Konseptler: Classlar, Kalıtım (Inheritance), Kapsülleme (Encapsulation)

✨ Temel Özellikler
Kitap Yönetimi: Yeni kitap ekleme, detay görüntüleme ve silme.

Kullanıcı Sistemi: Kişisel kitaplığım sayfası ve kullanıcı etkileşimi.

Dinamik Web Arayüzü: HTML şablonları (Templates) ile kullanıcı dostu tasarım.


# Hastane Randevu Sistemi (Hospital Appointment System)
Bu uygulama, hastaların polikliniklere ve doktorlara randevu almasını sağlayan, Nesne Tabanlı Programlama (OOP) mimarisi üzerine inşa edilmiş bir yönetim sistemidir.

🛠 Kullanılan Teknolojiler
Dil: Python

Web Çatısı: Flask / Django

Veritabanı: SQLite / PostgreSQL

Mimari: Model-View-Template (MVT)

🧩 OOP Yaklaşımı ve Sınıf Yapısı
Projede OOP prensiplerini uygulamak adına aşağıdaki temel sınıflar ve ilişkiler kullanılmıştır:

Kullanıcı (User) Sınıfı: Ortak özellikleri (Ad, Soyad, TC No) içeren temel sınıf (Base Class).

Hasta & Doktor Sınıfları: Kullanıcı sınıfından türetilen (Inheritance) alt sınıflar.

Randevu Sınıfı: Tarih, saat ve doktor-hasta eşleşmelerini yöneten sınıf.

✨ Temel Özellikler
Randevu Alma: Hastaların uygun tarih ve saate randevu oluşturabilmesi.

Doktor Paneli: Doktorların kendi randevu programlarını görüntüleyebilmesi.

Poliklinik Yönetimi: Branşlara göre doktor filtreleme ve listeleme.

Validasyon: Aynı saat dilimine mükerrer randevu alınmasını engelleyen kontrol mekanizması. 
