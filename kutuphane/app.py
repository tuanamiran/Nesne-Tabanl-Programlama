from flask import Flask, render_template, request
import kutuphane_system as ks  # Kendi yazdığın sistem dosyası

app = Flask(__name__)

# --- ROTALAR ---

@app.route('/')
def index():
    # Keşfet (Anasayfa) - Tüm kitapları veya öne çıkanları getirir
    kitaplar = ks.Kitap.tum_kitaplari_getir() 
    return render_template('index.html', kitaplar=kitaplar)

@app.route('/arama')
def arama():
    # Arama ve filtreleme fonksiyonu
    sorgu = request.args.get('q', '')
    # ks.Kitap.kitap_ara(sorgu) ile arama yapıyoruz. Sorgu boşsa tüm kitapları getirmemesi için boş liste döndürüyoruz.
    sonuclar = ks.Kitap.kitap_ara(sorgu) if sorgu else []
    return render_template('arama.html', sonuclar=sonuclar, sorgu=sorgu)

@app.route('/kitap/<int:kitap_id>')
def kitap_detay(kitap_id):
    # Kitap detay sayfası
    kitap = ks.Kitap.kitap_getir(kitap_id)
    return render_template('kitap_detay.html', kitap=kitap)

@app.route('/kitapligim')
def kitapligim():
    # Kitaplığım sayfası
    # ks.Kitap.kitapligimi_getir() ile ödünçte olan kitapları listeliyoruz.
    okunanlar = ks.Kitap.kitapligimi_getir()
    return render_template('kitapligim.html', kitaplar=okunanlar)

@app.route('/gecmis')
def gecmis():
    gecmis_kitaplar = ks.Kitap.gecmisi_getir()
    return render_template('gecmis.html', kitaplar=gecmis_kitaplar)

if __name__ == '__main__':
    # Hata ayıklama için debug=True açık
    app.run(debug=True)