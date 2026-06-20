import pytest
from io import BytesIO
from pypdf import PdfWriter
from core.pdf_engine import PDFParser, TextAnalyzer

@pytest.fixture
def complete_pdf_stream():
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    writer.add_blank_page(width=200, height=200)
    writer.add_metadata({
        "/Author": "Ceren",
        "/Title": "Yapay Zeka Projesi Raporu",
        "/Creator": "VS Code Enterprise"
    })
    stream = BytesIO()
    writer.write(stream)
    stream.seek(0)
    return stream

@pytest.fixture
def empty_pdf_stream():
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    stream = BytesIO()
    writer.write(stream)
    stream.seek(0)
    return stream

def test_pdf_parser_metadata_filled(complete_pdf_stream):
    parser = PDFParser(complete_pdf_stream)
    metadata = parser.get_metadata()
    assert metadata["pages"] == 2
    assert metadata["author"] == "Ceren"
    assert metadata["title"] == "Yapay Zeka Projesi Raporu"

def test_pdf_parser_metadata_empty(empty_pdf_stream):
    parser = PDFParser(empty_pdf_stream)
    metadata = parser.get_metadata()
    assert metadata["pages"] == 1
    assert metadata["author"] == "Bilinmiyor"
    assert metadata["title"] == "Başlıksız"

def test_text_analyzer_edge_cases():
    analyzer_empty = TextAnalyzer("   ")
    assert analyzer_empty.get_word_count() == 0
    assert analyzer_empty.get_most_common_words() == []
    assert analyzer_empty.search_keyword("") == []
    
    analyzer_stop = TextAnalyzer("ve veya ile için bir bu")
    assert analyzer_stop.get_word_count() == 6
    assert analyzer_stop.get_most_common_words() == []

def test_text_analyzer_turkish_characters():
    """Metin analiz motorunun kelime frekanslarını doğru saydığını test eder."""
    text = "mont mont ceket ceket kaban kaban"
    analyzer = TextAnalyzer(text)
    common = analyzer.get_most_common_words(top_n=3)
    
    word_dict = dict(common)
    assert word_dict["mont"] == 2
    assert word_dict["ceket"] == 2
    assert word_dict["kaban"] == 2