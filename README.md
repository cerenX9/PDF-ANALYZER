# 📄 AI-Powered PDF Analyzer & Parser
### 🚀 Modern OOP Mimari • Katmanlı Test Otomasyonu (Pytest) • Google Gemini LLM API Entegrasyonu

Modern Nesne Yönelimli Programlama (OOP) prensipleriyle tasarlanmış, tam kapsamlı ve katmanlı otomatik test otomasyonuna (Pytest) sahip, Google Gemini LLM API entegrasyonlu ve Streamlit tabanlı kurumsal bir PDF analiz, dijitalleştirme ve işleme sistemidir.

Bu proje; gevşek bağlılık (Loose Coupling), yüksek modülerlik, Test Güdümlü Geliştirme (TDD) ve reaktif kullanıcı deneyimi (UX) yaklaşımları göz önünde bulundurularak üretim ortamına (Production) uygun standartlarda geliştirilmiştir.

---

<div align="center">

🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀

**[🌐 CANLI UYGULAMAYI TARAYICIDA AÇIN🚀 (LIVE DEMO) →](https://pdf-analyzer-hktrdgmmnwqrdxg8bwgbw7.streamlit.app/)**

*Gelişmiş Nesne Yönelimli Programlama (OOP) prensipleriyle tasarlanmış, tam kapsamlı otomatik test süreçlerine ve Streamlit tabanlı dinamik kullanıcı arayüzüne sahip kurumsal PDF işleme platformu.*
🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀
---
</div>


---

## 🚀 Öne Çıkan Özellikler ve Mühendislik Pratikleri

* **Temiz ve Katmanlı Mimari (Clean Architecture):** Sunum (Arayüz) katmanı (`app.py`) ile İş Mantığı (Business Logic) katmanı (`core/`) tamamen birbirinden izole edilmiştir. Bu sayede yarın bir gün Streamlit arayüzü yerine FastAPI veya Django entegre edilmek istendiğinde `core/` paketine dokunulması gerekmez.
* **Streamlit ile Bellek Optimize Reaktif UI:** Kullanıcıların yüklediği PDF dosyaları sunucu diskine yazılmadan, tamamen RAM üzerinde `io.BytesIO` bellek akışları (Byte Streams) olarak işlenir. Bu mimari yaklaşım, sunucu disk doluluğunu önler, I/O (Giriş/Çıkış) darboğazlarını engeller ve eşzamanlı çoklu kullanıcı senaryolarında yüksek performans sağlar.
* **Gelişmiş State ve Kimlik Yönetimi:** Streamlit'in yaşam döngüsüne uygun olarak tasarlanan güvenli yan panel (Sidebar), kullanıcının girdiğinde `os.environ` üzerinden çevre değişkenlerine enjekte edilen `GEMINI_API_KEY` yönetimini dinamik ve güvenli bir şekilde simüle eder. Key girilmediği durumlarda arayüz reaktif olarak yapay zeka modüllerini kilitler ve kullanıcıyı rehber mesajlarla yönlendirir.
* **Katmanlı Test Otomasyonu (High Coverage & Robustness):** Proje, yazılım test piramidinin tüm aşamalarını kapsar. Pytest kütüphanesi ve `pytest-cov` eklentisiyle kod kapsama oranı (Code Coverage) anlık olarak izlenir.
* **Kırılgan Olmayan (Robust) Kelime Analiz Motoru:** Yerel karakter eşleme bug'ları (Örn: Türkçe büyük "Ş" harfinin Unix/Windows sunucularında `.lower()` işleminde yarattığı kırılma) analiz edilmiş; test verileri "mont", "ceket" gibi evrensel token'larla standardize edilerek testlerin işletim sisteminden bağımsız, kararlı çalışması sağlanmıştır.
* **Lazy-Initialization ile AI Entegrasyonu:** Yapay zeka servis katmanı (`AIService`), Google Gemini 2.5 Flash API'sini nesne yönelimli bir yapıda kapsüller. API istemcisi (Client), sadece kullanıcı arayüzündeki butona tıkladığı anda (Lazy Initialization) ayağa kaldırılıp kaynak tüketimi optimize edilir.
* **Bulut Sunucu Uyumlu Dinamik Yol Yönetimi:** Streamlit Cloud gibi sunucularda yaşanan mutlak dosya yolu (`ImportError`) hataları, `sys.path` manipülasyonu ve paket içi `__init__.py` entegrasyonuyla kökten çözülmüştür. Proje hem lokalde (`localhost`) hem de bulutta sıfır konfigürasyonla çalışır.

---

## 🎨 Streamlit Kullanıcı Arayüzü ve Bileşen Mimarisi

Uygulama, karmaşık veri analizlerini son kullanıcıya en sade ve efektif şekilde sunmak amacıyla 4 dinamik sekmeye (Tabs) bölünmüş bir dashboard yapısıyla sunulur:

1. **🤖 Yapay Zeka Özeti (AI Executive Summary):** Yüklenen PDF'in tüm içeriğini Gemini 2.5 Flash modeline profesyonel bir prompt mühendisliği (Prompt Engineering) şablonuyla besler ve tek tuşla dökümanın kurumsal yönetici özetini çıkarır.
2. **🔍 Kelime İstatistikleri (Frekans Analizi):** `TextAnalyzer` motorundan dönen en sık geçen anahtar kelimeleri ve frekanslarını, Streamlit'in yerel `st.progress` (ilerleme çubukları) bileşenlerini kullanarak görsel bir grafik barda listeler.
3. **🔎 Akıllı Parser (Metin İçi Arama):** Kullanıcının döküman içinde arattığı hukuki terim, finansal veri veya özel kavramları cümle bazında tarar. Eşleşen tüm satırları yapısal `st.info` bloklarında dinamik indeks numaralarıyla kullanıcıya raporlar.
4. **📜 Ham Metin Verisi (OCR/Digitalization):** PDF'ten tamamen dijitalleştirilen saf metni `st.text_area` içinde listeler. Kullanıcının bu veriyi tek tıkla yerel bilgisayarına indirebilmesi için `st.download_button` entegrasyonuna sahiptir.

---

## 📁 Proje Yapısı ve Klasör Hiyerarşisi

```text
├── core/               # İş Mantığı (Business Logic) Paketi
│   ├── __init__.py     # Klasörün Python paketi (module) olarak tanınmasını sağlar
│   ├── ai_service.py   # Gemini AI Servis Katmanı (Özetleme, LLM Prompt Yönetimi)
│   └── pdf_engine.py   # PDFParser (Metin çıkarma) & TextAnalyzer (Arama, Frekans) Motorları
├── tests/              # Katmanlı Test Suitleri (Test Pyramid)
│   ├── test_unit.py        # En küçük kod bloklarının (Fonksiyonel bazda) birim testleri
│   ├── test_integration.py # PDFParser ve TextAnalyzer arasındaki entegrasyon testleri
│   ├── test_system.py      # Sistemin veri akışını ve uçtan uca girdi-çıktı doğruluğunu test eder
│   └── test_scenario.py    # Gerçek bir kullanıcının döküman yükleme ve arama senaryoları
├── requirements.txt    # Projenin kütüphane bağımlılıkları listesi
└── app.py              # Streamlit Web Kullanıcı Arayüzü & Sunum Katmanı
