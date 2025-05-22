import streamlit as st
import numpy as np
import agregator as ag
import pandas as pd 
import embeding as em 
# --- Streamlit UI ---
st.set_page_config(page_title="Graph & Vector Database Integration", layout="wide")

# Fungsi untuk menampilkan halaman pertama: Mencari orang/artikel
def page_1():
    st.subheader("Cari Nama Orang/Artikel")
    
    # Input pencarian nama orang atau artikel
    query = st.text_input("Masukkan nama orang atau artikel:")
    
    if query:
        # Query untuk mencari nama orang/artikel di Graph Database
        graph_query = f"""
            MATCH (p:User)-[r]->(a:Article)
            WHERE p.name CONTAINS '{query}'
            RETURN p.name AS person_name, 
                a.id_berita AS article_title, 
                a.kategori AS article_kategori, 
                type(r) AS relationship_type
        """
        
        # Fetch data from the Graph Database
        try:
            graph_data = ag.fetch_graph_data(graph_query)  # Assuming ag.fetch_graph_data is your method to fetch the data
            if not graph_data:
                st.write("Tidak ada hasil yang ditemukan.")
            else:
                # Convert Graph Data to a structured format
                graph_df = []
                for record in graph_data:
                    graph_df.append({
                        "Person": record["person_name"],
                        "Article": record["article_title"],
                        "Content": record["article_kategori"],
                        "Relationship": record["relationship_type"]
                    })
                
                # Convert to Pandas DataFrame for better visualization
                graph_df = pd.DataFrame(graph_df)
                
                # Display the result
                st.write("Hasil Pencarian:")
                st.dataframe(graph_df)

                # Optional: Allow the user to filter or interact further with the displayed results
                with st.expander("View Article Content"):
                    st.write(graph_df["Content"].to_list())
                    
        except Exception as e:
            st.error(f"Terjadi kesalahan saat mengambil data: {e}")
def page_2():
    st.subheader("Cari Artikel dengan Topik Sama")
    
    query_text = st.text_input("Masukkan topik atau kata kunci:")
    
    if query_text:
        query_vector = em.generate_embedding(query_text)
        results = ag.search_vector_db(query_vector)
        results_list = [{"Artikel ID": result.id, "Skor": result.score, "Payload": result.payload} for result in results]
        if results_list:
            st.write("Artikel dengan topik yang relevan:")
            for idx, artikel in enumerate(results_list):

                title = artikel["Payload"].get("judul", f"Artikel {idx+1}")
                # Buat button per artikel dengan key unik
                if st.button(title, key=f"artikel_btn_{idx} : {title}"):
                    # Simpan ID artikel yang dipilih di session_state
                    st.session_state["selected_article_id"] = artikel["Artikel ID"]
                    st.session_state["payload"] = artikel["Payload"]
                    # Ubah halaman aktif ke page_3
                    st.session_state["page"] = "page_3"
                    # Panggil page_3 langsung
                    page_3()
                    # Stop eksekusi supaya tidak lanjut render page_2
                    return
        else:
            st.write("Tidak ada artikel yang ditemukan untuk topik ini.")

def page_3():
    st.subheader("Detail Artikel")
    
    article_id = st.session_state.get("selected_article_id", None)
    paylo = st.session_state["payload"]
    if article_id is None:
        st.write("Tidak ada artikel yang dipilih. Silakan kembali ke pencarian.")
        if st.button("Kembali ke pencarian"):
            st.session_state["page"] = "page_2"
            st.experimental_rerun()
        return
    
    # Query contoh untuk fetch detail artikel
    graph_query = f"""
    MATCH (p:User)-[r]->(a:Article)
    WHERE a.id_berita CONTAINS '{article_id}'
    RETURN p.name AS person_name, 
        a.kategori AS article_kategori, 
        a.tgl_publikasi AS article_pub, 
        a.jumlah_pembaca AS article_p  
    """
    graph_data = ag.fetch_graph_data(graph_query)
    st.write(graph_data)
    if graph_data:
        for record in graph_data:
            st.write(f"**Judul Artikel:** {paylo['judul']}")
            st.write(f"**Tgl Artikel:** {record['article_pub']}")
            st.write(f"**kategori Artikel:** {record['article_kategori']}")
            st.write(f"**jumlah pembaca Artikel:** {record['article_p']}")
            st.write(f"**Isi Artikel:** {paylo['isi']}")
            st.write(f"**Penulis:** {record['person_name']}")

    else:
        st.write("Artikel tidak ditemukan.")
    
    if st.button("Kembali ke pencarian"):
        st.session_state["page"] = "page_2"
        st.experimental_rerun()

# Atur halaman default
if "page" not in st.session_state:
    st.session_state["page"] = "page_1"

# Sidebar hanya untuk Page 1 dan Page 2
page = st.sidebar.selectbox(
    "Pilih Halaman",
    ("Page 1: Cari Nama Orang/Artikel", "Page 2: Cari Artikel dengan Topik Sama"),
    index=0 if st.session_state["page"] == "page_1" else 1
)

# Update session_state dari sidebar agar sinkron
if page == "Page 1: Cari Nama Orang/Artikel":
    st.session_state["page"] = "page_1"
elif page == "Page 2: Cari Artikel dengan Topik Sama":
    st.session_state["page"] = "page_2"

# Render halaman sesuai session_state
if st.session_state["page"] == "page_1":
    page_1()
elif st.session_state["page"] == "page_2":
    page_2()
elif st.session_state["page"] == "page_3":
    page_3()