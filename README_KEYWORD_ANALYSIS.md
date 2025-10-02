# 🔍 Comprehensive Keyword Analysis Tool

Bu araç, web sitelerini ve metinleri kapsamlı bir şekilde analiz ederek anahtar kelime önerileri ve SEO raporları sunar. Tüm analiz raporları ve yapılandırılmış veri dosyaları masaüstünde otomatik olarak oluşturulan klasöre kaydedilir.

## ✨ Özellikler

### 🎯 Anahtar Kelime Analizi
- **Kelime Yoğunluğu Analizi**: Her kelimenin içerikteki yoğunluğunu hesaplar
- **Anahtar Kelime Grupları**: 2-4 kelimelik önemli ifadeleri tespit eder
- **TF-IDF Analizi**: En önemli ve benzersiz terimleri belirler
- **Semantik Kümeleme**: İçeriği konulara göre gruplandırır

### 📊 Gelişmiş Analiz
- **Duygu Analizi**: İçeriğin genel tonunu değerlendirir
- **Okunabilirlik Analizi**: Metnin okunma zorluğunu ölçer
- **Metadata Analizi**: Başlık, açıklama ve header etiketlerini inceler
- **Kelime Bulutu**: Görsel anahtar kelime haritası oluşturur

### 🏆 Rekabet Analizi
- **Çoklu Site Karşılaştırması**: Rakip sitelerin anahtar kelimelerini analiz eder
- **Ortak Anahtar Kelimeler**: Sektördeki yaygın terimleri tespit eder
- **Benzersiz Fırsatlar**: Rakiplerin kullanmadığı anahtar kelimeleri bulur
- **Benzerlik Matrisi**: Siteler arası anahtar kelime benzerliğini gösterir

### 🤖 AI Destekli Öneriler
- **Otomatik SEO Önerileri**: GPT-4 ile oluşturulan özelleştirilmiş öneriler
- **Anahtar Kelime Optimizasyonu**: Yoğunluk ve dağılım önerileri
- **İçerik Geliştirme**: Eksik konular ve fırsatlar
- **Teknik SEO**: Metadata ve yapısal iyileştirmeler

## 🚀 Kurulum

### Gereksinimler
```bash
pip install -r requirements.txt
```

### OpenAI API Anahtarı
`.env` dosyası oluşturun:
```
OPENAI_API_KEY=your_api_key_here
```

## 💻 Kullanım

### 1. Komut Satırı Kullanımı

#### Tek URL Analizi
```bash
python comprehensive_keyword_tool.py https://example.com
```

#### Rekabet Analizi ile URL Analizi
```bash
python comprehensive_keyword_tool.py https://example.com --competitors https://competitor1.com https://competitor2.com
```

#### Metin Analizi
```bash
python comprehensive_keyword_tool.py --text "Analiz edilecek metin buraya" --title "Başlık" --description "Açıklama"
```

#### Çoklu URL Analizi
```bash
python comprehensive_keyword_tool.py --multiple https://site1.com https://site2.com https://site3.com
```

#### Dosyadan URL Listesi
```bash
python comprehensive_keyword_tool.py --file urls.txt
```

### 2. İnteraktif Mod
```bash
python comprehensive_keyword_tool.py
```

### 3. Demo Çalıştırma
```bash
python demo_keyword_analysis.py
```

## 📁 Çıktı Dosyaları

Araç, masaüstünde otomatik olarak `Keyword_Analysis_Reports_YYYYMMDD_HHMMSS` klasörü oluşturur:

```
Keyword_Analysis_Reports_20241002_143022/
├── HTML_Reports/                 # Görsel raporlar
│   ├── Keyword_Analysis_example_com_20241002_143022.html
│   └── Comparative_Analysis_20241002_143022.html
├── JSON_Data/                    # Yapılandırılmış veriler
│   └── Analysis_Data_example_com_20241002_143022.json
├── CSV_Exports/                  # Spreadsheet verileri
│   └── Keywords_example_com_20241002_143022.csv
└── Competitive_Analysis/         # Rekabet analizi verileri
    └── Competitive_Data_example_com_20241002_143022.json
```

## 📊 Rapor İçeriği

### HTML Raporu Bölümleri
1. **📊 Analiz Özeti**: Genel istatistikler ve kaynak bilgileri
2. **🎯 Anahtar Kelime Yoğunluğu**: En sık kullanılan kelimeler ve yoğunlukları
3. **🔗 Anahtar İfadeler**: Çok kelimeli önemli ifadeler
4. **🧠 Semantik Kümeler**: AI ile konusal gruplandırma
5. **📐 TF-IDF Analizi**: Terim önem skorları
6. **😊 Duygu Analizi**: İçerik tonunun değerlendirmesi
7. **📚 Okunabilirlik**: Metin zorluğu ve okunma süresi
8. **🏷️ Metadata Anahtar Kelimeleri**: SEO etiketlerinden çıkarılan kelimeler
9. **☁️ Kelime Bulutu**: Görsel anahtar kelime haritası
10. **🏆 Rekabet Analizi**: (varsa) Rakip karşılaştırması
11. **🚀 AI Önerileri**: Kişiselleştirilmiş optimizasyon önerileri

### JSON Veri Yapısı
```json
{
  "main_analysis": {
    "text_statistics": {...},
    "primary_keywords": [...],
    "keyword_density": {...},
    "key_phrases": [...],
    "semantic_clusters": [...],
    "tfidf_keywords": [...],
    "sentiment_analysis": {...},
    "readability_analysis": {...},
    "metadata_keywords": {...},
    "ai_recommendations": [...]
  },
  "competitive_data": {...},
  "generated_at": "2024-10-02T14:30:22",
  "source": "https://example.com"
}
```

## 🔧 Gelişmiş Özellikler

### Çoklu Dil Desteği
- Otomatik dil tespiti
- Türkçe dahil 100+ dil desteği
- Dile özel stop-word filtreleme

### Performans Optimizasyonu
- Paralel işleme desteği
- Bellek verimli analiz
- Büyük içerikler için chunk işleme

### Özelleştirilebilir Analiz
- Anahtar kelime sayısı limitleri
- Yoğunluk eşikleri
- Kümeleme parametreleri

## 🛠️ API Kullanımı

```python
from comprehensive_keyword_tool import ComprehensiveKeywordTool

# Araç örneği oluştur
tool = ComprehensiveKeywordTool()

# URL analizi
result = tool.analyze_url_comprehensive("https://example.com")

# Metin analizi
result = tool.analyze_text_comprehensive(
    text="Analiz edilecek metin",
    title="Başlık",
    description="Açıklama"
)

# Çoklu URL analizi
result = tool.analyze_multiple_urls([
    "https://site1.com",
    "https://site2.com"
])

# Sonuçları yazdır
tool.print_analysis_summary(result)
```

## 📈 Kullanım Senaryoları

### 1. SEO Optimizasyonu
- Mevcut içeriğin anahtar kelime performansını değerlendirin
- Eksik anahtar kelimeleri tespit edin
- Yoğunluk optimizasyonu yapın

### 2. İçerik Stratejisi
- Rakip analizi ile fırsat alanları bulun
- Trend anahtar kelimeleri tespit edin
- İçerik boşluklarını belirleyin

### 3. Rekabet İntelijansi
- Rakiplerin anahtar kelime stratejilerini analiz edin
- Pazar fırsatlarını keşfedin
- Benzersiz konumlandırma fırsatları bulun

### 4. İçerik Kalitesi
- Okunabilirlik skorunu iyileştirin
- Duygu tonunu optimize edin
- Kullanıcı deneyimini artırın

## ⚠️ Önemli Notlar

- **OpenAI API Anahtarı**: Geçerli bir API anahtarı gereklidir
- **İnternet Bağlantısı**: URL analizleri için internet gereklidir
- **Dosya Boyutu**: Çok büyük metinler için performans etkilenebilir
- **Rate Limiting**: OpenAI API limitlerini göz önünde bulundurun

## 🔍 Sorun Giderme

### Yaygın Hatalar
1. **API Anahtarı Hatası**: `.env` dosyasını kontrol edin
2. **URL Erişim Hatası**: Site erişilebilirliğini kontrol edin
3. **Bellek Hatası**: Daha küçük metin parçaları kullanın
4. **Encoding Hatası**: UTF-8 kodlaması kullanın

### Performans İyileştirme
- Küçük metin parçaları ile test edin
- Gereksiz anahtar kelime filtrelerini kullanın
- Paralel işleme için CPU çekirdek sayısını artırın

## 📞 Destek

Herhangi bir sorun veya öneriniz için:
- GitHub Issues kullanın
- Detaylı hata logları paylaşın
- Kullanım senaryonuzu açıklayın

## 🎯 Gelecek Özellikler

- [ ] Görsel anahtar kelime haritaları
- [ ] Sosyal medya analizi entegrasyonu
- [ ] Otomatik rapor planlama
- [ ] API endpoint'leri
- [ ] Veritabanı entegrasyonu
- [ ] Çoklu format export (PDF, Excel)

---

**🚀 Comprehensive Keyword Analysis Tool** - AI destekli gelişmiş anahtar kelime analizi ve SEO optimizasyonu için profesyonel çözüm.