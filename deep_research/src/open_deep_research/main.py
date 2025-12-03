import streamlit as st
import asyncio
from io import StringIO
import pandas as pd
import uuid

# deep_researcher.py dosyasından run_graph fonksiyonunu içeri aktar
from deep_researcher import run_graph

# Oturum başına benzersiz kullanıcı ID'si oluştur
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

# Arayüz Başlığı
st.set_page_config(page_title="Derin Araştırma Asistanı", page_icon="🔍")
st.title("🔎 Derin Araştırma Asistanı")
st.caption(f"Kullanıcı oturumu: {st.session_state.user_id}")

# === 🧠 Asenkron araştırma işlemi ===
async def async_process_research(input_text):
    try:
        result = await run_graph(input_text)

        final_report = result.get("final_report", "📄 Rapor bulunamadı.")
        raw_notes = result.get("raw_notes", [])

        st.subheader("📋 Nihai Rapor")
        st.success(final_report)

        st.subheader("🗒️ Ham Notlar")
        for note in raw_notes:
            st.markdown(f"- {note}")

        # Pandas tablosu olarak göster
        if raw_notes:
            df = pd.DataFrame({"Notlar": raw_notes})
            st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Hata oluştu: {e}")

# === 📥 Text Input Form ===
with st.form("text_form"):
    input_text = st.text_area("Araştırmak istediğiniz konuyu yazın:", "İstanbul'daki forwarding firmalarını bul")
    submit_btn = st.form_submit_button("🚀 Araştırmayı Başlat")

    if submit_btn:
        with st.spinner("🔍 Araştırma yapılıyor..."):
            asyncio.run(async_process_research(input_text))

# === 📤 Dosya Yükleme ===
st.markdown("---")
st.header("📄 Dosya ile Araştırma")

upload_file = st.file_uploader("Excel veya CSV dosyanızı yükleyin:", type=["csv", "xlsx"])

if upload_file:
    try:
        if upload_file.name.endswith(".csv"):
            df_file = pd.read_csv(upload_file)
        else:
            df_file = pd.read_excel(upload_file)

        st.success("✅ Dosya başarıyla yüklendi!")
        st.dataframe(df_file, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Dosya okuma hatası: {e}")
