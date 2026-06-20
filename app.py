import os
import sys

# 1. KRİTİK ADIM: Bulut sunucularda (Streamlit Cloud) klasör yollarının
# karışmaması için projenin kök dizinini Python arama yollarının en başına ekliyoruz.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 2. ADIM: Artık kendi yazdığımız modülleri ve harici kütüphaneleri 
# güvenle import edebiliriz.
from io import BytesIO
import streamlit as st
from core.pdf_engine import PDFParser, TextAnalyzer
from core.ai_service import AIService

# --- STREAMLIT SAYFA AYARLARI ---
st.set_page_config(
    page_title="AI PDF Analyzer", 
    page_icon="📄", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown("### 🔑 Yapay Zeka Yapılandırması")
    st.markdown(
        "Bu uygulama özetleme işlemleri için **Google Gemini 2.5 Flash** modelini kullanır. "
        "Ücretsiz API anahtarınızı [Google AI Studio](https://aistudio.google.com/) üzerinden alabilirsiniz."
    )
    api_key_input = st.text_input(
        "Gemini API Key Giriniz:", 
        type="password", 
        placeholder="AIzaSy..."
    )
    
    if api_key_input:
        os.environ["GEMINI_API_KEY"] = api_key_input
        st.success("✅ API Anahtarı Çevre Değişkenlerine Eklendi!")
    else:
        st.info("💡 Yapay zeka özelliğini kullanmak için lütfen API anahtarı girin.")

# --- ANA SAYFA BAŞLIKLARI ---
st.markdown("<h1 style='text-align: center; color: #0284C7;'>📄 AI-POWERED PDF ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B;'>OOP Mimari ve Yapay Zeka Destekli Belge Analiz Sistemi</p>", unsafe_allow_html=True)
st.divider()

# --- DOSYA YÜKLEME ALANI ---
uploaded_file = st.file_uploader(
    "Analiz edilecek PDF dosyasını sürükleyip bırakın veya seçin", 
    type=["pdf"]
)

if uploaded_file is not None:
    # PDF dosyasını belleğe alıp akışa (stream) çeviriyoruz
    file_stream = BytesIO(uploaded_file.read())
    
    # OOP Motorlarımızı çalıştırıyoruz
    with st.spinner("PDF ayrıştırılıyor ve metinler dijitalleştiriliyor..."):
        parser = PDFParser(file_stream)
        metadata = parser.get_metadata()
        extracted_text = parser.extract_all_text()
        analyzer = TextAnalyzer(extracted_text)
    
    # 📊 ÜST METRİK RAPORLARI
    st.markdown("### 📊 Genel Analiz Raporu")
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric(label="📄 Sayfa Sayısı", value=f"{metadata['pages']} Sayfa")
    with m_col2:
        st.metric(label="🔤 Toplam Kelime Sayısı", value=f"{analyzer.get_word_count()} Kelime")
    with m_col3:
        st.metric(label="✍️ Belge Müellifi (Author)", value=metadata['author'])
        
    st.divider()
    
    # 🗂️ SEKMELİ KULLANICI ARAYÜZÜ (TABS)
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 Yapay Zeka Özeti", 
        "🔍 Kelime İstatistikleri", 
        "🔎 Akıllı Parser (Arama)", 
        "📜 Ham Metin Verisi"
    ])
    
    # TAB 1: YAPAY ZEKA ÖZETİ
    with tab1:
        st.subheader("🧠 Gemini AI Yönetici Özeti")
        if not os.getenv("GEMINI_API_KEY"):
            st.warning(
                "⚠️ Sol panelden 'Gemini API Key' girerek yapay zeka özetleme özelliğini aktif edebilirsiniz. "
                "API anahtarı girmediğiniz sürece bu modül çalışmayacaktır."
            )
        else:
            if st.button("✨ Yapay Zeka ile Özet Üret", type="primary"):
                with st.spinner("Gemini doküman içeriğini okuyor ve kurumsal özet çıkarıyor..."):
                    try:
                        ai_service = AIService()
                        summary = ai_service.summarize_text(extracted_text)
                        st.markdown("#### 📋 Üretilen Yönetici Özeti")
                        st.info(summary)
                    except Exception as e:
                        st.error(f"Yapay zeka servisi çalıştırılırken bir hata oluştu: {str(e)}")
            
    # TAB 2: KELİME İSTATİSTİKLERİ
    with tab2:
        st.subheader("🔝 En Sık Geçen Kritik Kelimeler")
        common_words = analyzer.get_most_common_words(top_n=5)
        if common_words:
            max_freq = common_words[0][1]
            for word, count in common_words:
                col_w, col_p = st.columns([1, 4])
                with col_w: 
                    st.markdown(f"**{word}**")
                with col_p: 
                    st.progress(count / max_freq, text=f"{count} adet listelendi")
        else: 
            st.info("İstatistik ve frekans çıkarılacak anlamlı bir metin bulunamadı.")
            
    # TAB 3: CÜMLE İÇİ ARAMA MOTORU
    with tab3:
        st.subheader("🎯 Belge İçi Akıllı Cümle Arama")
        query = st.text_input(
            "Doküman içinde aratmak istediğiniz kavram veya kelime öbeği:",
            placeholder="Örn: Gizlilik, Cezai Şart, İptal..."
        )
        if query:
            results = analyzer.search_keyword(query)
            if results:
                st.success(f"🔍 Belge içinde **{len(results)}** adet eşleşen cümle bulundu:")
                for idx, sent in enumerate(results, 1): 
                    st.info(f"**{idx}.** ... {sent.strip()} ...")
            else: 
                st.warning("Aranan kelime ile eşleşen herhangi bir cümle veya paragraf bulunamadı.")
                
    # TAB 4: HAM METİN VERİSİ
    with tab4:
        st.subheader("📄 Dijitalleştirilen Ham Metin İçeriği")
        if extracted_text.strip():
            st.text_area(label="OCR / Dijital Metin Çıktısı", value=extracted_text, height=350)
            st.download_button(
                label="📥 Metni (.txt) Olarak İndir", 
                data=extracted_text, 
                file_name="dijitallestirilen_metin.txt",
                mime="text/plain"
            )
        else: 
            st.error("Bu PDF dosyasından okunabilir dijital bir metin verisi çıkarılamadı.")
else:
    st.info("💡 Sistemin analize başlayabilmesi için lütfen yukarıdaki alana geçerli bir PDF belgesi yükleyin.")