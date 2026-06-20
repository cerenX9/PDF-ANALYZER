import pytest
from core.pdf_engine import PDFParser, TextAnalyzer

def test_pdf_to_analyzer_data_flow():
    """Bileşenlerin entegrasyon zincirini ve veri akışını doğrular."""
    raw_text = "Python harika bir dildir. Python ile veri analizi çok kolaydır."
    analyzer = TextAnalyzer(raw_text)
    
    assert analyzer.get_word_count() == 10
    assert analyzer.get_most_common_words(top_n=1)[0] == ("python", 2)