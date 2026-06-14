import streamlit as st
import mysql.connector
import pandas as pd
import time

# Konfigurasi Page
st.set_page_config(page_title="Smart Street Lighting", layout="wide")

st.title("💡 Smart Street Lighting Dashboard")

# Gunakan placeholder untuk tempat data yang akan di-update terus menerus
placeholder = st.empty()

# Fungsi koneksi ke Clever Cloud (Pastikan kredensial sudah diisi dengan benar!)
def get_data():
    try:
        conn = mysql.connector.connect(
            host=st.secrets["DB_HOST"],
            user=st.secrets["DB_USER"],
            passwd=st.secrets["DB_PASS"],
            database=st.secrets["DB_NAME"],
            port=3306
        )
        query = "SELECT id_tiang, nilai_cahaya, status_lampu, waktu FROM tbl_monitoring ORDER BY waktu DESC LIMIT 20"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except:
        return pd.DataFrame()

# Loop untuk update otomatis setiap 2 detik
while True:
    df = get_data()
    
    with placeholder.container():
        if not df.empty:
            # Tampilan Metric
            terbaru = df.iloc[0]
            col1, col2, col3 = st.columns(3)
            col1.metric("Tiang Aktif", f"Tiang {terbaru['id_tiang']}")
            col2.metric("Intensitas LDR", int(terbaru['nilai_cahaya']))
            col3.metric("Status Lampu", terbaru['status_lampu'])
            
            # Tampilan Grafik & Tabel
            st.line_chart(df.sort_values('waktu').set_index('waktu')['nilai_cahaya'])
            st.dataframe(df)
        else:
            st.warning("Menunggu data masuk dari alat...")
            
    # Tunggu 2 detik sebelum ambil data lagi (Auto-update tanpa restart)
    time.sleep(2)
