# 👟 Flo Akıllı Fiyat Analiz & Segmentasyon Paneli

Bu proje, **Scrapy** kullanarak Flo.com.tr üzerindeki erkek ayakkabı verilerini çeken, **MongoDB** üzerinde depolayan ve **Yapay Zeka (K-Means Clustering)** algoritmasıyla pazar segmentasyonu yapan uçtan uca bir veri bilimi uygulamasıdır.

## 🚀 Proje Amacı
- E-ticaret verilerini asenkron ve hızlı bir şekilde toplamak.
- Veri temizliği (Data Cleaning) yaparak anlamlı veri setleri oluşturmak.
- Ürünleri 'Ekonomik', 'Standart' ve 'Premium' olarak segmente etmek.
- IQR yöntemiyle fiyat anomalilerini (aşırı düşük/yüksek fiyatlar) tespit etmek.

## 🛠️ Kullanılan Teknolojiler
- **Python** (Veri İşleme ve Analiz)
- **Scrapy** (Web Crawling & Scraping)
- **MongoDB** (NoSQL Veri Depolama)
- **Scikit-Learn** (K-Means Clustering - Yapay Zeka)
- **Streamlit & Plotly** (İnteraktif Dashboard)

## 📊 Analiz Özeti
Proje kapsamında 3.000+ ürün taranmış ve yapay zeka modeliyle fiyat haritası çıkarılmıştır. Elde edilen veriler interaktif grafiklerle görselleştirilmiştir.

## 📱 Projeden Görüntüler

### Yapay Zeka Destekli Analiz Paneli (Streamlit)
Aşağıdaki görsel, projenin canlı çalışan veri panelinden alınmıştır. Panelde anlık KPI metrikleri ve K-Means algoritması ile oluşturulan interaktif segmentasyon grafiği görülmektedir.

![Streamlit Dashboard Önizlemesi](panel.png)

## ⚙️ Kurulum ve Çalıştırma
1. `git clone https://github.com/Cxnse/flo-price-tracker.git`
2. `pip install -r requirements.txt`
3. Veri çekmek için: `scrapy crawl flo`
4. Analiz panelini açmak için: `streamlit run app.py`