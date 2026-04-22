// Sayfa yüklendiğinde ayarı kontrol et
document.addEventListener('DOMContentLoaded', () => {
    const toggleButton = document.getElementById('theme-toggle'); // HTML'deki butonunun ID'si

    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            // Tailwind için 'dark' sınıfını html etiketine ekleyip çıkarıyoruz
            document.documentElement.classList.toggle('dark');

            // Kullanıcının tercihini tarayıcıya kaydet
            if (document.documentElement.classList.contains('dark')) {
                localStorage.setItem('theme', 'dark');
            } else {
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // Sayfa açıldığında daha önce seçilen modu uygula
    if (localStorage.getItem('theme') === 'dark') {
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
    } else {
        document.documentElement.classList.remove('dark');
        document.documentElement.classList.add('light');
    }
});
