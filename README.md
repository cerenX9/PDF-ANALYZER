# 📄 AI-Powered PDF Analyzer & Parser

Modern Nesne Yönelimli Programlama (OOP) prensipleriyle tasarlanmış, tam kapsamlı otomatik test otomasyonuna sahip ve Google Gemini LLM API entegrasyonlu kurumsal bir PDF analiz ve dijitalleştirme sistemi.

## 🚀 Özellikler
- **OOP Mimari:** İş mantığı (`core`) ve arayüz katmanı (`app.py`) tamamen birbirinden bağımsızdır.
- **AI Özetleme:** Google Gemini API ile entegre uçtan uca doküman analizi.
- **Test Otomasyonu (High Coverage):** Pytest ile Unit, Integration, System ve Scenario test senaryoları.
- **Akıllı Parser:** Metin temizleme (Stop-words filtresi) ve döküman içi akıllı cümle arama motoru.

## 📁 Proje Yapısı
```text
├── core/               # İş Mantığı (Business Logic) Paketi
│   ├── ai_service.py   # Gemini AI Servis Katmanı
│   └── pdf_engine.py   # PDFParser & TextAnalyzer Motoru
├── tests/              # Katmanlı Test Suitleri
│   ├── test_unit.py        # Birim testleri
│   ├── test_integration.py # Entegrasyon testleri
│   ├── test_system.py      # Sistem testleri
│   └── test_scenario.py    # Gerçek kullanıcı senaryo testleri
└── app.py              # Streamlit Web Kullanıcı Arayüzü