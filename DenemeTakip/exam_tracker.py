# exam_tracker.py
import streamlit as st
import pandas as pd
from datetime import date
import time

CSV_PATHS = {
"TYT": "records/tyt_results.csv",
"AYT": "records/ayt_results.csv",
"Tek Ders": "records/isolate_results.csv"
}

# CSV yükle
def load_data(sinav_turu):
    try:
        return pd.read_csv(CSV_PATHS[sinav_turu])
    except FileNotFoundError:
        return pd.DataFrame()

# CSV kaydet
def save_data(new_entry, sinav_turu):
    df = load_data(sinav_turu)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(CSV_PATHS[sinav_turu], index=False)

# Net hesapla
def net_hesapla(d, y, b):
    return d - (y * 0.25)



# TYT dersleri
TYT_DERSLER = {
    "Türkçe": 40,
    "TYT Matematik": 40,
    "Sosyal Bilgiler": 20,
    "TYT Fizik": 7,
    "TYT Kimya": 7,
    "TYT Biyoloji": 6
}

# AYT dersleri
AYT_DERSLER = {
    "AYT Matematik": 40,
    "AYT Fizik": 14,
    "AYT Kimya": 13,
    "AYT Biyoloji": 13
}



# Deneme formu
def deneme_formu(dersler, sinav_turu):
    # Reset inputs if flag is set
    if st.session_state.get("reset_inputs", False):
        for key in st.session_state.keys():
            if any(sub in key for sub in ["_dogru", "_yanlis", "deneme_adi", "izole_ad", "ders", "tarih", "izole_tarih"]):
                value = st.session_state[key]
                if isinstance(value, str):
                    st.session_state[key] = ""
                elif isinstance(value, (int, float)):
                    st.session_state[key] = 0
                elif isinstance(value, date):
                    st.session_state[key] = date.today()
        st.session_state["reset_inputs"] = False  # Unset the flag

    st.subheader(f"📝 {sinav_turu} Denemesi Girişi")
    deneme_adi = st.text_input("Deneme Adı", key=f"{sinav_turu}_deneme_adi")
    tarih = st.date_input("Tarih", value=date.today(), key="tarih")

    veri = {
        "Sınav Türü": sinav_turu,
        "Deneme Adı": deneme_adi,
        "Tarih": tarih.strftime("%d-%m-%Y")
    }

    toplam_dogru = toplam_yanlis = toplam_bos = toplam_net = 0

    for ders, soru_sayisi in dersler.items():
        st.markdown(f"**{ders}** ({soru_sayisi} soru)")
        d_key = f"{sinav_turu}_{ders}_dogru"
        y_key = f"{sinav_turu}_{ders}_yanlis"
        dogru = st.number_input(f"{ders} Doğru", 0, soru_sayisi, key=d_key)
        yanlis = st.number_input(f"{ders} Yanlış", 0, int(soru_sayisi-dogru), key=y_key)
        bos = soru_sayisi - dogru - yanlis
        net = net_hesapla(dogru, yanlis, bos)
        st.write(f"Boş: {bos} | Net: {net:.2f}")

        veri[f"{ders} Doğru"] = dogru
        veri[f"{ders} Yanlış"] = yanlis
        veri[f"{ders} Boş"] = bos
        veri[f"{ders} Net"] = round(net, 2)

        toplam_dogru += dogru
        toplam_yanlis += yanlis
        toplam_bos += bos
        toplam_net += net

    veri["Toplam Doğru"] = toplam_dogru
    veri["Toplam Yanlış"] = toplam_yanlis
    veri["Toplam Boş"] = toplam_bos
    veri["Toplam Net"] = round(toplam_net, 2)

    if st.button("Kaydet", key=f"kaydet_{sinav_turu}"):
        save_data(veri, sinav_turu)
        st.success(f"✅ {sinav_turu} denemesi başarıyla kaydedildi!")
        time.sleep(0.5)
        st.info(f"⌛ Kayıtlar güncelleniyor, lütfen bekleyin...")
        time.sleep(1)
        st.session_state["reset_inputs"] = True  # Set reset flag
        st.rerun()
        


# Tek ders formu
def izole_ders_girisi():
        # Reset inputs if flag is set
    if st.session_state.get("reset_inputs", False):
        for key in st.session_state.keys():
            if any(sub in key for sub in ["_dogru", "_yanlis", "deneme_adi", "izole_ad", "ders", "tarih", "izole_tarih"]):
                value = st.session_state[key]
                if isinstance(value, str):
                    st.session_state[key] = ""
                elif isinstance(value, (int, float)):
                    st.session_state[key] = 0
                elif isinstance(value, date):
                    st.session_state[key] = date.today()
        st.session_state["reset_inputs"] = False  # Unset the flag
        
    st.subheader("🔹 Tek Ders Denemesi")
    deneme_adi = st.text_input("Deneme Adı", key="izole_ad")
    tarih = st.date_input("Tarih", value=date.today(), key="izole_tarih")
    ders = st.text_input("Ders Adı", key="ders").lower()
    ilkharf = ders[:1]
    kelime = ders[1:] 
    ders = ilkharf.upper() + kelime
    soru_sayisi = st.number_input("Toplam Soru Sayısı", 1, 100)
    dogru = st.number_input("Doğru Sayısı", 0, int(soru_sayisi))
    yanlis = st.number_input("Yanlış Sayısı", 0, int(soru_sayisi - dogru))
    bos = soru_sayisi - dogru - yanlis
    net = net_hesapla(dogru, yanlis, bos)
    st.write(f"Boş: {bos} | Net: {net:.2f}")

    if st.button("Kaydet", key="kaydet_tek"):
        veri = {
            "Sınav Türü": f"{ders}",
            "Deneme Adı": deneme_adi,
            "Tarih": tarih.strftime("%d-%m-%Y"),
            "Doğru": dogru,
            "Yanlış": yanlis,
            "Boş": bos,
            "Net": round(net, 2),
            "Toplam Doğru": dogru,
            "Toplam Yanlış": yanlis,
            "Toplam Boş": bos,
            "Toplam Net": round(net, 2)
        }
        save_data(veri, "Tek Ders")
        st.success(f"✅ {ders} denemesi başarıyla kaydedildi!")
        time.sleep(0.5)
        st.info(f"⌛ Kayıtlar güncelleniyor, lütfen bekleyin...")
        time.sleep(1)
        st.session_state["reset_inputs"] = True  # Set reset flag
        st.rerun()



# Son denemeler
def son_kayitlar():
    st.subheader("📊 En Son Kaydedilen Denemeler")
    sinav_turu_secim = st.selectbox("Görmek İstediğiniz Sınav Türü",["TYT", "AYT", "Tek Ders"])
    df = load_data(sinav_turu_secim)
    if df.empty:
        st.info(f"Daha önce hiç {sinav_turu_secim} denemesi kaydedilmedi.")
    else:
        st.dataframe(df)
        # Kullanıcıya kayıt seçtir
        df_display = df.copy()
        df_display["Görünen"] = f"{df_display["Deneme Adı"]} | {df_display["Tarih"]}"
        secilecek = df_display["Görünen"].tolist()

        if secilecek:
            secilen_kayit = st.selectbox("Silmek istediğiniz kaydı seçin", secilecek, key="delete_select")

            if st.button("Kaydı Sil", key="delete_button"):
                # Seçilen kaydın index'ini bul
                index_to_delete = df_display[df_display["Görünen"] == secilen_kayit].index[0]
                df.drop(index=index_to_delete, inplace=True)
                df.reset_index(drop=True, inplace=True)
                df.to_csv(CSV_PATHS[sinav_turu_secim], index=False)
                st.success(f"✅ Deneme başarıyla silindi.")
                time.sleep(0.5)
                st.info(f"⌛ Kayıtlar güncelleniyor, lütfen bekleyin...")
                time.sleep(1)
                st.rerun()
        else:
            st.info("Silinecek kayıt bulunamadı.")




# Menü değişim kontrolü
def menu_change():
    if "last_menu" not in st.session_state:
        st.session_state.last_menu = ""
    if st.session_state.last_menu != st.session_state.menu_secim:
        st.session_state.last_menu = st.session_state.menu_secim



# Arayüz
def main():
    st.set_page_config(page_title="Deneme Takibi", layout="centered")
    st.title("📘 Deneme Takip Uygulaması")

    st.sidebar.title("📚 Menü")
    secim = st.sidebar.radio("İşlem Seç", [
        "TYT Deneme Sonucu Gir",
        "AYT Deneme Sonucu Gir",
        "Tek Ders Deneme Sonucu Gir",
        "Sonuçları Gör"
    ], key="menu_secim")

    menu_change()

    if secim == "TYT Deneme Sonucu Gir":
        deneme_formu(TYT_DERSLER, "TYT")
    elif secim == "AYT Deneme Sonucu Gir":
        deneme_formu(AYT_DERSLER, "AYT")
    elif secim == "Tek Ders Deneme Sonucu Gir":
        izole_ders_girisi()
    elif secim == "Sonuçları Gör":
        son_kayitlar()

if __name__ == "__main__":
    main()