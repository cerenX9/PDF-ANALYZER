import pytest
from core.pdf_engine import TextAnalyzer

def test_end_to_end_pdf_intelligence_system():
    """Tüm sistemin yaşam döngüsünü (E2E) test eder."""
    contract_text = (
        "Bu bir gizlilik sözleşmesidir. "
        "Taraflar verileri korumakla yükümlüdür. "
        "İhlal durumunda Ankara mahkemeleri yetkilidir."
    )
    
    system_analyzer = TextAnalyzer(contract_text)
    
    # 1. Metrik raporlama kontrolü
    assert system_analyzer.get_word_count() > 10
    
    # 2. Kelime frekansı kontrolü
    assert len(system_analyzer.get_most_common_words(top_n=3)) > 0
    
    # 3. Parser arama motoru kontrolü
    search_results = system_analyzer.search_keyword("Ankara")
    assert len(search_results) == 1
    assert "Ankara mahkemeleri yetkilidir" in search_results[0]