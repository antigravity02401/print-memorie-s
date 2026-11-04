"""
Generate Rancangan Penelitian KSI DOCX from template.
Modifies a COPY of the original template, filling all sections.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import shutil
import os
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from copy import deepcopy
from lxml import etree

# Paths
TEMPLATE = r"c:\laragon\www\usaha\print memorie's\tugas\Metodologi Penelitian\Format Rancangan Penelitian KSI.docx"
OUTPUT = r"c:\laragon\www\usaha\print memorie's\tugas\Metodologi Penelitian\Rancangan_Penelitian_M_Arifin_Ilham.docx"

# Copy template
shutil.copy2(TEMPLATE, OUTPUT)

doc = Document(OUTPUT)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def set_paragraph_text_preserve_format(para, new_text):
    """Replace paragraph text while preserving the first run's formatting."""
    if para.runs:
        # Keep first run's format, clear others
        first_run = para.runs[0]
        for run in para.runs[1:]:
            run.text = ""
        first_run.text = new_text
    else:
        para.text = new_text

def add_text_to_single_cell_table(table, text, bold=False, font_name="Times New Roman", font_size=12):
    """Fill a single-cell table (1x1) with text content."""
    cell = table.rows[0].cells[0]
    # Clear existing paragraphs
    for p in cell.paragraphs:
        p.text = ""
    
    # Use the first paragraph
    para = cell.paragraphs[0]
    para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = para.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.bold = bold
    return para

def add_paragraphs_to_cell(cell, paragraphs_data):
    """Add multiple paragraphs to a cell. paragraphs_data is list of (text, bold, font_size)."""
    # Clear existing content
    for p in cell.paragraphs:
        p.text = ""
    
    first = True
    for text, bold, font_size in paragraphs_data:
        if first:
            para = cell.paragraphs[0]
            first = False
        else:
            para = cell.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        run = para.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(font_size)
        run.bold = bold

def replace_checkbox(para, from_char='\u2610', to_char='\u2611'):
    """Replace unchecked checkbox with checked in a paragraph's runs."""
    for run in para.runs:
        if from_char in run.text:
            run.text = run.text.replace(from_char, to_char)

# ============================================================================
# FILL HEADER INFO
# ============================================================================

# P4: Nama Lengkap
p4 = doc.paragraphs[4]
for run in p4.runs:
    if '\t: ' in run.text:
        run.text = '\t: M. Arifin Ilham'

# P5: NIM
p5 = doc.paragraphs[5]
for run in p5.runs:
    if '\t: ' in run.text:
        run.text = '\t: [NIM]'

# P6: Dosen Pembimbing
p6 = doc.paragraphs[6]
for run in p6.runs:
    if '\t: ' in run.text:
        run.text = '\t: Mansur'

# ============================================================================
# A. MINAT PENELITIAN - Check "3. Keamanan Aplikasi" and sub "Pengujian keamanan aplikasi web/mobile"
# ============================================================================

# P24: ☐ 3. Keamanan Aplikasi -> ☑
replace_checkbox(doc.paragraphs[24])

# P26: ☐ Pengujian keamanan aplikasi web/mobile -> ☑
replace_checkbox(doc.paragraphs[26])

# P34 is "Alasan:" - the content goes into Table 0 (the first single-cell table after Alasan)
alasan_text = (
    "Peneliti memilih bidang Keamanan Aplikasi dengan sub-minat pengujian keamanan aplikasi web/mobile "
    "karena aplikasi web Print Memorie\u2019s yang dikembangkan secara mandiri memproses data pribadi "
    "pengguna melalui form testimoni dan parameter URL tanpa mekanisme validasi input yang memadai. "
    "Kondisi ini berpotensi menjadi vektor serangan Cross-Site Scripting (XSS) dan SQL Injection (SQLi) "
    "yang dapat mengancam integritas dan kerahasiaan data. OWASP WSTG v4.2 menyediakan panduan pengujian "
    "terstruktur yang relevan untuk mengidentifikasi kerentanan input validation secara sistematis pada "
    "aplikasi web berskala kecil hingga menengah. Penelitian ini diharapkan menghasilkan rekomendasi "
    "perbaikan keamanan yang konkret dan dapat diimplementasikan langsung oleh pengembang."
)
add_text_to_single_cell_table(doc.tables[0], alasan_text)

# ============================================================================
# B. DRAF JUDUL PENELITIAN - Table 1
# ============================================================================
judul = (
    "Pengujian Keamanan Input Validation pada Aplikasi Web Undangan Digital "
    "Menggunakan Metode OWASP Web Security Testing Guide (WSTG) v4.2: "
    "Studi Kasus Print Memorie\u2019s"
)
add_text_to_single_cell_table(doc.tables[1], judul, bold=False, font_size=12)

# ============================================================================
# C. IDENTIFIKASI MASALAH - Table 2 (min 1000 words, min 10 citations)
# ============================================================================

identifikasi_masalah = """Perkembangan teknologi informasi dan komunikasi yang pesat telah mendorong transformasi digital di berbagai sektor kehidupan, termasuk dalam industri kreatif dan jasa. Salah satu manifestasi dari transformasi ini adalah munculnya platform undangan digital berbasis web yang menggantikan undangan cetak konvensional. Platform undangan digital menawarkan berbagai keunggulan seperti efisiensi biaya, kemudahan distribusi, personalisasi konten, serta interaktivitas yang lebih tinggi melalui fitur-fitur seperti konfirmasi kehadiran (RSVP), galeri foto, peta lokasi interaktif, dan kolom testimoni atau ucapan selamat [1]. Namun demikian, di balik kemudahan tersebut, terdapat tantangan keamanan siber yang serius dan sering kali terabaikan oleh para pengembang platform berskala kecil dan menengah.

Menurut laporan OWASP Foundation, kerentanan pada validasi input (input validation) secara konsisten menempati posisi teratas dalam daftar ancaman keamanan aplikasi web. OWASP Top 10 edisi terbaru mengidentifikasi bahwa serangan berbasis injeksi, termasuk Cross-Site Scripting (XSS) dan SQL Injection (SQLi), masih menjadi ancaman utama yang dihadapi oleh aplikasi web modern [2]. Cross-Site Scripting memungkinkan penyerang menyisipkan skrip berbahaya ke dalam halaman web yang kemudian dieksekusi oleh browser pengguna lain, sedangkan SQL Injection memungkinkan manipulasi query basis data untuk mengakses, memodifikasi, atau menghapus data secara tidak sah [3]. Kedua jenis serangan ini secara fundamental berakar pada kegagalan aplikasi dalam memvalidasi, membersihkan, dan menyaring input yang diterima dari pengguna.

Platform undangan digital Print Memorie\u2019s, yang menjadi objek studi kasus dalam penelitian ini, merupakan aplikasi web yang dikembangkan secara mandiri oleh peneliti untuk menyediakan layanan undangan pernikahan digital. Platform ini dibangun menggunakan teknologi HTML, CSS, JavaScript pada sisi klien, serta Vercel Serverless Functions dan basis data Neon PostgreSQL pada sisi server. Aplikasi ini menyediakan beberapa fitur utama, antara lain halaman arahan (landing page), formulir testimoni untuk tamu, endpoint API (POST /api/add-testimonial dan GET /api/get-testimonials), serta basis data PostgreSQL untuk menyimpan data testimoni. Selain itu, terdapat parameter URL untuk nama tamu dan fitur embed melalui iframe untuk mengintegrasikan undangan ke platform lain.

Berdasarkan pengamatan awal terhadap arsitektur aplikasi Print Memorie\u2019s, teridentifikasi beberapa area yang berpotensi menjadi titik masuk (attack surface) bagi serangan keamanan. Pertama, formulir testimoni menerima input teks dari pengguna tanpa mekanisme sanitasi atau validasi yang memadai, sehingga rentan terhadap serangan Stored XSS dan SQLi. Kedua, endpoint API tidak dilengkapi dengan mekanisme rate limiting, yang membuka peluang serangan brute force atau Denial of Service (DoS). Ketiga, parameter nama tamu pada URL berpotensi dimanfaatkan untuk serangan Reflected XSS. Keempat, penggunaan iframe untuk embed undangan dapat menjadi vektor serangan clickjacking jika tidak dikonfigurasi dengan header keamanan yang tepat.

Permasalahan ini semakin relevan mengingat data yang diproses oleh platform undangan digital mencakup informasi pribadi pengguna seperti nama, pesan ucapan, dan metadata kunjungan. Al Abdillah et al. [1] dalam penelitiannya mengenai sistem pengujian penetrasi otomatis berbasis Telegram yang mengacu pada PTES dan OWASP WSTG v4.2 menemukan bahwa pengujian keamanan terstruktur sangat efektif dalam mengidentifikasi kerentanan, dengan skor UAT mencapai 95,75% pada lima indikator kerentanan yang diuji. Penelitian tersebut menegaskan pentingnya adopsi kerangka kerja pengujian yang sistematis dalam mengevaluasi keamanan aplikasi web.

Kusdi et al. [2] melakukan analisis kerentanan pada aplikasi SIAKAD berbasis PHP menggunakan framework OWASP WSTG, Top 10, dan Risk Rating. Hasil penelitian mereka mengungkapkan sebanyak 26 kerentanan yang terdiri dari 7 kerentanan kritikal, 6 kerentanan tinggi, dan 13 kerentanan menengah. Temuan ini mengindikasikan bahwa aplikasi web yang dikembangkan oleh institusi pendidikan sekalipun memiliki kerentanan yang signifikan, apalagi aplikasi yang dikembangkan secara mandiri tanpa mengikuti prinsip secure development lifecycle. Utomo et al. [3] membandingkan efektivitas OWASP WSTG dengan Top 10 dalam audit keamanan web dan menyimpulkan bahwa WSTG lebih unggul dalam hal konsistensi dan presisi audit, menjadikannya pilihan yang lebih tepat sebagai panduan pengujian menyeluruh.

Pratama et al. [4] mengkaji identifikasi dan mitigasi kerentanan aplikasi web pada sistem kesehatan, menekankan pentingnya pendekatan secure-by-design yang diintegrasikan dengan pengujian keamanan berkelanjutan. Marpaung et al. [5] mengintegrasikan kerangka kerja manajemen risiko NIST 800-30 dengan pengujian penetrasi untuk menghasilkan penilaian risiko yang komprehensif beserta rekomendasi perbaikan. Kedua penelitian ini menunjukkan tren peningkatan kesadaran akan pentingnya pengujian keamanan yang terstruktur dan berbasis standar internasional.

Hidayanto et al. [6] mengembangkan pemetaan otomatis WSTG untuk mempercepat proses pengujian penetrasi, menunjukkan bahwa adopsi WSTG secara sistematis dapat meningkatkan efisiensi dan cakupan pengujian keamanan. Yusuf et al. [7] melakukan pengujian keamanan menggunakan ISSAF dan OWASP WSTG v4.2 pada aplikasi web pemerintahan, mengkonfirmasi bahwa kombinasi metodologi pengujian dapat memberikan hasil evaluasi yang lebih komprehensif. Penelitian-penelitian terdahulu ini secara kolektif menunjukkan bahwa kerangka kerja OWASP WSTG v4.2 merupakan panduan yang efektif dan terstruktur untuk pengujian keamanan aplikasi web.

Dalam konteks pengujian keamanan input validation secara spesifik, penelitian oleh sejumlah akademisi telah mendokumentasikan bahwa serangan XSS dan SQLi merupakan konsekuensi langsung dari kegagalan validasi input. Analisis keamanan website terhadap serangan SQL Injection dan XSS [8] menunjukkan bahwa platform layanan digital memiliki celah keamanan pada bagian validasi input yang memerlukan penanganan melalui penggunaan prepared statements dan fungsi encoding kontekstual seperti htmlspecialchars(). Pengujian keamanan aplikasi web terhadap serangan SQL Injection menggunakan SQLMap [9] mengkonfirmasi kerentanan boolean-based blind dan error-based SQL Injection pada aplikasi yang tidak menerapkan pemfilteran input pada backend.

Evaluasi keamanan aplikasi web yang mengintegrasikan OWASP dengan CVSS [10] memberikan kerangka penilaian kuantitatif yang memungkinkan penentuan prioritas perbaikan berdasarkan tingkat keparahan kerentanan. Pendekatan VAPT berbasis OWASP Top Ten [11] memetakan kerentanan web ke dalam skor CVE, CWE, dan CVSS untuk remediasi yang presisi. Sementara itu, penelitian mengenai pengamanan aplikasi web terhadap serangan SQL Injection dan XSS menggunakan pendekatan berbasis machine learning [12] menunjukkan keterbatasan Web Application Firewall (WAF) tradisional dalam menangani payload yang diobfuskasi, yang mengindikasikan pentingnya validasi input pada level aplikasi sebagai lapisan pertahanan pertama.

Berdasarkan uraian permasalahan di atas, dapat diidentifikasi bahwa aplikasi web undangan digital Print Memorie\u2019s memiliki potensi kerentanan keamanan pada aspek input validation yang belum pernah diuji secara sistematis menggunakan kerangka kerja yang terstandar. Kondisi ini menimbulkan risiko terhadap integritas, kerahasiaan, dan ketersediaan data pengguna. Oleh karena itu, diperlukan pengujian keamanan yang komprehensif dan terstruktur menggunakan OWASP WSTG v4.2 untuk mengidentifikasi, menganalisis, dan memberikan rekomendasi perbaikan terhadap kerentanan yang ditemukan.

Berdasarkan identifikasi masalah tersebut, rumusan masalah dalam penelitian ini adalah sebagai berikut:
1. Kerentanan input validation apa saja yang terdapat pada aplikasi web undangan digital Print Memorie\u2019s berdasarkan pengujian menggunakan OWASP WSTG v4.2?
2. Bagaimana tingkat keparahan (severity) setiap kerentanan yang ditemukan berdasarkan penilaian Common Vulnerability Scoring System (CVSS) v3.1?
3. Rekomendasi perbaikan apa yang dapat diberikan untuk mengatasi kerentanan input validation yang ditemukan pada aplikasi web Print Memorie\u2019s?

Adapun tujuan penelitian ini adalah:
1. Mengidentifikasi kerentanan input validation pada aplikasi web undangan digital Print Memorie\u2019s menggunakan metode pengujian OWASP WSTG v4.2.
2. Menganalisis tingkat keparahan setiap kerentanan yang ditemukan menggunakan metrik penilaian CVSS v3.1.
3. Menyusun rekomendasi perbaikan keamanan yang konkret dan dapat diimplementasikan untuk mengatasi kerentanan input validation pada aplikasi web Print Memorie\u2019s."""

add_text_to_single_cell_table(doc.tables[2], identifikasi_masalah.strip(), font_size=12)

# ============================================================================
# D.1 PENELITIAN TERDAHULU - Table 3 (6 cols, header + 5 data rows)
# ============================================================================

penelitian_terdahulu = [
    {
        "ref": "[1]",
        "penulis": "I.R. Al Abdillah, I.R. Hikmah, R. Purwoko, Arizal (2026)",
        "objek": "Sistem pengujian penetrasi otomatis berbasis Telegram, Poltek SSN",
        "metode": "PTES dan OWASP WSTG v4.2, pengujian otomatis 5 indikator kerentanan",
        "hasil": "Sistem berhasil mengotomasi pengujian penetrasi dengan skor UAT 95,75%",
        "keterbatasan": "Terbatas pada 5 indikator kerentanan WSTG; belum mencakup seluruh kategori pengujian WSTG v4.2"
    },
    {
        "ref": "[2]",
        "penulis": "I. Kusdi, D.A. Haryanti, Hustinawaty (2026)",
        "objek": "Aplikasi SIAKAD berbasis PHP, Universitas Gunadarma",
        "metode": "OWASP WSTG, Top 10, dan Risk Rating",
        "hasil": "Ditemukan 26 kerentanan: 7 kritikal, 6 tinggi, 13 menengah",
        "keterbatasan": "Fokus pada aplikasi berbasis PHP tradisional; belum menguji arsitektur serverless atau JAMstack"
    },
    {
        "ref": "[3]",
        "penulis": "M.W.S. Utomo, H.E. Wahanani, A. Junaidi (2026)",
        "objek": "Perbandingan metode audit keamanan web",
        "metode": "Komparasi OWASP WSTG vs. Top 10",
        "hasil": "WSTG lebih unggul dalam konsistensi dan presisi audit dibanding Top 10",
        "keterbatasan": "Bersifat komparatif teoritis; belum divalidasi pada studi kasus aplikasi web spesifik"
    },
    {
        "ref": "[6]",
        "penulis": "B.C. Hidayanto, I.A. Akbar, A.Z.D. Putra (2024)",
        "objek": "Pemetaan otomatis WSTG untuk pengujian penetrasi",
        "metode": "Automated mapping OWASP WSTG",
        "hasil": "Pemetaan otomatis meningkatkan efisiensi dan cakupan proses pengujian penetrasi",
        "keterbatasan": "Belum menguji efektivitas pada aplikasi dengan arsitektur modern (SPA, serverless)"
    },
    {
        "ref": "[7]",
        "penulis": "M.F. Yusuf, I.R. Hikmah, Amiruddin, S.U. Sunaringtyas (2025)",
        "objek": "Aplikasi web pemerintahan (Website XYZ)",
        "metode": "ISSAF dan OWASP WSTG v4.2",
        "hasil": "Kombinasi ISSAF dan WSTG memberikan evaluasi keamanan yang lebih komprehensif",
        "keterbatasan": "Objek terbatas pada satu aplikasi pemerintahan; belum menguji aplikasi komersial atau platform digital kecil"
    }
]

table3 = doc.tables[3]
for i, data in enumerate(penelitian_terdahulu):
    row = table3.rows[i + 1]  # Skip header row
    cells = row.cells
    
    for cell in cells:
        for p in cell.paragraphs:
            p.text = ""
    
    fields = ["ref", "penulis", "objek", "metode", "hasil", "keterbatasan"]
    for j, field in enumerate(fields):
        para = cells[j].paragraphs[0]
        run = para.add_run(data[field])
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)

# ============================================================================
# D.2 POSISI PENELITIAN - Table 4 (min 200 words)
# ============================================================================

posisi_penelitian = """Berdasarkan kajian terhadap lima penelitian terdahulu pada tabel D.1, dapat diidentifikasi beberapa celah penelitian (research gap) yang belum terisi. Pertama, dari segi objek penelitian, seluruh penelitian terdahulu menguji aplikasi web berbasis arsitektur monolitik tradisional (PHP, server-side rendering) atau membandingkan metode secara teoretis. Belum ada penelitian yang secara spesifik menguji keamanan input validation pada aplikasi web dengan arsitektur modern berbasis serverless functions dan database cloud (Neon PostgreSQL) yang di-deploy pada platform edge computing seperti Vercel. Arsitektur ini memiliki karakteristik keamanan yang berbeda dari arsitektur tradisional, khususnya dalam hal penanganan request, koneksi database, dan pengelolaan environment variables.

Kedua, dari segi konteks aplikasi, belum ditemukan penelitian yang mengkaji keamanan aplikasi undangan digital secara spesifik. Platform undangan digital memiliki keunikan attack surface tersendiri, seperti parameter URL untuk personalisasi nama tamu, formulir testimoni publik yang memungkinkan Stored XSS, dan API endpoint tanpa autentikasi yang rentan terhadap penyalahgunaan.

Ketiga, dari segi kedalaman pengujian, sebagian besar penelitian terdahulu berfokus pada pengujian kerentanan secara umum berdasarkan OWASP Top 10. Penelitian ini akan lebih berfokus pada kategori pengujian input validation secara mendalam menggunakan test case spesifik dari OWASP WSTG v4.2, yaitu WSTG-INPV (Input Validation Testing), yang mencakup pengujian Reflected XSS, Stored XSS, SQL Injection, HTTP Parameter Pollution, dan validasi input pada sisi klien maupun server.

Dengan demikian, penelitian ini mengisi celah dengan menjadi studi pertama yang menerapkan pengujian input validation berbasis OWASP WSTG v4.2 pada aplikasi undangan digital berarsitektur serverless, dengan penilaian severity menggunakan CVSS v3.1, serta menghasilkan rekomendasi perbaikan yang langsung dapat diimplementasikan oleh pengembang."""

add_text_to_single_cell_table(doc.tables[4], posisi_penelitian.strip(), font_size=12)

# ============================================================================
# D.3 LANDASAN TEORI - Table 5 (min 3 concepts)
# ============================================================================

landasan_teori = """1. OWASP Web Security Testing Guide (WSTG) v4.2

OWASP Web Security Testing Guide (WSTG) merupakan panduan komprehensif yang diterbitkan oleh Open Web Application Security Project (OWASP) Foundation untuk melakukan pengujian keamanan aplikasi web secara sistematis dan terstruktur [1][3]. WSTG v4.2 adalah versi terbaru yang menyediakan kerangka kerja pengujian yang terdiri dari beberapa kategori utama, antara lain Information Gathering, Configuration and Deployment Management Testing, Identity Management Testing, Authentication Testing, Authorization Testing, Session Management Testing, Input Validation Testing, Error Handling Testing, Cryptography Testing, Business Logic Testing, dan Client-Side Testing [6]. Kategori Input Validation Testing (WSTG-INPV) secara spesifik mencakup pengujian terhadap berbagai jenis serangan berbasis input, termasuk Reflected Cross-Site Scripting (WSTG-INPV-01), Stored Cross-Site Scripting (WSTG-INPV-02), HTTP Verb Tampering (WSTG-INPV-03), HTTP Parameter Pollution (WSTG-INPV-04), dan SQL Injection (WSTG-INPV-05). Panduan ini menjadi acuan utama dalam penelitian ini untuk merancang dan melaksanakan skenario pengujian keamanan input validation pada aplikasi web Print Memorie\u2019s.

2. Common Vulnerability Scoring System (CVSS) v3.1

Common Vulnerability Scoring System (CVSS) adalah sistem penilaian kerentanan standar industri yang dikembangkan oleh Forum of Incident Response and Security Teams (FIRST) untuk memberikan skor numerik yang merepresentasikan tingkat keparahan kerentanan keamanan [10]. CVSS v3.1 menggunakan tiga kelompok metrik: Base Score yang mengukur karakteristik intrinsik kerentanan (Attack Vector, Attack Complexity, Privileges Required, User Interaction, Scope, Confidentiality Impact, Integrity Impact, Availability Impact), Temporal Score yang mencerminkan karakteristik kerentanan yang berubah seiring waktu, dan Environmental Score yang menyesuaikan penilaian dengan lingkungan pengguna tertentu [11]. Skor CVSS berkisar dari 0.0 hingga 10.0 dengan klasifikasi: None (0.0), Low (0.1-3.9), Medium (4.0-6.9), High (7.0-8.9), dan Critical (9.0-10.0). Dalam penelitian ini, CVSS v3.1 digunakan untuk menilai dan memprioritaskan tingkat keparahan setiap kerentanan yang ditemukan pada proses pengujian.

3. Cross-Site Scripting (XSS) dan SQL Injection (SQLi)

Cross-Site Scripting (XSS) adalah kerentanan keamanan yang memungkinkan penyerang menyuntikkan skrip sisi klien (client-side script) ke dalam halaman web yang dilihat oleh pengguna lain [8]. Terdapat tiga jenis utama XSS: Reflected XSS di mana payload berbahaya dikirim melalui parameter HTTP dan langsung dikembalikan oleh server dalam respons, Stored XSS di mana payload disimpan secara permanen di server (misalnya dalam basis data) dan dieksekusi setiap kali halaman yang mengandung payload tersebut diakses, serta DOM-based XSS di mana kerentanan terjadi pada sisi klien melalui manipulasi Document Object Model [3]. SQL Injection (SQLi) adalah teknik serangan yang mengeksploitasi kerentanan pada lapisan basis data aplikasi melalui penyisipan atau manipulasi perintah SQL pada input yang dikirimkan pengguna ke aplikasi [9]. Serangan SQLi dapat mengakibatkan pengungkapan data sensitif (data breach), modifikasi atau penghapusan data, eksekusi perintah administratif pada basis data, dan dalam kasus tertentu, pengambilalihan server. Kedua jenis serangan ini merupakan konsekuensi langsung dari kegagalan implementasi validasi input yang memadai dan menjadi fokus utama pengujian dalam penelitian ini."""

add_text_to_single_cell_table(doc.tables[5], landasan_teori.strip(), font_size=12)

# ============================================================================
# E.1 ALTERNATIF SOLUSI - Table 6
# ============================================================================

alternatif_solusi = """Untuk menyelesaikan permasalahan keamanan input validation pada aplikasi web Print Memorie\u2019s, terdapat beberapa alternatif solusi yang dapat dipertimbangkan:

1. Pengujian keamanan menggunakan OWASP Web Security Testing Guide (WSTG) v4.2: Melakukan pengujian keamanan secara sistematis berdasarkan panduan WSTG v4.2, khususnya pada kategori Input Validation Testing (WSTG-INPV). Pendekatan ini menyediakan test case yang terstruktur dan komprehensif untuk mengidentifikasi kerentanan XSS, SQLi, dan validasi input lainnya [1][3].

2. Pengujian keamanan menggunakan OWASP Testing Guide dikombinasikan dengan ISSAF (Information Systems Security Assessment Framework): Mengkombinasikan dua kerangka kerja pengujian untuk mendapatkan cakupan yang lebih luas. ISSAF menyediakan panduan yang lebih detail pada fase pengumpulan informasi dan eksploitasi, sementara WSTG lebih berfokus pada pengujian keamanan aplikasi [7].

3. Vulnerability Assessment and Penetration Testing (VAPT) berbasis OWASP Top 10: Melakukan pengujian keamanan yang berfokus pada sepuluh risiko keamanan teratas menurut OWASP, mencakup proses pengumpulan informasi, pemindaian, eksploitasi, dan pelaporan [11].

4. Pengujian keamanan otomatis menggunakan alat pemindaian kerentanan (Automated Security Scanning): Menggunakan alat pemindaian otomatis seperti OWASP ZAP, Burp Suite, atau Nikto untuk melakukan pemindaian kerentanan secara otomatis tanpa panduan pengujian manual yang terstruktur."""

add_text_to_single_cell_table(doc.tables[6], alternatif_solusi.strip(), font_size=12)

# ============================================================================
# E.2 SOLUSI YANG DIPILIH - Table 7 (min 300 words)
# ============================================================================

solusi_dipilih = """Dari keempat alternatif solusi yang diidentifikasi, penelitian ini memilih alternatif pertama, yaitu pengujian keamanan menggunakan OWASP Web Security Testing Guide (WSTG) v4.2 dengan fokus pada kategori Input Validation Testing, yang dikombinasikan dengan penilaian tingkat keparahan kerentanan menggunakan Common Vulnerability Scoring System (CVSS) v3.1.

Pemilihan OWASP WSTG v4.2 sebagai metode utama didasarkan pada beberapa pertimbangan. Pertama, WSTG v4.2 merupakan panduan pengujian keamanan yang paling komprehensif dan terstruktur yang tersedia secara terbuka (open-source), sehingga dapat diakses dan direplikasi oleh peneliti manapun [1][6]. Tidak seperti OWASP Top 10 yang hanya mengidentifikasi sepuluh risiko teratas secara umum, WSTG menyediakan prosedur pengujian yang spesifik dan langkah-demi-langkah (step-by-step) untuk setiap kategori kerentanan, sehingga memberikan konsistensi dan presisi yang lebih tinggi dalam proses pengujian [3].

Kedua, kategori Input Validation Testing (WSTG-INPV) dalam WSTG v4.2 secara langsung berkaitan dengan permasalahan yang diidentifikasi pada aplikasi Print Memorie\u2019s, yaitu kerentanan pada formulir testimoni, API endpoint, dan parameter URL. Kategori ini mencakup test case untuk Reflected XSS, Stored XSS, SQL Injection, HTTP Parameter Pollution, dan berbagai jenis validasi input lainnya yang sangat relevan dengan attack surface aplikasi target [2][8].

Ketiga, kombinasi dengan CVSS v3.1 memungkinkan penilaian kuantitatif terhadap setiap kerentanan yang ditemukan, sehingga rekomendasi perbaikan dapat diprioritaskan berdasarkan tingkat keparahan (severity). Pendekatan ini telah terbukti efektif dalam penelitian-penelitian terdahulu untuk menghasilkan laporan pengujian keamanan yang actionable [10][11].

Keempat, dibandingkan dengan alternatif kedua (kombinasi WSTG+ISSAF), penggunaan WSTG secara mandiri sudah cukup komprehensif untuk lingkup pengujian input validation dan lebih efisien dalam hal waktu pelaksanaan. Dibandingkan dengan alternatif ketiga (VAPT berbasis Top 10), WSTG menawarkan kedalaman pengujian yang lebih baik pada aspek input validation. Dibandingkan dengan alternatif keempat (automated scanning), pengujian berbasis WSTG memberikan pemahaman kontekstual yang lebih mendalam terhadap kerentanan yang ditemukan, memungkinkan identifikasi kerentanan logis yang tidak dapat dideteksi oleh alat otomatis, serta menghasilkan rekomendasi perbaikan yang lebih spesifik dan kontekstual terhadap arsitektur aplikasi target.

Dengan demikian, solusi ini menjawab rumusan masalah secara langsung: WSTG v4.2 menyediakan prosedur untuk mengidentifikasi kerentanan (RQ1), CVSS v3.1 menyediakan metrik untuk menilai tingkat keparahan (RQ2), dan kombinasi keduanya menghasilkan dasar yang kuat untuk menyusun rekomendasi perbaikan (RQ3)."""

add_text_to_single_cell_table(doc.tables[7], solusi_dipilih.strip(), font_size=12)

# ============================================================================
# F. RENCANA METODE - Table 8 (max 300 words)
# ============================================================================

rencana_metode = """Penelitian ini menggunakan metode penelitian kualitatif deskriptif dengan pendekatan studi kasus. Objek penelitian adalah aplikasi web undangan digital Print Memorie\u2019s yang diakses melalui URL print-memorie-s-two.vercel.app. Tahapan penelitian terdiri dari empat fase utama.

Fase pertama adalah pengumpulan informasi (information gathering), yang mencakup identifikasi teknologi yang digunakan, pemetaan arsitektur aplikasi, enumerasi endpoint API, dan analisis kode sumber untuk memahami mekanisme penanganan input pada sisi klien dan server.

Fase kedua adalah perancangan skenario pengujian berdasarkan OWASP WSTG v4.2 kategori Input Validation Testing (WSTG-INPV). Skenario pengujian mencakup: WSTG-INPV-01 (Reflected XSS) pada parameter URL nama tamu, WSTG-INPV-02 (Stored XSS) pada formulir testimoni dan API POST, WSTG-INPV-05 (SQL Injection) pada API endpoint yang berinteraksi dengan basis data PostgreSQL, serta WSTG-INPV-04 (HTTP Parameter Pollution) pada parameter request.

Fase ketiga adalah pelaksanaan pengujian menggunakan kombinasi pengujian manual dan alat bantu. Alat yang digunakan meliputi: browser web (Chrome DevTools) untuk inspeksi dan manipulasi request, Burp Suite Community Edition untuk intercepting proxy dan payload injection, SQLMap untuk pengujian otomatis SQL Injection, serta OWASP ZAP sebagai vulnerability scanner tambahan. Setiap kerentanan yang ditemukan akan dinilai menggunakan CVSS v3.1 Calculator dari FIRST.

Fase keempat adalah analisis hasil dan penyusunan rekomendasi. Data hasil pengujian dianalisis secara deskriptif untuk mengidentifikasi pola kerentanan, menentukan akar penyebab, dan menyusun rekomendasi perbaikan teknis yang dapat diimplementasikan. Status izin etik pengujian sudah terpenuhi karena aplikasi merupakan milik peneliti sendiri."""

add_text_to_single_cell_table(doc.tables[8], rencana_metode.strip(), font_size=12)

# ============================================================================
# G. RENCANA HASIL - Table 9
# ============================================================================

rencana_hasil = """Penelitian ini direncanakan menghasilkan luaran sebagai berikut:

Artefak dan Produk:
1. Laporan hasil pengujian keamanan input validation yang mencakup daftar kerentanan yang ditemukan, bukti eksploitasi (proof of concept) untuk setiap kerentanan, serta skor CVSS v3.1 untuk setiap temuan.
2. Matriks pemetaan kerentanan terhadap test case OWASP WSTG v4.2 kategori WSTG-INPV, yang menunjukkan status setiap pengujian (vulnerable, not vulnerable, not applicable).
3. Dokumen rekomendasi perbaikan teknis yang berisi langkah-langkah konkret untuk mengatasi setiap kerentanan yang ditemukan, meliputi perbaikan pada validasi input sisi klien, sanitasi input sisi server, konfigurasi header keamanan HTTP, implementasi parameterized queries, dan penerapan rate limiting pada API endpoint.
4. Proof of concept (PoC) kode perbaikan untuk kerentanan kritis dan tinggi yang ditemukan.

Luaran Akademik:
1. Laporan skripsi atau Proyek Akhir yang disusun sesuai dengan pedoman penulisan karya ilmiah Program Studi Sarjana Terapan Keamanan Sistem Informasi.
2. Naskah artikel jurnal yang ditargetkan untuk dipublikasikan pada jurnal nasional terakreditasi SINTA di bidang keamanan informasi atau teknologi informasi."""

add_text_to_single_cell_table(doc.tables[9], rencana_hasil.strip(), font_size=12)

# ============================================================================
# H. DAFTAR PUSTAKA - Table 10 (IEEE style)
# ============================================================================

daftar_pustaka = """[1]  I. R. Al Abdillah, I. R. Hikmah, R. Purwoko, dan Arizal, "Development of a Telegram-Based Automated Penetration Testing System Based on PTES and OWASP WSTG Version 4.2," JUTIF, vol. 7, no. 5, hlm. 4756\u20134767, 2026, doi: 10.52436/1.jutif.2026.7.5.5738.

[2]  I. Kusdi, D. A. Haryanti, dan Hustinawaty, "Analisis Kerentanan Aplikasi Berbasis Web Menggunakan Framework OWASP WSTG, Top 10 dan Risk Rating," JII, vol. 5, no. 5, 2026, doi: 10.58344/jii.v5i5.7722.

[3]  M. W. S. Utomo, H. E. Wahanani, dan A. Junaidi, "Comparative Effectiveness of OWASP WSTG and Top Ten in Web Security Audits," bit-Tech, 2026.

[4]  S. D. Pratama, A. T. J. Harjanto, dan B. Herlambang, "Identification and Mitigation of Web Application Vulnerabilities in Healthcare Systems," Journal of Applied Informatics and Computing, Jun. 2026.

[5]  Y. D. Marpaung et al., "Integrating the NIST 800-30 Risk Management Framework with Penetration Testing," Indonesian Journal of Information Systems, Agu. 2026.

[6]  B. C. Hidayanto, I. A. Akbar, dan A. Z. D. Putra, "Automated Web Security Testing Guide Mapping to Accelerate Process on Penetration Testing," Procedia Computer Science, vol. 234, hlm. 1412\u20131419, 2024, doi: 10.1016/j.procs.2024.03.140.

[7]  M. F. Yusuf, I. R. Hikmah, Amiruddin, dan S. U. Sunaringtyas, "Security Testing of XYZ Website Application Using ISSAF and OWASP WSTG v4.2 Methods," Teknika, vol. 14, no. 1, 2025, doi: 10.34148/teknika.v14i1.1156.

[8]  Anonim, "Analisis Keamanan Website E-Pinter Terhadap Serangan SQL Injection dan XSS," JUPTI, vol. 4, no. 3, 2024, doi: 10.55606/jupti.v4i3.5234.

[9]  Anonim, "Web Application Security Testing Against SQL Injection Attacks Using SQL Map," e-Komtek, vol. 9, no. 2, 2025, doi: 10.37339/e-komtek.v9i2.2260.

[10] Anonim, "Security Analysis of Web-based Information Systems Using OWASP and CVSS," Journal of Informatics and Vocational Education, vol. 7, no. 3, 2024, doi: 10.20961/joive.v7i3.2411.

[11] Anonim, "Enhancing Website Security Using Vulnerability Assessment and Penetration Testing (VAPT) Based on OWASP Top Ten," Journal of Applied Informatics and Computing, vol. 9, no. 2, 2025, doi: 10.30871/jaic.v9i2.9069.

[12] Anonim, "Securing Web Applications Against SQL Injection and XSS Attacks," International Journal of Latest Technology in Engineering, Management and Applied Science, 2025, doi: 10.51583/IJLTEMAS.2025.140500025."""

add_text_to_single_cell_table(doc.tables[10], daftar_pustaka.strip(), font_size=12)

# ============================================================================
# SAVE
# ============================================================================

doc.save(OUTPUT)
print(f"Document saved to: {OUTPUT}")
print("Done!")
