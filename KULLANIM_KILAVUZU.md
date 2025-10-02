# 🚀 Kapsamlı Anahtar Kelime Analiz Aracı - Kullanım Kılavuzu

## 📋 Özet

Bu araç, web sitelerini ve metinleri kapsamlı bir şekilde analiz ederek anahtar kelime önerileri ve SEO raporları sunar. **Tüm analiz raporları ve yapılandırılmış veri dosyaları masaüstünde otomatik olarak oluşturulan klasöre kaydedilir.**

## ✨ Ana Özellikler

### 🎯 Anahtar Kelime Analizi
- **Kelime Yoğunluğu**: Her kelimenin içerikteki yoğunluğunu hesaplar
- **Anahtar İfadeler**: 2-4 kelimelik önemli ifadeleri tespit eder
- **TF-IDF Analizi**: En önemli ve benzersiz terimleri belirler
- **Semantik Kümeleme**: İçeriği konulara göre gruplandırır

### 📊 Gelişmiş Analiz
- **Duygu Analizi**: İçeriğin genel tonunu değerlendirir
- **Okunabilirlik**: Metnin okunma zorluğunu ölçer
- **Metadata Analizi**: SEO etiketlerini inceler
- **Kelime Bulutu**: Görsel anahtar kelime haritası

### 🏆 Rekabet Analizi
- **Çoklu Site Karşılaştırması**: Rakip sitelerin anahtar kelimelerini analiz eder
- **Ortak Anahtar Kelimeler**: Sektördeki yaygın terimleri tespit eder
- **Benzersiz Fırsatlar**: Rakiplerin kullanmadığı anahtar kelimeleri bulur

### 🤖 AI Destekli Öneriler
- **Otomatik SEO Önerileri**: GPT-4 ile oluşturulan özelleştirilmiş öneriler
- **Anahtar Kelime Optimizasyonu**: Yoğunluk ve dağılım önerileri
- **İçerik Geliştirme**: Eksik konular ve fırsatlar

## 🛠️ Kurulum

### 1. Gerekli Paketleri Yükle
```bash
pip install requests beautifulsoup4 openai python-dotenv textstat nltk scikit-learn wordcloud matplotlib plotly pandas numpy spellchecker langdetect
```

### 2. OpenAI API Anahtarı Ayarla
`.env` dosyası oluşturun ve API anahtarınızı ekleyin:
```
OPENAI_API_KEY=your_actual_api_key_here
```

## 💻 Kullanım Örnekleri

### 1. Tek URL Analizi
```bash
python3 comprehensive_keyword_tool.py https://example.com
```

### 2. Rekabet Analizi ile URL Analizi
```bash
python3 comprehensive_keyword_tool.py https://example.com --competitors https://competitor1.com https://competitor2.com
```

### 3. Metin Analizi
```bash
python3 comprehensive_keyword_tool.py --text "Analiz edilecek metin buraya gelir" --title "Başlık" --description "Açıklama"
```

### 4. Çoklu URL Analizi
```bash
python3 comprehensive_keyword_tool.py --multiple https://site1.com https://site2.com https://site3.com
```

### 5. Dosyadan URL Listesi
```bash
# urls.txt dosyası oluşturun (her satırda bir URL)
python3 comprehensive_keyword_tool.py --file urls.txt
```

### 6. İnteraktif Mod
```bash
python3 comprehensive_keyword_tool.py
```

### 7. Demo Çalıştırma
```bash
python3 demo_keyword_analysis.py
```

## 📁 Çıktı Dosyaları

Araç, masaüstünde otomatik olarak şu klasör yapısını oluşturur:

```
Keyword_Analysis_Reports_20241002_143022/
├── HTML_Reports/                 # 🌐 Görsel HTML raporları
│   ├── Keyword_Analysis_example_com_20241002_143022.html
│   └── Comparative_Analysis_20241002_143022.html
├── JSON_Data/                    # 📊 Yapılandırılmış JSON verileri
│   └── Analysis_Data_example_com_20241002_143022.json
├── CSV_Exports/                  # 📋 Excel/Spreadsheet verileri
│   └── Keywords_example_com_20241002_143022.csv
└── Competitive_Analysis/         # 🏆 Rekabet analizi verileri
    └── Competitive_Data_example_com_20241002_143022.json
```

## 📊 HTML Raporu İçeriği

Her HTML raporu şu bölümleri içerir:

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

## 🎯 Kullanım Senaryoları

### SEO Optimizasyonu
- Mevcut içeriğin anahtar kelime performansını değerlendirin
- Eksik anahtar kelimeleri tespit edin
- Yoğunluk optimizasyonu yapın

### İçerik Stratejisi
- Rakip analizi ile fırsat alanları bulun
- Trend anahtar kelimeleri tespit edin
- İçerik boşluklarını belirleyin

### Rekabet İntelijansi
- Rakiplerin anahtar kelime stratejilerini analiz edin
- Pazar fırsatlarını keşfedin
- Benzersiz konumlandırma fırsatları bulun

## 🔧 Komut Satırı Parametreleri

```bash
python3 comprehensive_keyword_tool.py [URL/metin] [seçenekler]

Seçenekler:
  --text, -t           Doğrudan metin analizi
  --title              Metin analizi için başlık
  --description, -d    Metin analizi için açıklama
  --competitors, -c    Rakip URL'leri (boşlukla ayrılmış)
  --multiple, -m       Çoklu URL analizi (boşlukla ayrılmış)
  --file, -f           URL listesi içeren dosya
```

## 📈 Performans İpuçları

### Hızlı Analiz İçin
- Küçük metin parçaları ile başlayın
- Tek URL analizi yapın
- Rekabet analizini sonraya bırakın

### Kapsamlı Analiz İçin
- Çoklu URL analizi kullanın
- Rekabet analizi ekleyin
- Büyük metin dosyalarını parçalara bölün

## ⚠️ Önemli Notlar

- **OpenAI API Anahtarı**: Geçerli bir API anahtarı gereklidir
- **İnternet Bağlantısı**: URL analizleri için gereklidir
- **Dosya Boyutu**: Çok büyük metinler performansı etkileyebilir
- **API Limitleri**: OpenAI API limitlerini göz önünde bulundurun

## 🔍 Sorun Giderme

### Yaygın Hatalar ve Çözümleri

**API Anahtarı Hatası**
```
❌ Error: OPENAI_API_KEY not found in .env file
```
**Çözüm**: `.env` dosyasını kontrol edin ve geçerli API anahtarı ekleyin

**URL Erişim Hatası**
```
❌ Error analyzing URL: Connection timeout
```
**Çözüm**: URL'nin erişilebilir olduğunu kontrol edin

**Paket Eksik Hatası**
```
ModuleNotFoundError: No module named 'requests'
```
**Çözüm**: Gerekli paketleri yükleyin: `pip install -r requirements.txt`

## 🚀 Gelişmiş Kullanım

### Python API Kullanımı
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

# Sonuçları yazdır
tool.print_analysis_summary(result)
```

### Toplu İşleme
```python
# Çoklu URL analizi
urls = [
    "https://site1.com",
    "https://site2.com",
    "https://site3.com"
]

result = tool.analyze_multiple_urls(urls)
```

## 📞 Destek ve Yardım

Herhangi bir sorun yaşarsanız:

1. **Hata Mesajını Kontrol Edin**: Genellikle sorunu açıklar
2. **API Anahtarını Doğrulayın**: En yaygın sorun budur
3. **İnternet Bağlantısını Kontrol Edin**: URL analizleri için gerekli
4. **Dosya İzinlerini Kontrol Edin**: Masaüstü klasörü oluşturma için

## 🎉 Başarı İpuçları

### En İyi Sonuçlar İçin
1. **Kaliteli İçerik Kullanın**: Daha iyi analiz için
2. **Rakip Analizi Yapın**: Fırsatları keşfetmek için
3. **Düzenli Analiz Yapın**: İçerik performansını takip etmek için
4. **AI Önerilerini Uygulayın**: SEO performansını artırmak için

### Zaman Tasarrufu İçin
1. **Demo ile Başlayın**: Aracı tanımak için
2. **Küçük Testler Yapın**: Büyük analizlerden önce
3. **Sonuçları Kaydedin**: Gelecekte karşılaştırma için

---

**🔍 Comprehensive Keyword Analysis Tool** - Profesyonel anahtar kelime analizi ve SEO optimizasyonu için AI destekli çözüm.

**Masaüstünde otomatik klasör oluşturma ve tüm raporları kaydetme özelliği ile tam otomatik analiz deneyimi!**