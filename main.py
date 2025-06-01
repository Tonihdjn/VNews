# import streamlit as st
# import pandas as pd
# import time
# import agregator as ag
# import embed as em

# st.set_page_config(page_title="Graph & Vector Database Integration", layout="wide")

# RESULT_LIMIT = 20  # batasi hasil maksimal di semua query

# def page_1():
#     st.subheader("Cari Nama Orang/Artikel")
#     query = st.text_input("Masukkan nama orang atau artikel:")

#     if query:
#         # Query tanpa index dengan LIMIT
#         graph_query_no_index = f"""
#             MATCH (p:User)-[r]->(a:Article)
#             WHERE p.authors CONTAINS '{query}'
#             RETURN p.authors AS person_name, 
#                    a.id_artikel AS article_title, 
#                    a.category AS article_kategori, 
#                    type(r) AS relationship_type
#             LIMIT {RESULT_LIMIT}
#         """

#         # Query dengan index fulltext dengan LIMIT
#         graph_query_index = f"""
#             CALL db.index.fulltext.queryNodes('authorsIndex', '{query}') YIELD node AS p, score
#             MATCH (p)-[r]->(a:Article)
#             RETURN p.authors AS person_name,
#                    a.id_artikel AS article_title,
#                    a.category AS article_kategori,
#                    type(r) AS relationship_type,
#                    score
#             ORDER BY score DESC
#             LIMIT {RESULT_LIMIT}
#         """

#         start_no = time.time()
#         res_no = ag.fetch_graph_data(graph_query_no_index)
#         dur_no = time.time() - start_no

#         start_idx = time.time()
#         res_idx = ag.fetch_graph_data(graph_query_index)
#         dur_idx = time.time() - start_idx

#         st.write(f"Waktu query tanpa index: {dur_no:.4f} detik")
#         st.write(f"Waktu query dengan index: {dur_idx:.4f} detik")

#         if res_idx:
#             df = pd.DataFrame(res_idx)
#             st.write("Hasil Pencarian dengan Index:")
#             st.dataframe(df)
#         elif res_no:
#             df = pd.DataFrame(res_no)
#             st.write("Hasil Pencarian tanpa Index:")
#             st.dataframe(df)
#         else:
#             st.write("Tidak ada hasil ditemukan.")

# def page_2():
#     st.subheader("Cari Artikel dengan Topik Sama")
#     query_text = st.text_input("Masukkan topik atau kata kunci:")

#     if query_text:
#         query_vector = em.generate_embedding(query_text)

#         start_no = time.time()
#         results_no_index = ag.search_vector_db_no_index(query_vector, k=RESULT_LIMIT)
#         dur_no = time.time() - start_no

#         start_idx = time.time()
#         results_index = ag.search_vector_db(query_vector, k=RESULT_LIMIT)
#         dur_idx = time.time() - start_idx

#         st.write(f"Waktu pencarian tanpa index (linear scan): {dur_no:.4f} detik")
#         st.write(f"Waktu pencarian dengan index: {dur_idx:.4f} detik")

#         results_list = [{"Artikel ID": r.id, "Skor": r.score, "Payload": r.payload} for r in results_index]
#         if results_list:
#             st.write("Artikel dengan topik yang relevan (index):")
#             for idx, artikel in enumerate(results_list):
#                 title = artikel["Payload"].get("headline", f"Artikel {idx+1}")
#                 if st.button(title, key=f"artikel_btn_{idx} : {title}"):
#                     st.session_state["selected_article_id"] = artikel["Artikel ID"]
#                     st.session_state["payload"] = artikel["Payload"]
#                     st.session_state["page"] = "page_3"
#                     page_3()
#                     return
#         else:
#             st.write("Tidak ada artikel ditemukan.")

# def page_3():
#     st.subheader("Detail Artikel")
#     article_id = st.session_state.get("selected_article_id", None)
#     paylo = st.session_state.get("payload", {})

#     if article_id is None:
#         st.write("Tidak ada artikel yang dipilih. Silakan kembali ke pencarian.")
#         if st.button("Kembali ke pencarian"):
#             st.session_state["page"] = "page_2"
#             st.experimental_rerun()
#         return

#     graph_query_no_index = f"""
#     MATCH (p:User)-[r]->(a:Article)
#     WHERE a.id_artikel = {article_id}
#     RETURN p.authors AS person_name, 
#            a.category AS article_kategori, 
#            a.date AS article_pub 
#     LIMIT 1
#     """

#     graph_query_index = f"""
#     CALL db.index.fulltext.queryNodes('articleIdIndex', '{article_id}') YIELD node AS a
#     MATCH (p:User)-[r]->(a)
#     RETURN p.authors AS person_name, 
#            a.category AS article_kategori, 
#            a.date AS article_pub
#     LIMIT 1
#     """

#     start_no = time.time()
#     graph_data_no_index = ag.fetch_graph_data(graph_query_no_index)
#     duration_no_index = time.time() - start_no

#     start_idx = time.time()
#     graph_data_index = ag.fetch_graph_data(graph_query_index)
#     duration_index = time.time() - start_idx

#     st.write(f"Waktu query detail tanpa index: {duration_no_index:.4f} detik")
#     st.write(f"Waktu query detail dengan index: {duration_index:.4f} detik")

#     graph_data = graph_data_index if graph_data_index else graph_data_no_index

#     if graph_data:
#         record = graph_data[0]
#         article_pub = record.get('article_pub')
#         try:
#             article_pub_str = article_pub.to_native().strftime("%Y-%m-%d")
#         except Exception:
#             article_pub_str = str(article_pub) if article_pub else "Tanggal tidak tersedia"

#         st.write(f"*Judul Artikel:* {paylo.get('headline', '-')}")
#         st.write(f"*Tgl Artikel:* {article_pub_str}")
#         st.write(f"*Kategori Artikel:* {record.get('article_kategori', '-')}")
#         st.write(f"*Isi Artikel:* {paylo.get('short_desc', '-')}")
#         st.write(f"*Penulis:* {record.get('person_name', '-')}")
#     else:
#         st.write("Artikel tidak ditemukan.")

#     if st.button("Kembali ke pencarian"):
#         st.session_state["page"] = "page_2"
#         st.experimental_rerun()

# if "page" not in st.session_state:
#     st.session_state["page"] = "page_1"

# page = st.sidebar.selectbox(
#     "Pilih Halaman",
#     ("Page 1: Cari Nama Orang/Artikel", "Page 2: Cari Artikel dengan Topik Sama"),
#     index=0 if st.session_state["page"] == "page_1" else 1
# )

# if page == "Page 1: Cari Nama Orang/Artikel":
#     st.session_state["page"] = "page_1"
# elif page == "Page 2: Cari Artikel dengan Topik Sama":
#     st.session_state["page"] = "page_2"

# if st.session_state["page"] == "page_1":
#     page_1()
# elif st.session_state["page"] == "page_2":
#     page_2()
# elif st.session_state["page"] == "page_3":
#     page_3()

import streamlit as st
import pandas as pd
import time
import agregator as ag
import embed as em

st.set_page_config(page_title="Graph & Vector Database Integration", layout="wide")

RESULT_LIMIT = 20

def page_1():
    st.subheader("Cari Nama Orang")
    query = st.text_input("Masukkan nama orang:")

    if query:
        graph_query_no_index = """
            MATCH (p:User)-[r]->(a:Article)
            WHERE p.authors CONTAINS $query_param
            RETURN p.authors AS person_name, 
                   a.id_artikel AS article_title, 
                   a.category AS article_kategori, 
                   type(r) AS relationship_type
            
        """

        graph_query_index = """
            CALL db.index.fulltext.queryNodes('authorsIndex', $query_param) YIELD node AS p, score
            MATCH (p)-[r]->(a:Article)
            RETURN p.authors AS person_name,
                   a.id_artikel AS article_title,
                   a.category AS article_kategori,
                   type(r) AS relationship_type,
                   score
            ORDER BY score DESC
            
        """

        start_no = time.time()
        res_no = ag.fetch_graph_data(graph_query_no_index, {"query_param": query, "limit_param": RESULT_LIMIT})
        dur_no = time.time() - start_no

        start_idx = time.time()
        res_idx = ag.fetch_graph_data(graph_query_index, {"query_param": query, "limit_param": RESULT_LIMIT})
        dur_idx = time.time() - start_idx

        st.write(f"Waktu query tanpa index: {dur_no:.4f} detik")
        st.write(f"Waktu query dengan index: {dur_idx:.4f} detik")

        if res_idx:
            df = pd.DataFrame(res_idx)
            st.write("Hasil Pencarian dengan Index:")
            st.dataframe(df)
        elif res_no:
            df = pd.DataFrame(res_no)
            st.write("Hasil Pencarian tanpa Index:")
            st.dataframe(df)
        else:
            st.write("Tidak ada hasil ditemukan.")

def page_2():
    st.subheader("Bandingkan Performa Pencarian Vektor")
    query_text = st.text_input("Masukkan topik atau kata kunci:")

    if query_text:
        # 1. Generate embedding dari query
        query_vector = em.generate_embedding(query_text)

        # 2. Lakukan pencarian dengan dan tanpa index HNSW untuk perbandingan
        start_no_idx = time.time()
        results_no_index = ag.search_vector_db_brute_force(query_vector, k=RESULT_LIMIT)
        dur_no_idx = time.time() - start_no_idx

        start_idx = time.time()
        results_index = ag.search_vector_db_with_index(query_vector, k=RESULT_LIMIT)
        dur_idx = time.time() - start_idx

        # 3. Tampilkan hasil perbandingan waktu
        st.write(f"Waktu pencarian **Tanpa HNSW Index** (Brute-force): **{dur_no_idx:.4f} detik**")
        st.write(f"Waktu pencarian **Dengan HNSW Index**: **{dur_idx:.4f} detik**")
        st.write("---")

        # 4. Filter hasil dari pencarian yang lebih cepat (dengan index) untuk ditampilkan
        # PERBAIKAN: Gunakan `r['score']` untuk mengakses skor dari dictionary
        filtered_results = [r for r in results_index if r['score'] >= 0.3]

        # 5. Tampilkan hasil yang sudah difilter
        if filtered_results:
            st.write("Artikel dengan topik yang relevan (ditemukan menggunakan HNSW index):")
            
            # PERBAIKAN: Akses data dari 'artikel' yang merupakan sebuah dictionary
            for idx, artikel in enumerate(filtered_results):
                # Gunakan key 'payload' (lowercase)
                title = artikel['payload'].get("headline", f"Artikel {idx+1}")
                
                # Gunakan key 'id' untuk session state dan key button
                if st.button(title, key=f"artikel_btn_{artikel['id']}"):
                    st.session_state["selected_article_id"] = artikel['id']
                    st.session_state["payload"] = artikel['payload']
                    st.session_state["page"] = "page_3"
                    page_3()
                    # Di versi Streamlit baru, st.rerun() lebih direkomendasikan
                    # untuk memicu penggantian halaman
            
                    return # Hentikan eksekusi fungsi setelah berpindah halaman
        else:
            st.write("Tidak ada artikel yang cukup relevan ditemukan (skor >= 0.3).")

def page_3():
    st.subheader("Detail Artikel")
    article_id = st.session_state.get("selected_article_id", None)
    paylo = st.session_state.get("payload", {})

    if article_id is None:
        st.write("Tidak ada artikel yang dipilih. Silakan kembali ke pencarian.")
        if st.button("Kembali ke pencarian"):
            st.session_state["page"] = "page_2"
            st.experimental_rerun()
        return

    # Cek eksistensi article_id di vector DB dulu
    if not ag.check_vector_exists(article_id):
        st.write("Artikel tidak ditemukan di Vector Database.")
        if st.button("Kembali ke pencarian"):
            st.session_state["page"] = "page_2"
            st.experimental_rerun()
        return

    graph_query_no_index = """
    MATCH (p:User)-[r]->(a:Article)
    WHERE a.id_artikel = $article_id
    RETURN p.authors AS person_name, 
           a.category AS article_kategori, 
           a.date AS article_pub
    LIMIT 1
    """

    graph_query_index = """
    CALL db.index.fulltext.queryNodes('articleIdIndex', $article_id) YIELD node AS a
    MATCH (p:User)-[r]->(a)
    RETURN p.authors AS person_name, 
           a.category AS article_kategori, 
           a.date AS article_pub
    LIMIT 1
    """

    start_no = time.time()
    data_no = ag.fetch_graph_data(graph_query_no_index, {"article_id": article_id})
    dur_no = time.time() - start_no

    start_idx = time.time()
    data_idx = ag.fetch_graph_data(graph_query_index, {"article_id": str(article_id)})
    dur_idx = time.time() - start_idx

    st.write(f"Waktu query detail tanpa index: {dur_no:.4f} detik")
    st.write(f"Waktu query detail dengan index: {dur_idx:.4f} detik")

    graph_data = data_idx if data_idx else data_no

    if graph_data:
        record = graph_data[0]
        article_pub = record.get('article_pub')
        try:
            article_pub_str = article_pub.to_native().strftime("%Y-%m-%d")
        except Exception:
            article_pub_str = str(article_pub) if article_pub else "Tanggal tidak tersedia"

        st.write(f"*Judul Artikel:* {paylo.get('headline', '-')}")
        st.write(f"*Tanggal Artikel:* {article_pub_str}")
        st.write(f"*Kategori Artikel:* {record.get('article_kategori', '-')}")
        st.write(f"*Isi Artikel:* {paylo.get('short_desc', '-')}")
        st.write(f"*Penulis:* {record.get('person_name', '-')}")
    else:
        st.write("Artikel tidak ditemukan.")

    if st.button("Kembali ke pencarian"):
        st.session_state["page"] = "page_2"
        st.experimental_rerun()

if "page" not in st.session_state:
    st.session_state["page"] = "page_1"

page = st.sidebar.selectbox(
    "Pilih Halaman",
    ("Page 1: Cari Nama Orang/Artikel", "Page 2: Cari Artikel dengan Topik Sama"),
    index=0 if st.session_state["page"] == "page_1" else 1
)

if page == "Page 1: Cari Nama Orang/Artikel":
    st.session_state["page"] = "page_1"
elif page == "Page 2: Cari Artikel dengan Topik Sama":
    st.session_state["page"] = "page_2"

if st.session_state["page"] == "page_1":
    page_1()
elif st.session_state["page"] == "page_2":
    page_2()
elif st.session_state["page"] == "page_3":
    page_3()