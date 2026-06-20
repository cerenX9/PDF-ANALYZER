import os
import streamlit as st
from io import BytesIO
from core.pdf_engine import PDFParser, TextAnalyzer
from core.ai_service import AIService

st.set_page_config(page_title="AI PDF Analyzer", page_icon="📄", layout="wide")

# --- SOL PANELDE API KEY GİRİŞİ ---
with st.sidebar:
    st.header("🔑 Yapay Zeka Ayarları")
    api_key_input = st.text_input("Gemini API Key Giriniz:", type="password", help="Google AI Studio'dan aldığınız ücretsiz API anahtarı.")
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        st.success("API Anahtarı Tanımlandı!")

st.markdown("<h1 style='text-align: center; color: #0284C7;'>📄 AI-POWERED PDF ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B;'>OOP Mimarili ve Yapay Zeka Destekli PDF Analiz Sistemi</p>", unsafe_allow_html=True)
st.divider()

uploaded_file = st.file_uploader("Analiz edilecek PDF dosyasını seçin", type=["pdf"])

if uploaded_file is not None:
    file_stream = BytesIO(uploaded_file.read())
    
    parser = PDFParser(file_stream)
    metadata = parser.get_metadata()
    extracted_text = parser.extract_all_text()
    analyzer = TextAnalyzer(extracted_text)
    
    # Metrik Raporları
    st.markdown("### 📊 Genel Analiz Raporu")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="📄 Sayfa Sayısı", value=f"{metadata['pages']} Sayfa")
    with m_col2:
        st.metric(label="🔤 Kelime Sayısı", value=f"{analyzer.get_word_count()} Kelime")
    with m_col3:
        st.metric(label="✍️ Belge Müellifi (Author)", value=metadata['author'])
        
    st.divider()
    
    # GÜNCELLENEN SEKMELİ YAPI (AI EKLENDİ)
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Yapay Zeka Özeti", "🔍 Kelime İstatistikleri", "🔎 Akıllı Parser (Arama)", "📜 Ham Metin"])
    
    with tab1:
        st.subheader("🧠 Gemini AI Yönetici Özeti")
        if not os.getenv("GEMINI_API_KEY"):
            st.warning("⚠️ Sol panelden 'Gemini API Key' girerek yapay zeka özetleme özelliğini aktif edebilirsiniz. (Google AI Studio'dan ücretsiz alabilirsiniz)")
        else:
            if st.button("✨ Yapay Zeka ile Özeti Çıkar", type="primary"):
                with st.spinner("Gemini dökümanı inceliyor ve özetliyor..."):
                    ai_service = AIService()
                    summary = ai_service.summarize_text(extracted_text)
                    st.markdown("### 📋 Yönetici Özeti")
                    st.info(summary)
            
    with tab2:
        st.subheader("🔝 En Sık Geçen Kelimeler")
        common_words = analyzer.get_most_common_words(top_n=5)
        if common_words:
            max_freq = common_words[0][1]
            for word, count in common_words:
                col_w, col_p = st.columns([1, 4])
                with col_w: st.markdown(f"**{word}**")
                with col_p: st.progress(count / max_freq, text=f"{count} adet")
        else: st.info("İstatistik çıkarılacak metin bulunamadı.")
            
    with tab3:
        st.subheader("🎯 Cümle İçi Arama Motoru")
        query = st.text_input("Döküman içinde aratmak istediğiniz kavram:")
        if query:
            results = analyzer.search_keyword(query)
            if results:
                st.success(f"**{len(results)}** eşleşen cümle listelendi:")
                for idx, sent in enumerate(results, 1): st.info(f"**{idx}.** ... {sent} ...")
            else: st.warning("Eşleşme bulunamadı.")
                
    with tab4:
        st.subheader("📄 Dijitalleştirilen Metin Verisi")
        if extracted_text.strip():
            st.text_area(label="Tüm İçerik", value=extracted_text, height=300)
            st.download_button(label="📥 TXT Olarak İndir", data=extracted_text, file_name="extracted.txt")
        else: st.error("Okunabilir metin bulunamadı.")
else:
    st.info("💡 Başlamak için lütfen yukarıdaki alana bir PDF belgesi yükleyin.")