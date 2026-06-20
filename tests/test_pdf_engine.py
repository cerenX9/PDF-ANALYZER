import pytest
from io import BytesIO
from pypdf import PdfWriter
from core.pdf_engine import PDFParser, TextAnalyzer

@pytest.fixture
def sample_pdf_stream():
    """Bellek üzerinde (In-Memory) sahte ve temiz bir test PDF belgesi üretir."""
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.add_metadata({
        "/Author": "Ceren",
        "/Title": "Mühendislik Testi"
    })
    stream = BytesIO()
    writer.write(stream)
    stream.seek(0)
    return stream

def test_pdf_parser_metadata(sample_pdf_stream):
    parser = PDFParser(sample_pdf_stream)
    metadata = parser.get_metadata()
    assert metadata["pages"] == 1
    assert metadata["author"] == "Ceren"

def test_text_analyzer_word_count():
    analyzer = TextAnalyzer("Mühendislik testleri kod kalitesini doğrudan artırır.")
    assert analyzer.get_word_count() == 6
    
    empty_analyzer = TextAnalyzer("   ")
    assert empty_analyzer.get_word_count() == 0

def test_text_analyzer_common_words():
    analyzer = TextAnalyzer("Python veri veri Python kod Python")
    common = analyzer.get_most_common_words(top_n=2)
    assert common[0] == ("python", 3)

def test_text_analyzer_search_keyword():
    analyzer = TextAnalyzer("Git sürüm kontrolüdür. Pytest test aracıdır.")
    results = analyzer.search_keyword("Pytest")
    assert len(results) == 1
    assert "Pytest test aracıdır." in results[0]