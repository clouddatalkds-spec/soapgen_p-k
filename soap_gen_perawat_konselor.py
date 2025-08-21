import streamlit as st
import asyncio
import json
import httpx


# --- Data untuk Perawat ---
nursing_diagnoses_list = [
    "Bersihan Jalan Napas Tidak Efektif",
    "Gangguan Penyapihan Ventilator",
    "Gangguan Pertukaran Gas",
    "Gangguan Ventilasi Spontan",
    "Pola Napas Tidak Efektif",
    "Risiko Aspirasi",
    "Gangguan Sirkulasi Spontan",
    "Penurunan Curah Jantung",
    "Perfusi perifer tidak efektif",
    "Risiko Gangguan Sirkulasi Spontan",
    "Resiko Penurunan Curah Jantung",
    "Resiko Perdarahan",
    "Risiko Perfusi Gastrointestinal Tidak Efektif",
    "Risiko Perfusi Miokard Tidak Efektif",
    "Risiko Perfusi Perifer Tidak Efektif",
    "Risiko Perfusi Renal Tidak Efektif",
    "Risiko Perfusi Serebral Tidak Efektif",
    "Berat Badan Lebih",
    "Defisit Nutrisi",
    "Diare",
    "Disfungsi Motilitas Gastrointestinal",
    "Hipervolemia",
    "Hipovolemia",
    "Ikterik Neonatus",
    "Kesiapan Peningkatan Keseimbangan Cairan",
    "Kesiapan Peningkatan Nutrisi",
    "Ketidakstabilan Kadar Glukosa Darah",
    "Menyusui Efektif",
    "Menyusui Tidak Efektif",
    "Obesitas",
    "Risiko Berat Badan Lebih",
    "Resiko Defisit Nutrisi",
    "Risiko disfungsi motilitas gastrointestinal",
    "Risiko Hipovolemia",
    "Risiko Ikterik Neonatus",
    "Risiko Ketidakseimbangan Cairan",
    "Resiko Ketidakseimbangan Elektrolit",
    "Resiko Ketidakstabilan Glukosa Darah",
    "Resiko Syok",
    "Gangguan Eliminasi Urin",
    "Inkontinensia Fekal",
    "Inkontinensia Urin Berlanjut",
    "Inkontinensia Urin Berlebih",
    "Inkontinensia Urin Fungsional",
    "Inkontinensia Urin Refleks",
    "Inkontinensia Urin Stres",
    "Inkontinensia Urine Urgensi",
    "Kesiapan Peningkatan Eliminasi Urin",
    "KONSTIPASI",
    "Retensi Urine",
    "Risiko Inkontinensia Urine Urgensi",
    "Risiko Konstipasi",
    "Disorganisasi Perilaku Bayi",
    "Gangguan Mobilitas Fisik",
    "Gangguan Pola Tidur",
    "Intoleransi Aktivitas",
    "Keletihan",
    "Kesiapan Peningkatan Tidur",
    "Risiko Disorganisasi Perilaku Bayi",
    "Risiko Intoleransi Aktivitas",
    "Disrefleksia Otonom",
    "Gangguan Memori",
    "Gangguan Menelan",
    "Konfusi Akut",
    "Konfusi Kronis",
    "Penurunan Kapasitas Adaptif Intrakranial",
    "Risiko Disfungsi Neurovaskuler Perifer",
    "Risiko Konfusi Akut",
    "Disfungsi Seksual",
    "Kesiapan Persalinan",
    "Pola Seksual Tidak Efektif",
    "Risiko Disfungsi Seksual",
    "Risiko Kehamilan Tidak Dikehendaki",
    "Gangguan Rasa Nyaman",
    "Ketidaknyamanan Pasca Partum",
    "Nausea",
    "Nyeri Akut",
    "Nyeri Kronis",
    "Nyeri Melahirkan",
    "Ansietas",
    "Berduka",
    "Distres Spiritual",
    "Gangguan Citra Tubuh",
    "Gangguan Identitas Diri",
    "Gangguan Persepsi Sensori (Pendengaran)",
    "Harga Diri Rendah Kronis",
    "Harga Diri Rendah Situasional",
    "Keputusasaan",
    "Kesiapan Peningkatan Konsep Diri",
    "Kesiapan Peningkatan Koping Keluarga",
    "Kesiapan Peningkatan Koping Komunitas",
    "Ketidakberdayaan",
    "Ketidakmampuan Koping Keluarga",
    "Koping Defensif",
    "Koping Komunitas Tidak Efektif",
    "Koping Tidak Efektif",
    "Penurunan Koping Keluarga",
    "Penyangkalan Tidak Efektif",
    "Perilaku Kesehatan Cenderung Berisiko",
    "Risiko Distres Spiritual",
    "Risiko Harga Diri Rendah",
    "Risiko Harga Diri Rendah Situasional",
    "Risiko Ketidakberdayaan",
    "Sindrom Pasca Trauma",
    "Waham",
    "Gangguan Tumbuh Kembang",
    "Risiko Gangguan Perkembangan",
    "Risiko Gangguan Pertumbuhan",
    "Defisit Perawatan Diri (spesifikan)",
    "Defisit Kesehatan Komunitas",
    "Defisit Pengetahuan",
    "Kesiapan Peningkatan Manajemen Kesehatan",
    "Kesiapan Peningkatan Pengetahuan",
    "Ketidakpatuhan",
    "Manajemen Kesehatan Keluarga Tidak Efektif",
    "Manajemen Kesehatan Tidak Efektif",
    "Pemeliharaan Kesehatan Tidak Efektif",
    "Gangguan Interaksi Sosial",
    "Gangguan Komunikasi Verbal",
    "Gangguan Proses Keluarga",
    "Isolasi Sosial",
    "Kesiapan Peningkatan Menjadi Orang Tua",
    "Kesiapan Peningkatan Proses Keluarga",
]

nursing_prompt_template = """
Sebagai perawat, buatlah catatan keperawatan lengkap dengan format SOAP (Subjective, Objective, Assessment, Planning) untuk diagnosis keperawatan berikut: {diagnosis}.

Gunakan deskripsi pasien berikut untuk membuat catatan yang lebih spesifik:
{description}

Berikan informasi untuk setiap bagian (S, O, A, P). Pastikan format keluarannya jelas, dengan setiap bagian diawali dengan S:, O:, A:, dan P:.

S: Tulis keluhan subjektif pasien.
O: Tulis data objektif seperti tanda-tanda vital, hasil observasi fisik, dan perilaku pasien.
A: Tulis diagnosis keperawatan lengkap berdasarkan data S dan O.
P: Tulis rencana intervensi keperawatan yang relevan.

Format keluaran harus seperti contoh berikut:
S: [Teks subjektif]
O: [Teks objektif]
A: [Teks asesmen]
P: [Teks perencanaan]
"""

# --- Data untuk Konselor Adiksi ---
addiction_diagnoses_list = [
    "Nicotine Abuse/Depedence",
    "Substance-Induced Disorder",
    "Substance Intoxication/Withdrawal",
    "Substance Use Disorder",
    "Chronic Pain",
    "Medical Issue",
    "Adult Child Of An Alcoholic (ACA) Traits",
    "Anger",
    "Antisocial Behavior",
    "Anxiety",
    "ADHD Adolescent",
    "ADHD Adult",
    "Bipolar Disorder",
    "Borderline Traits",
    "Childhood Trauma",
    "Conduct Disorder/Delinquency",
    "Dangerousness/Lethality",
    "Dependent Traits",
    "Eating Disorder and Obesity",
    "Family Conflicts",
    "Gambling",
    "Grief/Loss Unresolved",
    "Impulsivity",
    "Legal Problems",
    "Narcissistic Traits",
    "OCD",
    "Oppositional Defiant Behavior",
    "Posttraumatic Stress Disorder (PTSD)",
    "Psychosis",
    "Self Care Deficits Primary",
    "Self Care Deficits Secondary",
    "Self Harm",
    "Sexual Abuse",
    "Sexual Promiscuity",
    "Sleep Disturbance",
    "Social Anxiety",
    "Spiritual Confusion",
    "Suicidal Ideation",
    "Unipolar Depression",
    "Treatment Resistance",
    "Relapse Proneness",
    "Living Environment Deficiency",
    "Occupational Problems",
    "Parent Child Relational Problem",
    "Partner Relational Conflicts",
    "Peer Group Negativity"
]

addiction_prompt_template = """
Sebagai konselor adiksi di sebuah lembaga rehabilitasi, buatlah catatan konseling dengan format SOAP (Subjective, Objective, Assessment, Planning) untuk klien yang menghadapi isu konseling berikut: {diagnosis}.

Gunakan deskripsi klien berikut untuk membuat catatan yang lebih spesifik:
{description}

Berikan informasi yang relevan untuk setiap bagian (S, O, A, P). Pastikan format keluarannya jelas, dengan setiap bagian diawali dengan S:, O:, A:, dan P:.

S: Tulis keluhan subjektif atau pernyataan klien.
O: Tulis data objektif seperti observasi perilaku, interaksi, dan ekspresi emosi klien selama sesi.
A: Tulis asesmen atau diagnosis fungsional berdasarkan data S dan O.
P: Tulis rencana intervensi jangka panjang dan jangka pendek konseling yang relevan dengan mengunakan kriteria SMART (Specific, Measurable, Achievable, Relevant, Time-bound), dan setiap rencana intervensi berikan satu kalimat utuh dari kriteria SMART serta langkah selanjutnya.

Format keluaran harus seperti contoh berikut:
S: [Teks subjektif klien]
O: [Teks objektif konselor]
A: [Teks asesmen konselor]
P: [Teks perencanaan konselor]
"""

# Fungsi untuk membuat panggilan API async ke model Gemini
async def generate_text_from_model(prompt):
    """
    Menghasilkan teks menggunakan Gemini API berdasarkan prompt yang diberikan.
    """
    # Ambil API_KEY dari session_state
    api_key = st.session_state.get('api_key', None)
    if not api_key:
        st.error("Kesalahan: Kunci API tidak ditemukan. Silakan masukkan kunci API Anda.")
        return None

    try:
        chat_history = []
        chat_history.append({"role": "user", "parts": [{"text": prompt}]})
        
        payload = {
            "contents": chat_history,
            "generationConfig": {
                "responseMimeType": "text/plain",
            }
        }
        
        apiUrl = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
        
        async with httpx.AsyncClient() as client:
            # Implementasi exponential backoff untuk mencoba kembali
            for i in range(5):  # Maksimal 5 kali percobaan
                try:
                    response = await client.post(
                        apiUrl,
                        headers={"Content-Type": "application/json"},
                        json=payload,
                        timeout=30.0  # Atur batas waktu yang wajar
                    )
                    response.raise_for_status()
                    result = response.json()
                    
                    if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
                        text = result["candidates"][0]["content"]["parts"][0]["text"]
                        return text
                    else:
                        st.error("Kesalahan: Format respons API tidak terduga.")
                        return None
                except httpx.HTTPStatusError as e:
                    if e.response.status_code in [429, 503] and i < 4:
                        st.warning(f"Batas laju API terlampaui atau layanan tidak tersedia. Mencoba lagi dalam {2**i} detik...")
                        await asyncio.sleep(2**i)  # Exponential backoff
                    else:
                        raise e
    except Exception as e:
        st.error(f"Kesalahan selama panggilan API: {e}")
        return None

async def generate_soap_note_async(diagnosis_key, description, prompt_template):
    """
    Menghasilkan catatan SOAP lengkap secara asinkron dengan memanggil LLM.
    """
    prompt = prompt_template.format(diagnosis=diagnosis_key, description=description)
    
    with st.spinner("Sedang menghasilkan catatan SOAP..."):
        full_note_raw = await generate_text_from_model(prompt)

    if not full_note_raw:
        return "Gagal menghasilkan catatan SOAP. Pastikan kunci API Anda valid dan terisi."
    
    return full_note_raw

# Pengaturan halaman Streamlit
st.set_page_config(
    page_title="Generator Catatan SOAP Gabungan",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Judul utama aplikasi
st.title("Generator Catatan SOAP Gabungan")
st.write("Aplikasi ini menggunakan AI untuk menghasilkan catatan SOAP yang relevan dengan peran yang Anda pilih.")

st.markdown("---")

st.markdown("## Cara Menggunakan Aplikasi")
st.markdown("### 🔑 Kunci API Google")
st.markdown("""
Aplikasi ini memanfaatkan model AI Google Gemini. Untuk menggunakannya, Anda harus memasukkan **kunci API** pribadi Anda.

1.  Kunjungi **Google AI Studio** di [https://aistudio.google.com/](https://aistudio.google.com/).
2.  Masuk dengan akun Google Anda dan ikuti petunjuk untuk membuat kunci API.
3.  Salin kunci API yang dibuat dan tempelkan di kolom yang tersedia di **sidebar** (panel samping).
""")

st.markdown("### ⚠️ Konsekuensi Biaya")
st.markdown("""
Penggunaan API Gemini memiliki batas gratis yang sangat besar. Namun, penting untuk dipahami bahwa setelah batas tersebut terlampaui, akan ada biaya yang dikenakan oleh Google. Aplikasi ini **TIDAK** mengenakan biaya apapun; biaya sepenuhnya dikelola oleh Google berdasarkan penggunaan kunci API Anda.

* **Model**: `gemini-2.5-flash`
* **Tarif**: Sekitar $0.0001 per 1.000 karakter (harga dapat berubah, cek situs Google AI untuk informasi terbaru).
* **Penting**: Kunci API Anda terhubung dengan akun Google Cloud Anda. Pantau penggunaan Anda di Google Cloud Console untuk menghindari biaya tak terduga.
""")

st.markdown("### 📝 Input Klien")
st.markdown("""
* **Pilih Isu Konseling**: Pilih dari daftar isu adiksi yang relevan dengan kasus klien.
* **Deskripsi Klien**: Masukkan detail spesifik tentang klien (usia, latar belakang, riwayat penggunaan, perilaku selama sesi, dll.). Semakin detail deskripsi Anda, semakin akurat catatan SOAP yang dihasilkan.
""")

st.markdown("### ✨ Konsep SMART pada Rencana (P) pada KONSELOR")
st.markdown("""
Bagian **P (Planning)** pada catatan SOAP akan dihasilkan dengan mengikuti konsep **SMART**. Setiap poin intervensi akan dilengkapi dengan penjelasan singkat yang menunjukkan bagaimana poin tersebut memenuhi kriteria SMART.
""")

st.markdown("---")

# --- Masukan Kunci API di sidebar
with st.sidebar:
    st.subheader("Kunci API")
    api_key_input = st.text_input(
        "Masukkan Kunci API Google Anda",
        type="password",
        help="Anda dapat memperoleh kunci API dari Google AI Studio atau Google Cloud."
    )
    if api_key_input:
        st.session_state['api_key'] = api_key_input
        st.success("Kunci API berhasil disimpan!")
    
    # Hapus kunci API jika tombol ditekan (opsional)
    if st.button("Hapus Kunci API"):
        if 'api_key' in st.session_state:
            del st.session_state['api_key']
            st.info("Kunci API telah dihapus dari sesi.")

# Tampilkan pesan jika kunci API belum dimasukkan
if 'api_key' not in st.session_state:
    st.warning("Silakan masukkan kunci API Anda di sidebar untuk menggunakan aplikasi.")
    st.stop() # Hentikan eksekusi kode utama hingga kunci terisi

# --- Pilih peran (role) aplikasi
selected_role = st.radio(
    "Pilih Peran Anda:",
    options=["Perawat", "Konselor Adiksi"],
)

# Berdasarkan peran yang dipilih, atur data yang relevan
if selected_role == "Perawat":
    st.subheader("Generator Catatan SOAP Keperawatan")
    st.write("Buat catatan keperawatan berdasarkan diagnosis keperawatan.")
    diagnoses_list = nursing_diagnoses_list
    prompt_template = nursing_prompt_template
    issue_label = "Pilih Diagnosis Keperawatan:"
    issue_help = "Pilih diagnosis yang paling sesuai dengan kondisi pasien."
    description_label = "Deskripsi Pasien"
    description_help = "Masukkan detail tentang pasien, seperti usia, jenis kelamin, keluhan tambahan, dan riwayat kesehatan yang relevan."
elif selected_role == "Konselor Adiksi":
    st.subheader("Generator Catatan SOAP Konseling Adiksi")
    st.write("Buat catatan konseling berdasarkan isu-isu adiksi.")
    diagnoses_list = addiction_diagnoses_list
    prompt_template = addiction_prompt_template
    issue_label = "Pilih Isu Konseling Adiksi:"
    issue_help = "Pilih isu yang paling sesuai dengan kondisi klien."
    description_label = "Deskripsi Klien"
    description_help = "Masukkan detail tentang klien, seperti usia, latar belakang, dan riwayat penggunaan zat atau perilaku."

# --- Bagian utama aplikasi
selected_issue = st.selectbox(
    issue_label,
    options=diagnoses_list,
    help=issue_help
)

patient_description = st.text_area(
    description_label,
    height=150,
    help=description_help,
    placeholder="Contoh: Pasien laki-laki, 65 tahun, pasca stroke. Mengalami kesulitan menelan dan sering tersedak saat makan. Sering mengeluhkan tenggorokannya terasa 'tercekik'."
)

# Tombol untuk menghasilkan catatan SOAP lengkap
if st.button("Hasilkan Catatan SOAP Lengkap"):
    st.markdown("---")
    
    full_note = asyncio.run(generate_soap_note_async(selected_issue, patient_description, prompt_template))
    
    st.subheader("Catatan SOAP Lengkap")
    st.text_area(
        "Salin teks di bawah:",
        value=full_note,
        height=350,
        help="Klik di dalam kotak teks, lalu gunakan Ctrl+C (atau Cmd+C) untuk menyalin."
    )
    
    st.markdown("---")

# Informasi tambahan
st.markdown("---")

st.info("Aplikasi ini dibuat sebagai contoh. Isi catatan harus disesuaikan dengan kondisi spesifik klien dan diverifikasi oleh tenaga profesional.")
