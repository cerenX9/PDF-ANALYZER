import re
from collections import Counter
from io import BytesIO
from typing import Dict, List, Any
from pypdf import PdfReader

class PDFParser:
    """PDF dosyalarından ham veri okuma (extraction) işlemlerini yöneten sınıf."""
    
    def __init__(self, file_stream: BytesIO):
        self.file_stream = file_stream
        self._reader = None
        
    @property
    def reader(self) -> PdfReader:
        if self._reader is None:
            self._reader = PdfReader(self.file_stream)
        return self._reader

    def get_metadata(self) -> Dict[str, Any]:
        """PDF meta verilerini (Yazar, Sayfa sayısı vb.) güvenli bir şekilde döner."""
        meta = self.reader.metadata
        return {
            "pages": len(self.reader.pages),
            "author": meta.author if meta and meta.author else "Bilinmiyor",
            "creator": meta.creator if meta and meta.creator else "Bilinmiyor",
            "title": meta.title if meta and meta.title else "Başlıksız"
        }

    def extract_all_text(self) -> str:
        """PDF içindeki tüm sayfaların metinlerini birleştirerek string olarak döner."""
        full_text = []
        for page in self.reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
        return "\n".join(full_text)


class TextAnalyzer:
    """Extract edilmiş metinler üzerinde gelişmiş analiz ve parse işlemleri yapan sınıf."""
    
    def __init__(self, text: str):
        self.text = text

    def get_word_count(self) -> int:
        """Metindeki toplam kelime sayısını hesaplar."""
        if not self.text.strip():
            return 0
        return len(self.text.split())

    def get_most_common_words(self, top_n: int = 5) -> List[tuple]:
        """Metinde en çok tekrar eden kelimeleri temizleyerek (Stop-Words hariç) döner."""
        words = re.findall(r'\b[a-zA-ZğüşıöçĞÜŞİÖÇ]{3,}\b', self.text.lower())
        
        # Filtrelenecek anlamsız kelimeler (Veri Temizleme)
        stop_words = {
            "ve", "veya", "ile", "için", "bir", "bu", "şu", "o", "da", "de", "ise",
            "the", "and", "for", "with", "that", "this", "from", "are", "was"
        }
        filtered_words = [w for w in words if w not in stop_words]
        return Counter(filtered_words).most_common(top_n)

    def search_keyword(self, keyword: str) -> List[str]:
        """Metin içinde aranan kelimenin geçtiği cümleleri ayıklar."""
        if not keyword:
            return []
        sentences = re.split(r'(?<=[.!?])\s+', self.text)
        matches = [s.strip() for s in sentences if keyword.lower() in s.lower()]
        return matches