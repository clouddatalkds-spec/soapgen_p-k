import streamlit as st
import asyncio
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
    "Kesiapan Peningkatan Proses Keluarga"
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

nursing_care_plan_prompt_template = """
Sebagai perawat, buatlah rencana keperawatan yang komprehensif untuk pasien berdasarkan deskripsi berikut:
{description}

Berdasarkan deskripsi pasien di atas, identifikasi 2 Diagnosa Keperawatan yang paling relevan dari daftar berikut:
{diagnosis_list_str}

Berdasarkan deskripsi pasien di atas, identifikasi 1 Diagnosa Resiko yang paling relevan dari daftar berikut:
{diagnosis_list_str}


Gunakan format di bawah ini, dengan setiap bagian yang jelas:

**Diagnosa Keperawatan yang Muncul:**
Sebutkan diagnosis yang paling relevan dari daftar, diikuti dengan Data Subjektif dan Data Objektif yang mendukung dari deskripsi pasien.

**Diagnosa Resiko yang Muncul:**
Sebutkan diagnosis resiko yang paling relevan dari daftar, diikuti dengan Data Dukung.

**Tujuan:**
Sebutkan tujuan jangka pendek (misalnya, dalam 3 hari) dan tujuan jangka panjang (misalnya, dalam 1 minggu) yang realistis.

**Intervensi:**
Daftar setidaknya 3 intervensi keperawatan yang spesifik dan dapat dilakukan untuk mencapai tujuan.

**Rasional:**
Berikan alasan ilmiah atau tujuan dari setiap intervensi yang Anda sebutkan.

Pastikan output Anda terstruktur, profesional, dan mudah dibaca.
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
Sebagai konselor adiksi pada lembaga rehabilitasi narkotika rawat inap, buatlah catatan konseling dengan format SOAP (Subjective, Objective, Assessment, Planning) untuk klien yang menghadapi isu konseling berikut: {diagnosis}.

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

# --- Prompt baru untuk Rencana Rawatan Adiksi ---
# --- Prompt baru untuk Rencana Rawatan Adiksi ---
treatment_plan_prompt_template = """
Sebagai konselor adiksi profesional pada lembaga rehabilitasi narkotika rawat inap, buatlah rencana rawatan yang komprehensif untuk klien berdasarkan deskripsi berikut:
{description}

Berdasarkan deskripsi klien di atas, identifikasi dan daftar setidaknya 3 isu konseling yang paling relevan dari daftar berikut:
{diagnosis_list_str}

**Kekuatan Klien:**
Identifikasi dan daftar minimal 3 kekuatan utama klien yang dapat dimanfaatkan dalam proses pemulihan.

**Potensi Hambatan/Kebutuhan yang Teridentifikasi:**
Daftar potensi hambatan atau kebutuhan spesifik yang mungkin dihadapi klien selama proses rawatan.

**Tujuan Jangka Panjang:**
Buat setidaknya 3 tujuan jangka panjang. Gunakan konsep SMART (Specific, Measurable, Achievable, Relevant, Time-bound) dan jadikan satu kalimat utuh.

**Tujuan Jangka Pendek:**
Buat setidaknya 5 tujuan jangka pendek. Gunakan konsep SMART dan jadikan satu kalimat utuh.

**Sasaran:**
Daftar setidaknya 5 sasaran yang spesifik dan terukur untuk mencapai tujuan jangka pendek. Sasaran harus menjadi langkah-langkah yang dapat dicapai.

**Intervensi:**
Daftar setidaknya 5 intervensi yang relevan dan dapat dilakukan untuk membantu klien mencapai sasaran mereka. Intervensi harus praktis dan berfokus pada tindakan.

Pastikan output Anda terstruktur, profesional, dan mudah dibaca.
"""

# Fungsi untuk membuat panggilan API async ke model Gemini
async def generate_text_from_model(prompt):
    """
    Menghasilkan teks menggunakan Gemini API berdasarkan prompt yang diberikan.
    """
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
            for i in range(5):
                try:
                    response = await client.post(
                        apiUrl,
                        headers={"Content-Type": "application/json"},
                        json=payload,
                        timeout=30.0
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
                        await asyncio.sleep(2**i)
                    else:
                        raise e
    except Exception as e:
        st.error(f"Kesalahan selama panggilan API: {e}")
        return None

async def generate_note_async(description, prompt_template, issues_list=None):
    """
    Menghasilkan catatan secara asinkron dengan memanggil LLM.
    """
    prompt = ""
    if issues_list:
        diagnosis_list_str = ", ".join(issues_list)
        prompt = prompt_template.format(description=description, diagnosis_list_str=diagnosis_list_str)
    else:
        # Menangani prompt yang tidak memerlukan daftar diagnosis
        prompt = prompt_template.format(description=description)

    with st.spinner("Sedang menghasilkan catatan..."):
        full_note_raw = await generate_text_from_model(prompt)

    if not full_note_raw:
        return "Gagal menghasilkan catatan. Pastikan kunci API Anda valid dan terisi."
    
    return full_note_raw

# Pengaturan halaman Streamlit
st.set_page_config(
    page_title="Generator Catatan SOAP dan Rencana Rawatan",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Judul utama aplikasi
st.title("Generator Catatan SOAP dan Rencana Rawatan")
st.write("Aplikasi ini menggunakan AI untuk menghasilkan catatan yang relevan dengan peran yang Anda pilih.INGAT ini hanya alat bantu")

st.markdown("---")

st.markdown("## Cara Menggunakan Aplikasi")
st.markdown("### 🔑 Kunci API Google")
st.markdown("""
Aplikasi ini memanfaatkan model AI Google Gemini. Untuk menggunakannya, Anda harus memasukkan **kunci API** pribadi Anda.

1.  Kunjungi **Google AI Studio** di [https://aistudio.google.com/](https://aistudio.google.com/).
2.  Masuk dengan akun Google Anda dan ikuti petunjuk untuk membuat kunci API.
3.  Salin kunci API yang dibuat dan tempelkan di kolom yang tersedia di **sidebar** (panel samping).
4.  Kunci API bersifat PRIBADI dan RAHASIA maka diharapkan menjaganya.
""")

st.markdown("### ⚠️ Konsekuensi Biaya")
st.markdown("""
Penggunaan API Gemini memiliki batas GRATIS yang sangat besar. Namun, penting untuk dipahami bahwa setelah batas tersebut terlampaui, akan ada biaya yang dikenakan oleh Google. Aplikasi ini **TIDAK** mengenakan biaya apapun; biaya sepenuhnya dikelola oleh Google berdasarkan penggunaan kunci API Anda.

* **Model**: `gemini-2.5-flash`
* **Penting**: Kunci API Anda terhubung dengan akun Google Cloud Anda. Pantau penggunaan Anda di Google Cloud Console untuk menghindari biaya tak terduga.
""")
#* **Tarif**: Sekitar $0.0001 per 1.000 karakter (harga dapat berubah, cek situs Google AI untuk informasi terbaru).

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
    
    if st.button("Hapus Kunci API"):
        if 'api_key' in st.session_state:
            del st.session_state['api_key']
            st.info("Kunci API telah dihapus dari sesi.")

if 'api_key' not in st.session_state:
    st.warning("Silakan masukkan kunci API Anda di sidebar untuk menggunakan aplikasi.")
    st.stop()

# --- Pilih peran (role) aplikasi
selected_role = st.radio(
    "Pilih Peran Anda:",
    options=["Perawat", "Konselor Adiksi"],
)

# --- Pilih jenis dokumen
document_type = None
if selected_role == "Perawat":
    document_type = st.radio(
        "Pilih Jenis Dokumen:",
        options=["Catatan SOAP", "Rencana Keperawatan"]
    )
elif selected_role == "Konselor Adiksi":
    document_type = st.radio(
        "Pilih Jenis Dokumen:",
        options=["Catatan SOAP", "Rencana Rawatan Adiksi"]
    )

# --- Bagian utama aplikasi
if selected_role == "Perawat":
    if document_type == "Catatan SOAP":
        st.subheader("Generator Catatan SOAP Keperawatan")
        st.write("Buat catatan keperawatan berdasarkan diagnosis keperawatan.")
        diagnoses_list = nursing_diagnoses_list
        prompt_template = nursing_prompt_template
        issue_label = "Pilih Diagnosis Keperawatan:"
        issue_help = "Pilih diagnosis yang paling sesuai dengan kondisi pasien."
        description_label = "Deskripsi Pasien"
        description_help = "Masukkan detail tentang pasien, seperti usia, jenis kelamin, keluhan tambahan, dan riwayat kesehatan yang relevan."
        
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
        
        if st.button("Hasilkan Catatan SOAP Lengkap"):
            st.markdown("---")
            full_note = asyncio.run(generate_note_async(patient_description, prompt_template, issue=selected_issue))
            st.subheader("Catatan SOAP Lengkap")
            st.text_area(
                "Salin teks di bawah:",
                value=full_note,
                height=350,
                help="Klik di dalam kotak teks, lalu gunakan Ctrl+C (atau Cmd+C) untuk menyalin."
            )
            st.markdown("---")
            
    elif document_type == "Rencana Keperawatan":
        st.subheader("Generator Rencana Keperawatan")
        st.write("Hasilkan rencana keperawatan yang komprehensif.")
        
        description_label = "Deskripsi Pasien"
        description_help = "Masukkan detail lengkap tentang pasien, termasuk kondisi medis, gejala, dan informasi relevan lainnya untuk membuat rencana yang akurat."
        
        patient_description = st.text_area(
            description_label,
            height=200,
            help=description_help,
            placeholder="Contoh: Pasien laki-laki, 65 tahun, pasca stroke. Mengalami kesulitan menelan dan sering tersedak saat makan. Sering mengeluhkan tenggorokannya terasa 'tercekik'."
        )
        
        if st.button("Hasilkan Rencana Keperawatan Lengkap"):
            st.markdown("---")
            full_note = asyncio.run(generate_note_async(patient_description, nursing_care_plan_prompt_template, issues_list=nursing_diagnoses_list))
            st.subheader("Rencana Keperawatan Lengkap")
            st.text_area(
                "Salin teks di bawah:",
                value=full_note,
                height=500,
                help="Klik di dalam kotak teks, lalu gunakan Ctrl+C (atau Cmd+C) untuk menyalin."
            )
            st.markdown("---")


elif selected_role == "Konselor Adiksi":
    if document_type == "Catatan SOAP":
        st.subheader("Generator Catatan SOAP Konseling Adiksi")
        st.write("Buat catatan konseling berdasarkan isu-isu adiksi.")
        diagnoses_list = addiction_diagnoses_list
        prompt_template = addiction_prompt_template
        issue_label = "Pilih Isu Konseling Adiksi:"
        issue_help = "Pilih isu yang paling sesuai dengan kondisi klien."
        description_label = "Deskripsi Klien"
        description_help = "Masukkan detail tentang klien, seperti usia, latar belakang, dan riwayat penggunaan zat atau perilaku."

        selected_issue = st.selectbox(
            issue_label,
            options=diagnoses_list,
            help=issue_help
        )

        patient_description = st.text_area(
            description_label,
            height=150,
            help=description_help,
            placeholder="Contoh: Klien laki-laki, 25 tahun, memiliki riwayat penyalahgunaan opioid sejak 5 tahun lalu. Datang ke sesi dengan ekspresi cemas dan melaporkan kesulitan mengelola 'craving' saat menghadapi stres dari pekerjaan."
        )
        
        if st.button("Hasilkan Catatan SOAP Lengkap"):
            st.markdown("---")
            full_note = asyncio.run(generate_note_async(patient_description, prompt_template, issues_list=[selected_issue]))
            st.subheader("Catatan SOAP Lengkap")
            st.text_area(
                "Salin teks di bawah:",
                value=full_note,
                height=350,
                help="Klik di dalam kotak teks, lalu gunakan Ctrl+C (atau Cmd+C) untuk menyalin."
            )
            st.markdown("---")

    elif document_type == "Rencana Rawatan Adiksi":
        st.subheader("Generator Rencana Rawatan Adiksi")
        st.write("Hasilkan rencana rawatan komprehensif. AI akan mengidentifikasi isu konseling yang relevan dari daftar.")
        
        description_label = "Deskripsi Klien"
        description_help = "Masukkan detail lengkap tentang klien, termasuk riwayat adiksi, situasi hidup, dan informasi relevan lainnya untuk membuat rencana yang akurat."
        
        patient_description = st.text_area(
            description_label,
            height=200,
            help=description_help,
            placeholder="Contoh: Klien laki-laki, 30 tahun, lajang. Riwayat penyalahgunaan alkohol selama 10 tahun, mengalami kecanduan berat. Sudah berhenti selama 2 minggu. Klien memiliki dukungan keluarga yang kuat dan pekerjaan yang stabil. Namun, ia merasa cemas saat bersosialisasi dan takut kembali ke lingkungan lama yang memicu penggunaan."
        )

        if st.button("Hasilkan Rencana Rawatan Lengkap"):
            st.markdown("---")
            full_note = asyncio.run(generate_note_async(patient_description, treatment_plan_prompt_template, issues_list=addiction_diagnoses_list))
            st.subheader("Rencana Rawatan Lengkap")
            st.text_area(
                "Salin teks di bawah:",
                value=full_note,
                height=500,
                help="Klik di dalam kotak teks, lalu gunakan Ctrl+C (atau Cmd+C) untuk menyalin."
            )
            st.markdown("---")

st.markdown("---")
st.info("Aplikasi ini dibuat sebagai contoh. Isi catatan harus disesuaikan dengan kondisi spesifik klien dan diverifikasi oleh tenaga profesional.")
