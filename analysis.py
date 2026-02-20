import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

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
                'price': latest_price
            })

df = pd.DataFrame(clean_data)

q1 = df['price'].quantile(0.25)
q3 = df['price'].quantile(0.75)
iqr = q3 - q1
upper_bound = q3 + 1.5 * iqr

anomalies = df[df['price'] > upper_bound]

X = df['price'].values.reshape(-1, 1)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['segment'] = kmeans.fit_predict(X)

centers = kmeans.cluster_centers_.flatten()
sorted_idx = np.argsort(centers)
mapping = {sorted_idx[0]: 'Ekonomik', sorted_idx[1]: 'Standart', sorted_idx[2]: 'Premium'}
df['segment_label'] = df['segment'].map(mapping)

plt.figure(figsize=(12, 6))
colors = {'Ekonomik': '#2ecc71', 'Standart': '#3498db', 'Premium': '#e74c3c'}
for label, color in colors.items():
    subset = df[df['segment_label'] == label]
    plt.scatter(subset.index, subset['price'], c=color, label=label, alpha=0.6, s=15)

plt.axhline(y=upper_bound, color='gray', linestyle='--', label='Anomali Sınırı')
plt.title('Flo Ayakkabı Pazarı Segmentasyon ve Anomali Analizi')
plt.ylabel('Fiyat (TL)')
plt.legend()
plt.grid(True, alpha=0.3)

print(f"Veri Seti Boyutu: {len(df)}")
print(f"Anomali Eşiği: {upper_bound:.2f} TL")
print(f"Toplam Anomali Sayısı: {len(anomalies)}")
print("\n--- Segment İstatistikleri ---")
print(df.groupby('segment_label')['price'].agg(['mean', 'count', 'min', 'max']))

plt.tight_layout()
plt.show()