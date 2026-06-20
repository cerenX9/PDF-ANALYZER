import pytest
from core.pdf_engine import TextAnalyzer

# ==============================================================================
# SENARYO 1: "AVUKAT CEREN" - BAŞARILI SÖZLEŞME ANALİZİ VE ARŞİVLEME HİKAYESİ
# ==============================================================================
def test_scenario_successful_contract_analysis_by_lawyer():
    """
    Kullanıcı Hikayesi: Avukat Ceren, sisteme 3 maddelik bir gizlilik sözleşmesi metni yükler.
    Sistemin toplam kelime sayısını doğru hesapladığını, en kritik hukuki terimleri listelediğini
    ve 'ceza' kelimesini arattığında ilgili yaptırım maddesini başarıyla bulduğunu doğrulamak ister.
    """
    # 1. Ceren sözleşmeyi sisteme yükler (Arka planda text extraction yapıldığını varsayıyoruz)
    uploaded_contract = (
        "Madde 1: Bu bir Gizlilik ve Veri Güvenliği Sözleşmesidir. "
        "Madde 2: Taraflar ticari sırları üçüncü şahıslarla paylaşamaz. "
        "Madde 3: İhlal durumunda 50000 USD ceza şartı uygulanacaktır."
    )
    
    # 2. Sistem Ceren'in belgesini analiz motoruna alır
    analyzer = TextAnalyzer(uploaded_contract)
    
    # 3. DOĞRULAMA: Ceren arayüzde genel metrikleri görür
    assert analyzer.get_word_count() == 25  # Toplam kelime tam olmalı
    
    # 4. DOĞRULAMA: Ceren en çok tekrar eden kelimeleri inceler
    common_words = [word for word, count in analyzer.get_most_common_words(top_n=5)]
    # 've', 'bir' gibi bağlaçlar elenmiş olmalı, kritik kelimeler kalmalı
    assert "gizlilik" in common_words or "sözleşmesidir" in common_words
    assert "ve" not in common_words  # Stop-words veri temizleme filtresi çalışmalı
    
    # 5. DOĞRULAMA: Ceren 'ceza' kelimesini aratarak yaptırım maddesini bulur
    search_results = analyzer.search_keyword("ceza")
    assert len(search_results) == 1
    assert "Madde 3: İhlal durumunda 50000 USD ceza şartı uygulanacaktır." in search_results[0]


# ==============================================================================
# SENARYO 2: "MUHASEBECİ AHMET" - BOZUK/BOŞ FATURA YÜKLEME VE HATA YÖNETİMİ HİKAYESİ
# ==============================================================================
def test_scenario_empty_invoice_error_handling_by_accountant():
    """
    Kullanıcı Hikayesi: Muhasebeci Ahmet, yanlışlıkla içi tamamen boş olan veya 
    sadece tarayıcı lekelerinden (boşluklardan) oluşan bozuk bir fatura PDF'i yükler.
    Sistemin hata fırlatıp çökmediğini (Crash), Ahmet'e '0 Kelime' raporu döndüğünü 
    ve arama yaptığında sistemi kilitlemeden boş sonuç verdiğini doğrulamak ister.
    """
    # 1. Ahmet bozuk/boş faturayı yükler
    corrupted_invoice_text = "   \n   \t   "
    
    # 2. Sistem Ahmet'in belgesini analiz motoruna alır
    analyzer = TextAnalyzer(corrupted_invoice_text)
    
    # 3. DOĞRULAMA: Sistem çökmez ve Ahmet'e 0 kelime raporlar (Zarif Hata Yönetimi)
    assert analyzer.get_word_count() == 0
    
    # 4. DOĞRULAMA: Kelime istatistikleri boş liste döner, arayüz Ahmet'i uyarabilir
    assert analyzer.get_most_common_words() == []
    
    # 5. DOĞRULAMA: Ahmet panikle arama motoruna 'KDV' yazsa bile sistem hata vermez, boş döner
    search_results = analyzer.search_keyword("KDV")
    assert search_results == []