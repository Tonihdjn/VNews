import torch
from transformers import BertTokenizer, BertModel
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import json
client = QdrantClient(url="http://localhost:6333")  # Adjust URL if necessary
# Initialize BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Function to generate embeddings using BERT
def generate_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Take the [CLS] token (first token) embedding as sentence embedding
    embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return embedding

# Initialize Qdrant clie

# Recreate collection with vector configuration
collection_name = "article's"


articles =[
    {
        "id": "12001",
        "judul": "Pemilu 2024 Berlangsung Damai dan Tertib di Seluruh Indonesia",
        "isi": "Pemilu serentak 2024 yang diadakan di Indonesia pada tanggal 14 Februari lalu berjalan dengan lancar dan damai. Meskipun ada tantangan logistik di daerah-daerah terpencil, proses pemungutan suara tetap berjalan dengan aman. Para pemilih datang ke TPS dengan antusias, menunjukkan tingkat partisipasi yang tinggi di seluruh Indonesia, baik di kota besar maupun pedesaan.",
        "vector": []
    },
    {
        "id": "12002",
        "judul": "Harga Sembako Naik Menjelang Lebaran: Apa Penyebabnya?",
        "isi": "Menjelang Hari Raya Idul Fitri, harga sembako di pasar tradisional dan supermarket mengalami kenaikan yang signifikan. Kenaikan harga ini terutama terjadi pada bahan makanan pokok seperti beras, minyak goreng, dan daging ayam. Kenaikan ini disebabkan oleh tingginya permintaan menjelang Lebaran, yang seringkali lebih tinggi dari biasanya.",
        "vector": []
    },
    {
        "id": "12003",
        "judul": "Persaingan Ketat di Dunia Start-Up Teknologi Indonesia: Peluang dan Tantangan",
        "isi": "Industri start-up teknologi di Indonesia berkembang pesat. Dengan semakin banyaknya investor yang tertarik untuk berinvestasi, para pendiri start-up kini harus berinovasi dengan cepat. Namun, persaingan yang ketat dan regulasi yang berubah-ubah menambah tantangan bagi mereka yang ingin bertahan di pasar.",
        "vector": []
    },
    {
        "id": "12004",
        "judul": "Pembangunan Infrastruktur Jalan Tol untuk Meningkatkan Konektivitas Antar Daerah",
        "isi": "Pembangunan jalan tol yang menghubungkan berbagai kota besar dan daerah-daerah terpencil di Indonesia semakin diperluas. Proyek jalan tol yang menghubungkan Lampung hingga Aceh ini diharapkan dapat memangkas biaya logistik dan mempercepat distribusi barang, serta meningkatkan konektivitas antar kota.",
        "vector": []
    },
    {
        "id": "12005",
        "judul": "Inovasi Teknologi dalam Dunia Pendidikan di Indonesia",
        "isi": "Di Indonesia, teknologi semakin banyak digunakan dalam dunia pendidikan. Pembelajaran online dan penggunaan aplikasi pendidikan membantu siswa dan guru untuk berinteraksi lebih efektif. Namun, tantangan terbesar yang dihadapi adalah kesenjangan akses teknologi antara daerah urban dan rural.",
        "vector": []
    },
    {
        "id": "12006",
        "judul": "Perkembangan Ekonomi Digital di Indonesia: Peluang dan Tantangan",
        "isi": "Ekonomi digital Indonesia terus berkembang, dengan semakin banyaknya platform e-commerce dan fintech yang bermunculan. Meskipun demikian, tantangan utama adalah ketimpangan infrastruktur dan regulasi yang belum sepenuhnya siap menghadapi kemajuan teknologi.",
        "vector": []
    },
    {
        "id": "12007",
        "judul": "Tantangan dalam Mengelola Sampah Plastik di Indonesia",
        "isi": "Masalah sampah plastik di Indonesia semakin serius. Walaupun banyak inisiatif untuk mengurangi penggunaan plastik, tingkat pengelolaan sampah yang buruk dan kurangnya kesadaran masyarakat menghambat upaya tersebut. Oleh karena itu, dibutuhkan kolaborasi antara pemerintah, masyarakat, dan sektor swasta untuk mengatasi masalah ini.",
        "vector": []
    },
    {
        "id": "12008",
        "judul": "Keberhasilan Program Vaksinasi di Indonesia",
        "isi": "Program vaksinasi COVID-19 di Indonesia telah berhasil mencapai target yang diinginkan. Setelah beberapa bulan pelaksanaan, sebagian besar penduduk Indonesia telah divaksin, dan pandemi mulai terkendali. Meskipun demikian, masih ada tantangan dalam distribusi vaksin ke daerah-daerah terpencil.",
        "vector": []
    },
    {
        "id": "12009",
        "judul": "Peluang dan Tantangan Sektor Pariwisata Indonesia",
        "isi": "Sektor pariwisata Indonesia mulai pulih setelah pandemi, dengan destinasi wisata yang kembali ramai dikunjungi. Meskipun demikian, sektor ini harus menghadapi tantangan seperti menjaga keberlanjutan lingkungan dan meningkatkan kualitas layanan wisata.",
        "vector": []
    },
    {
        "id": "12010",
        "judul": "Pengembangan Sektor Energi Terbarukan di Indonesia",
        "isi": "Indonesia berkomitmen untuk mengembangkan sektor energi terbarukan sebagai bagian dari upaya global untuk mengurangi emisi karbon. Proyek-proyek energi surya dan angin semakin digalakkan di berbagai daerah, meskipun tantangan besar adalah pendanaan dan pengelolaan teknologi.",
        "vector": []
    },
    {
        "id": "12011",
        "judul": "Peran Pemerintah dalam Meningkatkan Kualitas Pendidikan",
        "isi": "Pemerintah terus berupaya meningkatkan kualitas pendidikan di Indonesia dengan memperbaiki infrastruktur sekolah, meningkatkan kualitas guru, dan mendigitalisasi proses pembelajaran. Program-program ini diharapkan dapat menekan angka ketidakmerataan kualitas pendidikan.",
        "vector": []
    },
    {
        "id": "12012",
        "judul": "Tren Teknologi Terbaru yang Mempengaruhi Dunia Industri",
        "isi": "Teknologi terbaru seperti AI, blockchain, dan IoT semakin mengubah cara perusahaan beroperasi. Di Indonesia, perusahaan-perusahaan mulai mengadopsi teknologi ini untuk meningkatkan efisiensi dan produktivitas mereka, meskipun masalah integrasi dan regulasi masih menjadi hambatan.",
        "vector": []
    },
    {
        "id": "12013",
        "judul": "Digitalisasi Layanan Publik untuk Mempercepat Pembangunan",
        "isi": "Pemerintah Indonesia semakin mendorong digitalisasi layanan publik untuk meningkatkan efisiensi dan transparansi dalam pengelolaan pemerintahan. Meskipun demikian, banyak daerah yang masih kesulitan dalam implementasi digitalisasi karena terbatasnya akses internet.",
        "vector": []
    },
    {
        "id": "12014",
        "judul": "Berkembangnya Ekonomi Hijau di Indonesia",
        "isi": "Ekonomi hijau semakin populer di Indonesia. Sektor-sektor seperti energi terbarukan, pertanian berkelanjutan, dan wisata alam berkelanjutan menunjukkan pertumbuhan yang signifikan, mendorong Indonesia untuk menjadi pemimpin dalam pembangunan ekonomi yang ramah lingkungan.",
        "vector": []
    },
    {
        "id": "12015",
        "judul": "Perubahan Iklim dan Dampaknya pada Sumber Daya Alam",
        "isi": "Perubahan iklim global membawa dampak besar terhadap sumber daya alam Indonesia, mulai dari peningkatan suhu yang mempengaruhi sektor pertanian hingga perubahan pola curah hujan yang menyebabkan bencana alam seperti banjir dan kekeringan.",
        "vector": []
    }
]

def convert_id(id):
    return int(id)
# Embed articles and add them to Qdrant
for article in articles:
    text = article['judul'] + " " + article['isi']
    id = convert_id(article['id'])
    embedding = generate_embedding(text)

    point = PointStruct(
        id=id,
        vector=embedding.tolist(),
        payload={
            "judul": article['judul'],
            "isi": article['isi']
        }
    )

    client.upload_points(
        collection_name=collection_name,
        points=[point]
    )



print("Articles have been successfully embedded and uploaded to Qdrant.")
