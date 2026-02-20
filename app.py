import streamlit as st
import pymongo
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import plotly.express as px

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Flo Fiyat Takip Paneli", layout="wide")

st.title("👟 Flo.com.tr Akıllı Fiyat Analiz Paneli")
st.markdown(
    "Bu proje, **Scrapy** ile toplanan verileri **MongoDB**'de saklar ve **Yapay Zeka (K-Means)** ile analiz ederek pazar segmentlerini ve fiyat anomalilerini canlı olarak sunar.")


# --- 1. Veri Yükleme ve Temizlik (Önbellekleme ile Hızlandırılmış) ---
@st.cache_data(ttl=600)  # Veriyi 10 dakikada bir yenile
def load_data():
    client = pymongo.MongoClient('mongodb://localhost:27017/')
    db = client['flo_monitoring']
    collection = db['prices']
    raw_data = list(collection.find())

    clean_data = []
    shoe_keywords = ['Ayakkabı', 'Sneaker', 'Bot', 'Terlik', 'Sandalet', 'Çizme', 'Loafer', 'Spor']
    junk_brands = ['Unisex', 'Erkek', 'Günlük', 'Siyah', 'Beyaz', '311729', '392336-08', 'SSC911']

    for item in raw_data:
        if 'price_history' in item and len(item['price_history']) > 0:
            latest_price = item['price_history'][-1]['price']
            model_name = item.get('model', '').lower()
            brand = item.get('brand', 'Unknown')

            is_shoe = any(keyword.lower() in model_name for keyword in shoe_keywords)

            if is_shoe and latest_price < 8000 and brand not in junk_brands:
                clean_data.append({
                    'brand': brand,
                    'model': item.get('model', 'Unknown'),
                    'price': latest_price,
                    'url': item.get('url', '')
                })
    return pd.DataFrame(clean_data)


with st.spinner('Veriler MongoDB\'den çekiliyor ve yapay zeka ile işleniyor...'):
    df = load_data()

# --- 2. AI Segmentasyon ve Anomali Analizi ---
X = df['price'].values.reshape(-1, 1)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['segment'] = kmeans.fit_predict(X)

centers = kmeans.cluster_centers_.flatten()
sorted_idx = np.argsort(centers)
mapping = {sorted_idx[0]: 'Ekonomik', sorted_idx[1]: 'Standart', sorted_idx[2]: 'Premium'}
df['segment_label'] = df['segment'].map(mapping)

q1 = df['price'].quantile(0.25)
q3 = df['price'].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr
anomalies = df[df['price'] > upper_bound]

# --- 3. Görselleştirme (KPI'lar) ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Toplam Ayakkabı", f"{len(df)}")
col2.metric("Ortalama Fiyat", f"{df['price'].mean():.0f} TL")
col3.metric("Anomali Eşiği", f"{upper_bound:.0f} TL")
col4.metric("Tespit Edilen Anomali", f"{len(anomalies)}", delta_color="inverse")

# --- 4. İnteraktif Grafik (Plotly) ---
st.subheader("📊 Yapay Zeka Destekli Pazar Segmentasyonu")
st.markdown(
    "Aşağıdaki grafik **interaktiftir**. Noktaların üzerine gelerek ayakkabının modelini ve fiyatını görebilirsiniz. Kırmızı noktalar Premium segmenti, kesikli çizgi ise anomali sınırını gösterir.")

fig = px.scatter(
    df,
    x=df.index,
    y="price",
    color="segment_label",
    color_discrete_map={'Ekonomik': '#2ecc71', 'Standart': '#3498db', 'Premium': '#e74c3c'},
    hover_data=['brand', 'model', 'price'],
    labels={'price': 'Fiyat (TL)', 'index': 'Ürün ID', 'segment_label': 'Segment'},
    title="Flo Erkek Ayakkabı Fiyat Dağılımı"
)

# Anomali çizgisi ekle
fig.add_hline(y=upper_bound, line_dash="dash", line_color="gray", annotation_text="Anomali Sınırı")
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

# --- 5. Veri Tablosu (Anomaliler) ---
st.subheader("🚨 Dikkat Çeken Anomaliler (En Pahalı 20 Ürün)")
st.dataframe(anomalies.sort_values(by='price', ascending=False).head(20)[['brand', 'model', 'price', 'segment_label']])