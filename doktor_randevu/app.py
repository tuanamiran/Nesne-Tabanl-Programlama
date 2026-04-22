from flask import Flask, render_template, request, redirect, url_for, flash
# randevu_system.py dosyanın içindeki sınıfları buraya bağlıyoruz
from randevu_system import Doktor, Hasta, Randevu

app = Flask(__name__)
app.secret_key = 'gizli_anahtar_123'  # Flash mesajları için gerekli

# --- Mock Veri ---
UZMANLAR = [
    {
        "id": 1,
        "ad": "Dr. Ayşe Yılmaz",
        "uzmanlik": "Kıdemli Cilt Uzmanı",
        "fiyat": 85,
        "puan": "4.9",
        "inceleme_sayisi": 120,
        "tecrube": "12 Yıl",
        "hasta_sayisi": "2.4k+",
        "diller": "TR, EN",
        "biyografi": "Dr. Ayşe Yılmaz, estetik dermatoloji ve karmaşık cilt hastalıkları konusunda uzmanlaşmış kurul sertifikalı bir dermatologdur. 12 yılı aşkın klinik tecrübesiyle, en son tıbbi gelişmeleri kişiselleştirilmiş bir yaklaşımla birleştirir.",
        "fotograf": "https://lh3.googleusercontent.com/aida-public/AB6AXuBL1hsvgjxYfnOkwhLzTgJ9Y60x9SlzFMWiyW512FLbQhmounjatSKH3gHZU7qpHNQoKAhymgtTG92xfDWw-ZITwS18nGfK8g1kmjKwutPN724KAAEC05C9TYhYxIP3OuwRp_DKk1YYHEi9j4Fkqehs4aEcb57558lQHHURUr6253nV8M4zdLEtMoc6-8hOpSeqZn64BQntfDPKqsRN5QrlVOlDsysz3PaTA3JaaRDJR4OnxdtuzCGs2BE4aoc9hZJLonLa6cljFg"
    },
    {
        "id": 2,
        "ad": "Dr. Mehmet Çelik",
        "uzmanlik": "Bütünsel Zindelik Koçu",
        "fiyat": 120,
        "puan": "4.8",
        "inceleme_sayisi": 95,
        "tecrube": "15 Yıl",
        "hasta_sayisi": "3.1k+",
        "diller": "TR, EN, DE",
        "biyografi": "Dr. Mehmet Çelik, fiziksel ve zihinsel sağlığı bir bütün olarak ele alan, uluslararası deneyime sahip bir yaşam ve zindelik koçudur. Kişiye özel programlarla danışanlarının hayat kalitesini artırmayı hedefler.",
        "fotograf": "https://lh3.googleusercontent.com/aida-public/AB6AXuBnLtVwNP2soAa-EwRQY_CQmkFqr1VHXxFtrYXiqbBWN96RfohHVF97CZYHF05v2LCwkQLN4mtYpBNq-BNA8dsp6DOE786S8Eys7bFsHBX0rNnwiteC9ozPQrpYQnstEPt9GODIb3uXYMTbWaWcA2PYkVbVnEGtGNRCOJfGgZSYBscjdLWppEsrwD8GXO9qxoV94QsTC39CH3GrKuvftT10tiKgjyQmkVy27IrFk_8C86p8ygzyXzCTGBnY_huY5blWRekAY9D8Xg"
    },
    {
        "id": 3,
        "ad": "Ali Veli",
        "uzmanlik": "İç Mekan Danışmanlığı",
        "fiyat": 90,
        "puan": "4.7",
        "inceleme_sayisi": 80,
        "tecrube": "8 Yıl",
        "hasta_sayisi": "1.2k+",
        "diller": "TR, EN",
        "biyografi": "Ali Veli, yaşam alanlarınızı hem fonksiyonel hem de estetik açıdan mükemmelleştirmek için yaratıcı çözümler sunan bir iç mimardır. Modern ve minimalist tasarımlarla ruhunuzu yansıtan mekanlar oluşturur.",
        "fotograf": "https://lh3.googleusercontent.com/aida-public/AB6AXuAhitLDTao30m-HCRmLilvisum813NrYhMKh18h7s70MI71suED5HKTWAXCUu7xt8hoODnG7YFt03qjZ3cyG-OFxucjHldiqf_k1ZmQHWFdpF8mJxbBoWaEuh9utxCrD_25DAC21IM8rBwsYwhDXMXFD-6pW541EmnZlFJXLy5FVFg4SlVdiza4JuYOdKEXr3fBgKcumQLNHsT2mPWm42khHuKyJw2567VlTq_M-cUwW67bCH5GeVXFXTFcNyuVX4tW9L4ufht6dQ"
    },
    {
        "id": 4,
        "ad": "Zeynep Demir",
        "uzmanlik": "Özel Yoga Dersi",
        "fiyat": 60,
        "puan": "4.9",
        "inceleme_sayisi": 150,
        "tecrube": "10 Yıl",
        "hasta_sayisi": "2.8k+",
        "diller": "TR",
        "biyografi": "Zeynep Demir, zihin ve beden dengesini kurmaya odaklanan deneyimli bir yoga eğitmenidir. Birebir seanslarla esneklik, güç ve iç huzuru kazanmanıza yardımcı olur.",
        "fotograf": "https://lh3.googleusercontent.com/aida-public/AB6AXuCYt4Gsovl4irZYbA857Ua6cTviC081ZK7IbrSGcRE4yaWE8Mi24b4-I-yVwfctf4eu8j5tPvZDIi6aBBJBNLNzBhE9v7NR-Ca1sLUXfmtFzPbxP8ZQlcBAz_2IQ03wqX5MLUAaB1W6W1twv1yjKZYer0fjkw3cVn8ptawkp6iPzmg4O80pkBNukWM8jmccf_eD4RD_Xdi216GlYSy2aYhqptpmDHe2msvRb8u60gWVJg5jNY5FbrQ1PHr_bTNgWYMxZ8b5bEq7yg"
    }
]

# --- Rotalar (Sayfalar Arası Geçişler) ---

# 1. Ana Sayfa (Keşfet)
@app.route('/')
def index():
    populer_uzmanlar = UZMANLAR[:2]
    son_goruntulenenler = UZMANLAR[2:]
    return render_template('index.html', populer_uzmanlar=populer_uzmanlar, son_goruntulenenler=son_goruntulenenler)

# 2. Uzman Detay Sayfası
@app.route('/doktor/<int:doktor_id>')
def uzman_detay(doktor_id):
    doktor = next((u for u in UZMANLAR if u['id'] == doktor_id), None)
    if not doktor:
        flash("Uzman bulunamadı!", "error")
        return redirect(url_for('index'))
    return render_template('uzman_detay.html', doktor=doktor)

# 3. Zaman Seçimi Sayfası
@app.route('/zaman-secimi')
def zaman_secimi():
    doktor_id = request.args.get('doktor_id', 1, type=int)
    doktor = next((u for u in UZMANLAR if u['id'] == doktor_id), UZMANLAR[0])
    return render_template('zaman_secimi.html', doktor=doktor)

# 4. Randevularım Sayfası
@app.route('/randevularim')
def randevularim():
    # URL parametresinden TC'yi al (Örn: /randevularim?tc=12345678901)
    tc = request.args.get('tc', '12345678901') 
    randevular = Randevu.hastanin_randevularini_getir(tc)
    return render_template('randevularim.html', randevular=randevular)

# --- İşlemler (Form İşleme) ---

# 5. Randevu Alma İşlemi
@app.route('/randevu-al', methods=['POST'])
def randevu_al():
    # Form verilerini al
    ad = request.form.get('ad')
    tc = request.form.get('tc')
    telefon = request.form.get('telefon')
    doktor_id = request.form.get('doktor_id')
    tarih = request.form.get('tarih')
    saat = request.form.get('saat')

    # Hasta nesnesi oluştur ve randevu al
    hasta = Hasta(ad, tc, telefon)
    basarili, mesaj = hasta.randevu_al(int(doktor_id), tarih, saat)
    
    if basarili:
        flash("Randevunuz başarıyla oluşturuldu!", "success")
        return redirect(url_for('randevularim', tc=tc))
    else:
        flash(f"Hata: {mesaj}", "error")
        return redirect(url_for('uzman_detay', doktor_id=doktor_id))

# --- Sunucuyu Başlatma ---
if __name__ == '__main__':
    app.run(debug=True)