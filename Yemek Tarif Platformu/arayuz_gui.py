import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QListWidget, QStackedWidget, QMessageBox, 
                             QFrame, QComboBox)
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt

# veritabani baglantisi saglayan sinifin ice aktarilmasi
from yemek_sistemi import YemekTarifSistemi

# qwidget sinifindan miras alarak ana pencereyi temsil eden gui sinifi
class YemekPlatformuArayuzu(QWidget):
    # init yapici metodu: arayuz objesi yaratildigi an calisir
    def __init__(self, sistem_nesnesi):
        super().__init__()
        # arayuzun backend ile konusabilmesi icin sistem objesi hafizada tutulur
        self.sistem = sistem_nesnesi
        
        # arayuzu ve gorsel tasarimi baslatan zincirleme metod cagrilari
        self.pencere_yapilandir()
        self.stil_uygula()

    # ana formun geometrisini ve dikey-yatay duzenlerini ayarlayan ana metod
    def pencere_yapilandir(self):
        self.setWindowTitle("Yemek Tarif Platformu - Yönetici Paneli")
        self.resize(1150, 780)
        self.setFont(QFont("Segoe UI", 11))

        # form icerisindeki bilesenleri yukaridan asagiya siralayan ana layout
        self.ana_layout = QVBoxLayout()
        
        # sayfalari (sekmeleri) ust uste koyarak sadece secili olan indeksli sayfayi gosteren mekanizma
        self.sayfa_yoneticisi = QStackedWidget()

        self.ana_sayfa_hazirla()
        self.sayfa_yoneticisi.addWidget(self.ana_ekran)

        self.ana_layout.addWidget(self.sayfa_yoneticisi)
        # form cercevesi ile icerik arasindaki marging (dis bosluk) sifirlanir
        self.ana_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.ana_layout)

    # css (cascading style sheets) mantigi ile pyqt5 elemanlarina modern, koyu temali stil enjekte eder
    def stil_uygula(self):
        modern_qss = """
        QWidget {
            background-color: #18181b;
            color: #f4f4f5;
            font-family: 'Segoe UI', sans-serif;
        }
        /* sol menuyu iceren cerceveye sag sinir cizgisi ekler */
        QFrame#sol_menu {
            background-color: #09090b;
            border-right: 1px solid #27272a;
        }
        QLabel#ana_baslik {
            font-size: 20px;
            color: #f4f4f5;
            padding: 15px;
            letter-spacing: 1px;
        }
        /* sol menudeki dugmelerin baslangic stili */
        QPushButton#sol_menu_buton {
            background-color: transparent;
            color: #a1a1aa;
            text-align: left;
            padding: 16px 25px;
            font-size: 15px;
            border: none;
            border-left: 3px solid transparent;
        }
        /* fare sol menudeki bir butonun uzerine geldiginde (hover) tetiklenen animasyon stili */
        QPushButton#sol_menu_buton:hover {
            background-color: #27272a;
            color: #f4f4f5;
            border-left: 3px solid #3b82f6;
        }
        QLabel {
            font-size: 15px;
            color: #3b82f6;
            margin-bottom: 5px;
        }
        /* verileri listeleyen liste widget'inin gorsel ayarlari */
        QListWidget {
            background-color: #09090b;
            border: 1px solid #27272a;
            border-radius: 8px;
            padding: 10px;
            font-size: 15px;
            outline: none;
        }
        QListWidget::item {
            padding: 14px;
            border-bottom: 1px solid #18181b;
        }
        /* listwidget elemani uzerine fare geldigindeki efeti */
        QListWidget::item:hover {
            background-color: #27272a;
            border-radius: 6px;
        }
        /* liste icerisindeki bir satir secildiginde gosterilecek aktif renk stili */
        QListWidget::item:selected {
            background-color: #3b82f6;
            color: #ffffff;
            border-radius: 6px;
        }
        /* yazi girisi yapilan lineedit'ler ve secim yapilan combobox'larin ortak stili */
        QLineEdit, QComboBox {
            padding: 14px 15px;
            background-color: #09090b;
            border: 1px solid #27272a;
            border-radius: 6px;
            color: #f4f4f5;
            font-size: 14px;
        }
        /* yazi giris alanina tiklandiginda (focus) cerceve rengi degisir */
        QLineEdit:focus, QComboBox:focus {
            border: 1px solid #3b82f6;
            background-color: #18181b;
        }
        /* combobox icerisindeki asagiya acilan listenin (drop-down) yapilandirmasi */
        QComboBox::drop-down {
            border: none;
            padding-right: 10px;
        }
        QComboBox QAbstractItemView {
            background-color: #09090b;
            color: #f4f4f5;
            selection-background-color: #3b82f6;
            border: 1px solid #27272a;
            outline: none;
        }
        /* islemleri (veritabani ekleme/guncelleme) tetikleyen mavi renkteki ana buton stili */
        QPushButton#islem_butonu {
            padding: 14px;
            background-color: #3b82f6;
            color: #ffffff;
            border-radius: 6px;
            font-size: 15px;
        }
        QPushButton#islem_butonu:hover { background-color: #2563eb; }
        QPushButton#islem_butonu:pressed { background-color: #1d4ed8; }
        """
        self.setStyleSheet(modern_qss)

    # yatay duzende calisan (sol panel ve sag icerik) ikiye bolunmus ana ekrani insa eden metod
    def ana_sayfa_hazirla(self):
        self.ana_ekran = QWidget()
        layout = QHBoxLayout() # saga dogru yanyana dizilim yapar
        
        # --- 1. SOL MENU ALANININ OLUSTURULMASI ---
        sol_menu = QFrame()
        sol_menu.setObjectName("sol_menu")
        sol_menu.setFixedWidth(260)
        sol_layout = QVBoxLayout()
        sol_layout.setContentsMargins(0, 0, 0, 0)
        sol_layout.setSpacing(5)
        
        baslik = QLabel("TARİF YÖNETİMİ")
        baslik.setObjectName("ana_baslik")
        
        # sayfalari tetikleyecek gezinme dugmeleri tanimlanir
        self.btn_tarif_listesi = QPushButton("Tarif Listesi")
        self.btn_yeni_tarif = QPushButton("Yeni Tarif Ekle")
        self.btn_guncelleme = QPushButton("Tarif Güncelle")
        
        sol_layout.addWidget(baslik)
        sol_layout.addSpacing(15)

        # qss uzerinden css stili almalari icin objelere isimler islenir ve layout'a eklenir
        for btn in [self.btn_tarif_listesi, self.btn_yeni_tarif, self.btn_guncelleme]:
            btn.setObjectName("sol_menu_buton")
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            sol_layout.addWidget(btn)

        # butonlara sol tiklandiginda (clicked) sayfa yoneticisine sinyal gonderilir (signal-slot baglantisi)
        self.btn_tarif_listesi.clicked.connect(lambda: self.sekme_degistir(0))
        self.btn_yeni_tarif.clicked.connect(lambda: self.sekme_degistir(1))
        self.btn_guncelleme.clicked.connect(lambda: self.sekme_degistir(2))
        
        sol_layout.addStretch() # tasarimin alta yaslanmamasi icin yukaridan bastiran yay
        sol_menu.setLayout(sol_layout)

        # --- 2. SAG ICERIK ALANININ OLUSTURULMASI ---
        self.icerik_alani = QStackedWidget()
        
        # 3 farkli sayfanin (sekmenin) qwidget formlari ilgili metodlar tarafindan cizilir
        self.sekme_liste_olustur()
        self.sekme_ekle_olustur()
        self.sekme_guncelle_olustur()
        
        # cizilen bu 3 widget, sayfa yoneticisinin uzerine (index sirasiyla) yigilir
        self.icerik_alani.addWidget(self.liste_sekmesi) # index 0
        self.icerik_alani.addWidget(self.ekle_sekmesi) # index 1
        self.icerik_alani.addWidget(self.guncelle_sekmesi) # index 2

        # hazirlanan sol panel ve sag panel en son ana yatay duzene eklenir
        layout.addWidget(sol_menu)
        layout.addWidget(self.icerik_alani)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.ana_ekran.setLayout(layout)
        
        # liste sekmensi ilk acildiginda bos kalmasin diye guncelleme islevi cagirilir
        self.ekran_tazele()

    # sekme 1: veritabanindaki tum kayitlari goruntuleyen panel
    def sekme_liste_olustur(self):
        self.liste_sekmesi = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 40, 50, 40)
        
        # qlistwidget metinleri satir satir tutabilen interaktif bir objedir
        self.liste_tarifler = QListWidget()
        
        layout.addWidget(QLabel("Sistemdeki Kayıtlı Tarifler (ID   Ad   Kategori   Süre)"))
        layout.addSpacing(10)
        layout.addWidget(self.liste_tarifler)
        
        self.liste_sekmesi.setLayout(layout)

    # sekme 2: veritabanina insert islemi gonderen panel
    def sekme_ekle_olustur(self):
        self.ekle_sekmesi = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 50, 60, 50)
        
        # tek satirlik yazi okuma kutulari (qlineedit)
        self.in_id = QLineEdit()
        self.in_id.setPlaceholderText("Tarif ID")
        
        self.in_ad = QLineEdit()
        self.in_ad.setPlaceholderText("Tarif Adı")
        
        # kullanicinin serbest yazi girmesini onleyen, teknik kisitlama saglayan acilir kutu objesi (qcombobox)
        self.in_kat = QComboBox()
        self.in_kat.addItems(["Çorba", "Ana Yemek", "Ara Sıcak", "Zeytinyağlı", "Salata", "Tatlı", "İçecek"])
        
        self.in_sure = QLineEdit()
        self.in_sure.setPlaceholderText("Hazırlama Süresi (Dakika)")
        
        btn = QPushButton("Tarifi Veritabanına Kaydet")
        btn.setObjectName("islem_butonu")
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        # tiklandiginda kayit yapan metodu tetikler
        btn.clicked.connect(self.tarif_kaydet_islem)
        
        # bilesenler sayfaya duzenli bosluklarla (spacing) dahil edilir
        layout.addWidget(QLabel("Yeni Tarif Tanımlama Merkezi"))
        layout.addSpacing(15)
        layout.addWidget(self.in_id)
        layout.addSpacing(10)
        layout.addWidget(self.in_ad)
        layout.addSpacing(10)
        layout.addWidget(self.in_kat)
        layout.addSpacing(10)
        layout.addWidget(self.in_sure)
        layout.addSpacing(25)
        layout.addWidget(btn)
        layout.addStretch()
        
        self.ekle_sekmesi.setLayout(layout)

    # sekme 3: veritabanindaki bir kaydi id referansi ile update eden panel
    def sekme_guncelle_olustur(self):
        self.guncelle_sekmesi = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(60, 50, 60, 50)
        
        self.in_guncel_id = QLineEdit()
        self.in_guncel_id.setPlaceholderText("Güncellenecek Tarif ID Numarası")
        
        self.in_yeni_ad = QLineEdit()
        self.in_yeni_ad.setPlaceholderText("Yeni Tarif Adı")
        
        self.in_yeni_sure = QLineEdit()
        self.in_yeni_sure.setPlaceholderText("Yeni Hazırlama Süresi (Dakika)")
        
        btn = QPushButton("Tarif Bilgilerini Güncelle")
        btn.setObjectName("islem_butonu")
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        # tiklandiginda guncelleme yapan metodu tetikler
        btn.clicked.connect(self.tarif_guncelle_islem)
        
        layout.addWidget(QLabel("Mevcut Tarif Konfigürasyonu"))
        layout.addSpacing(15)
        layout.addWidget(self.in_guncel_id)
        layout.addSpacing(10)
        layout.addWidget(self.in_yeni_ad)
        layout.addSpacing(10)
        layout.addWidget(self.in_yeni_sure)
        layout.addSpacing(25)
        layout.addWidget(btn)
        layout.addStretch()
        
        self.guncelle_sekmesi.setLayout(layout)

    # sol menuden alinan index numarasi ile arayuzde acik olan sekmeyi yonetir
    def sekme_degistir(self, i):
        self.icerik_alani.setCurrentIndex(i)

    # sistemdeki tablo guncellendikce qlistwidget arayuzunu bosaltip veritabanindan tekrardan taze ceken metod
    def ekran_tazele(self):
        # eski verilerin ust uste yigilmamasi (duplication) icin clear kullanilir
        self.liste_tarifler.clear()
        
        # backend class'indaki select sorgusu calistirilir
        tarifler = self.sistem.tum_tarifleri_getir()
        
        # dondurulen veriler for dongusuyle arayuz formatina donusturulerel eklenir
        for t in tarifler:
            self.liste_tarifler.addItem(f"  {t[0]}   {t[1]}   {t[2]}   {t[3]} Dakika")

    # sekme 2'deki ekleme butonunun slot islevi
    def tarif_kaydet_islem(self):
        # kullanici kutulara sayi yerine harf girerse programin cokmemesi (crash) icin try/except hata ayiklama blogu
        try:
            # lineedit objesindeki veriler str'den int formatina parse (cast) edilir
            id_no = int(self.in_id.text())
            sure_no = int(self.in_sure.text())
            # combobox objesinde su an aktif olan metin .currentText() ile alinir
            kategori_secimi = self.in_kat.currentText()
            
            # backend nesnesinin metodu tetiklenir ve geriye islem durumu ile mesaj doner
            res, msg = self.sistem.tarif_ekle(id_no, self.in_ad.text(), kategori_secimi, sure_no)
            
            # qmessagebox ile kullaniciya gorsel bilgi baloncugu verilir
            QMessageBox.information(self, "Bilgi", msg)
            
            # listeye yeni veri girdigi icin ekran tazelenir
            self.ekran_tazele()
            
            # islem bittikten sonra input kutulari sonraki islem icin temizlenir (.clear) ve combobox en basa sari
            self.in_id.clear()
            self.in_ad.clear()
            self.in_kat.setCurrentIndex(0) 
            self.in_sure.clear()
            
        except ValueError:
            # eger parse sirasinda cast hatasi olduysa (int icine yazi yazildiysa) gosterilecek uyaridir
            QMessageBox.warning(self, "Sistem Uyarısı", "ID ve Süre alanlarına sadece sayısal veri girilmelidir.")

    # sekme 3'teki guncelle butonunun slot islevi
    def tarif_guncelle_islem(self):
        try:
            # arayuz verileri int degiskenlerine atanir
            id_no = int(self.in_guncel_id.text())
            sure_no = int(self.in_yeni_sure.text())
            
            # guncelleme yapmak uzere veriler yemek_sistemi backend'ine aktarilir
            res, msg = self.sistem.tarif_guncelle(id_no, self.in_yeni_ad.text(), sure_no)
            
            QMessageBox.information(self, "Bilgi", msg)
            self.ekran_tazele() # degisen veriyi listede canli gostermek icin guncelle
            
            self.in_guncel_id.clear()
            self.in_yeni_ad.clear()
            self.in_yeni_sure.clear()
            
        except ValueError:
            QMessageBox.warning(self, "Sistem Uyarısı", "ID ve Süre alanlarına sadece sayısal veri girilmelidir.")

# dunder main kontrolu: bu dosya module olarak projeye dahil edilmek yerine bizzat komut satirindan calistirilmissa kod blogunu aktif et
if __name__ == "__main__":
    # pyqt5 projelerinin calisabilmesi icin sistem argumanlariyla zorunlu olarak bir qapplication objesi olusturulmalidir
    app = QApplication(sys.argv)
    
    # 1. oncelikle arka plan veritabani mimarisi baslatilir (sistem nesnesi)
    backend = YemekTarifSistemi()
    
    # 2. olusan sistem nesnesi, arayuz nesnesine yapici metod sirasinda arguman olarak atanarak aralarindaki kopru kurulur
    pencere = YemekPlatformuArayuzu(backend)
    
    # olusturulan widget (pencere) ekranda gosterilir
    pencere.show()
    
    # programdaki x tusuna veya sistem exit verisine basilana kadar programin memory (ram) uzerinde bir sonsuz dongude calismasini saglayan eylem zinciri baslatilir
    sys.exit(app.exec_())