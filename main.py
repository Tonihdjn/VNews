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
            MATCH (p:Person)-[r]->(a:Article)
            WHERE p.name CONTAINS '{query}' OR a.title CONTAINS '{query}'
            RETURN p.name AS person_name, 
                   a.title AS article_title, 
                   a.content AS article_content, 
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
                        "Content": record["article_content"],
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

# Fungsi untuk menampilkan halaman kedua: Mencari artikel dengan topik yang sama
def page_2():
    st.subheader("Cari Artikel dengan Topik Sama")
    
    # Input query teks untuk mencari artikel berdasarkan topik
    query_text = st.text_input("Masukkan topik atau kata kunci:")
    
    if query_text:
        # Mengubah teks menjadi vektor menggunakan SentenceTransformer
        query_vector = em.generate_embedding(query_text)
        
        # Mencari artikel berdasarkan query vektor di Qdrant
        results = ag.search_vector_db(query_vector)
        
        # Menyusun hasil pencarian
        results_list = [{"Artikel ID": result.id, "Skor": result.score, "Payload": result.payload} for result in results]
        
        if results_list:
            st.write("Artikel dengan topik yang relevan:")
            st.dataframe(pd.DataFrame(results_list))
        else:
            st.write("Tidak ada artikel yang ditemukan untuk topik ini.")

# Fungsi untuk menampilkan halaman ketiga: Menampilkan detail artikel yang dipilih
def page_3():
    st.subheader("Detail Artikel")
    
    # Menampilkan ID artikel yang dipilih
    article_id = st.text_input("Masukkan ID Artikel untuk melihat detail:")
    if article_id:
        # Query untuk mengambil informasi lebih lanjut tentang artikel yang dipilih
        graph_query = f"""
        MATCH (p:Person)-[:WRITES]->(a:Article)
        WHERE a.id = '{article_id}'
        RETURN p.name AS person_name, a.title AS article_title, a.content AS article_content
        """
        graph_data = ag.fetch_graph_data(graph_query)
        
        if graph_data:
            for record in graph_data:
                st.write(f"**Artikel Title**: {record['article_title']}")
                st.write(f"**Isi Artikel**: {record['article_content']}")
                st.write(f"**Penulis**: {record['person_name']}")
        else:
            st.write("Artikel tidak ditemukan.")

# Fungsi untuk memilih halaman
page = st.sidebar.selectbox("Pilih Halaman", ("Page 1: Cari Nama Orang/Artikel", "Page 2: Cari Artikel dengan Topik Sama", "Page 3: Detail Artikel"))

if page == "Page 1: Cari Nama Orang/Artikel":
    page_1()
elif page == "Page 2: Cari Artikel dengan Topik Sama":
    page_2()
elif page == "Page 3: Detail Artikel":
    page_3()