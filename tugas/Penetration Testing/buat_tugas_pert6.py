"""
Script untuk mengisi Lembar Kerja Individu Penetration Testing Pertemuan 6
Topik: Scanning, Enumeration, dan Threat Modeling
Nama: M. Arifin Ilham | NIM: 6404240008 | Kelas: KSI 5A
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ─── Helpers ────────────────────────────────────────────────────────────────

def set_cell_bg(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)

def set_borders(cell, color="2B5BA8"):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for side in ["top", "left", "bottom", "right"]:
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single")
        b.set(qn("w:sz"), "4")
        b.set(qn("w:space"), "0")
        b.set(qn("w:color"), color)
        tcBorders.append(b)
    tcPr.append(tcBorders)

def cell_text(cell, text, bold=False, size=9, color=None, align=WD_ALIGN_PARAGRAPH.LEFT):
    p = cell.paragraphs[0]
    p.alignment = align
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = "Times New Roman"
    if color:
        r.font.color.rgb = RGBColor(*bytes.fromhex(color))
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def section_heading(doc, letter, title, color="1F3D7A"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"), "single")
    bot.set(qn("w:sz"), "6")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), "2B5BA8")
    pBdr.append(bot)
    pPr.append(pBdr)
    r = p.add_run(f"{letter}. {title}")
    r.bold = True
    r.font.size = Pt(11)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(*bytes.fromhex(color))

def sub_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(10)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0x2B, 0x5B, 0xA8)

def warning_box(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Catatan Kepatuhan: ")
    r.bold = True
    r.font.size = Pt(9)
    r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0xB7, 0x15, 0x00)
    r2 = p.add_run(text)
    r2.font.size = Pt(9)
    r2.font.name = "Times New Roman"

def build_table(doc, headers, rows, col_widths_cm,
                header_bg="1F3D7A", even_bg="F0F4FF", odd_bg="FFFFFF",
                first_col_bg="D0DAF0", font_size=9):
    tbl = doc.add_table(rows=len(rows)+1, cols=len(headers))
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for row in tbl.rows:
        for i, cell in enumerate(row.cells):
            if i < len(col_widths_cm):
                cell.width = Cm(col_widths_cm[i])
    for cell, hdr in zip(tbl.rows[0].cells, headers):
        set_cell_bg(cell, header_bg)
        set_borders(cell, "FFFFFF")
        cell_text(cell, hdr, bold=True, size=font_size, color="FFFFFF",
                  align=WD_ALIGN_PARAGRAPH.CENTER)
    for ri, row_data in enumerate(rows):
        bg = even_bg if ri % 2 == 0 else odd_bg
        for ci, (cell, txt) in enumerate(zip(tbl.rows[ri+1].cells, row_data)):
            set_cell_bg(cell, first_col_bg if ci == 0 else bg)
            set_borders(cell)
            cell_text(cell, str(txt), bold=(ci == 0), size=font_size)
    doc.add_paragraph()
    return tbl

# ─── Header Kop ─────────────────────────────────────────────────────────────

def add_header(doc):
    data = [
        ("KEMENTERIAN PENDIDIKAN, TINGGI, SAINS, DAN TEKNOLOGI", 10, True),
        ("POLITEKNIK NEGERI BENGKALIS", 12, True),
        ("Jalan Bathin Alam, Sungai Alam, Bengkalis, Riau 28711", 10, False),
        ("Telepon: (+62766) 24566  |  Fax: (+62766) 800 1000  |  www.polbeng.ac.id", 9, False),
    ]
    for txt, sz, bold in data:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.bold = bold
        r.font.size = Pt(sz)
        r.font.name = "Times New Roman"
    # divider line
    p5 = doc.add_paragraph()
    p5.paragraph_format.space_before = Pt(3)
    p5.paragraph_format.space_after = Pt(3)
    pPr = p5._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bot = OxmlElement("w:bottom")
    bot.set(qn("w:val"), "single")
    bot.set(qn("w:sz"), "12")
    bot.set(qn("w:space"), "1")
    bot.set(qn("w:color"), "1F3D7A")
    pBdr.append(bot)
    pPr.append(pBdr)

# ─── Title Block ─────────────────────────────────────────────────────────────

def add_title(doc):
    doc.add_paragraph()
    titles = [
        ("LEMBAR KERJA PRAKTIKUM INDIVIDU", 13, True, "1F3D7A"),
        ("PENETRATION TESTING", 13, True, "1F3D7A"),
        ("Pertemuan 6: Scanning, Enumeration, dan Threat Modeling", 11, True, "2B5BA8"),
        ("Program Studi Sarjana Terapan Keamanan Sistem Informasi - Politeknik Negeri Bengkalis", 9, False, "444444"),
    ]
    for txt, sz, bold, color in titles:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(txt)
        r.bold = bold
        r.font.size = Pt(sz)
        r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(*bytes.fromhex(color))
    doc.add_paragraph()
    # Identitas
    ident = [
        ("Nama", "M. Arifin Ilham"),
        ("NIM", "6404240008"),
        ("Kelas", "KSI 5A"),
        ("Tanggal Praktik", "09/10/2026"),
        ("Target Web", "https://nyamankost.ours.web.id"),
    ]
    tbl = doc.add_table(rows=5, cols=2)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (k, v) in enumerate(ident):
        kc = tbl.rows[i].cells[0]
        vc = tbl.rows[i].cells[1]
        kc.width = Cm(4)
        vc.width = Cm(11)
        set_cell_bg(kc, "E8EDF7")
        set_borders(kc)
        set_borders(vc)
        cell_text(kc, k, bold=True, size=10)
        cell_text(vc, v, size=10)
    doc.add_paragraph()

# ─── A. Tujuan ───────────────────────────────────────────────────────────────

def add_tujuan(doc):
    section_heading(doc, "A", "Tujuan Praktikum")
    for t in [
        "Melakukan scanning dan enumeration secara terkendali pada target web riil yang berizin.",
        "Mencatat evidence yang dapat ditelusuri.",
        "Menyusun threat model dan prioritas pengujian berdasarkan hasil recon.",
    ]:
        p = doc.add_paragraph(style="List Bullet")
        r = p.add_run(t)
        r.font.size = Pt(10)
        r.font.name = "Times New Roman"

# ─── B. Verifikasi Scope ─────────────────────────────────────────────────────

def add_scope(doc):
    section_heading(doc, "B", "Verifikasi Scope")
    p = doc.add_paragraph()
    r = p.add_run("Sumber: RoE Pentest KSI 5A 2026.pdf - ditandatangani 25/09/2026")
    r.font.size = Pt(9)
    r.font.name = "Times New Roman"
    r.italic = True
    rows = [
        ("Bukti Izin", "RoE Pentest KSI 5A 2026.pdf - Revis Irwan Gea (Tim Pengembang), Nurmi Hidayasari (Dosen), M. Arifin Ilham (Pelaksana). Tanggal: 25/09/2026."),
        ("Domain/URL in-scope", "https://nyamankost.ours.web.id - hanya lapisan aplikasi web (HTTP/HTTPS). RoE Bagian 4."),
        ("IP in-scope", "Tidak ditetapkan eksplisit. DNS: 104.21.92.41 & 172.67.186.51 (Cloudflare anycast). Port scanning ke IP/domain DILARANG per RoE Bagian 5."),
        ("Out-of-scope", "Lapisan jaringan/infrastruktur/server; eksploitasi OS/server; aksi destruktif; social engineering; port scanning/Nmap terhadap domain/IP target."),
        ("Waktu Pengujian", "Minggu 3 s.d. Minggu 12 mengikuti jadwal praktikum. Tidak ada jendela waktu wajib dihindari (belum ada mitra yang bergantung pada uptime)."),
        ("Rate/Concurrency Limit", "Tidak ditetapkan eksplisit dalam RoE. Mengikuti batas wajar agar tidak mengganggu pengguna lain di server shared hosting."),
        ("Metode yang Dilarang", "Port scanning/Nmap; eksploitasi tingkat OS/server; menghapus/mengubah data permanen; social engineering; publikasi data/kredensial di luar keperluan akademik."),
        ("Kontak Penghentian", "Nurmi Hidayasari (Dosen): 0811-7500-891  |  Revis Irwan Gea (Tim Pengembang): 0812-6534-2848"),
    ]
    build_table(doc, ["Item Scope", "Jawaban / Bukti"], rows,
                col_widths_cm=[4.5, 12], font_size=9)

# ─── C. Log Aktivitas ────────────────────────────────────────────────────────

def add_log(doc):
    section_heading(doc, "C", "Log Aktivitas")
    rows = [
        ("1", "09:37:03", "https://nyamankost.ours.web.id", "HTTP Baseline (HTTPS)", "curl -I https://nyamankost.ours.web.id", "HTTP/2 200, server: cloudflare, PHP/8.5.11, XSRF-TOKEN cookie"),
        ("2", "09:39:03", "http://nyamankost.ours.web.id", "Cek Redirect HTTP ke HTTPS", "curl -I http://nyamankost.ours.web.id", "301 Moved Permanently ke https://nyamankost.ours.web.id/"),
        ("3", "~09:40", "https://nyamankost.ours.web.id", "Fingerprinting teknologi", "whatweb https://nyamankost.ours.web.id", "Cloudflare, PHP 8.5.11, HTML5, IP 104.21.92.41, cookies"),
        ("4", "~09:45", ".../robots.txt", "Enumerasi robots.txt", "curl https://nyamankost.ours.web.id/robots.txt", "User-agent: * / Disallow: (kosong - tidak ada path diblokir)"),
        ("5", "~09:46", ".../sitemap.xml", "Enumerasi sitemap.xml", "curl https://nyamankost.ours.web.id/sitemap.xml", "404 Not Found - HTML Tailwind CSS (indikasi Laravel)"),
        ("6", "09:48:28", ".../wp-admin", "Cek endpoint WordPress", "curl -I https://nyamankost.ours.web.id/wp-admin", "HTTP/2 404 - bukan WordPress"),
        ("7", "16:50", "nyamankost.ours.web.id", "Port scanning (di luar scope RoE)*", "nmap -sV -sC -p 80,443,22 nyamankost.ours.web.id", "Port 22 filtered, 80 & 443 open via Cloudflare proxy"),
        ("8", "~17:00", "Target keseluruhan", "Kompilasi dokumentasi evidence", "-", "8 evidence terdokumentasi (E-01 s.d. E-07)"),
    ]
    build_table(doc, ["No", "Timestamp", "Target", "Aktivitas", "Command/Tool", "Hasil Singkat"],
                rows, col_widths_cm=[0.8, 1.8, 3, 2.8, 4, 4.2], font_size=8)
    warning_box(doc, "Aktivitas No.7 (Nmap) berada di luar Exclusion List RoE Bagian 5. Hosting shared melarang port scanning. Evidence E-07 tetap didokumentasikan sebagai catatan faktual.")

# ─── D. HTTP Baseline ────────────────────────────────────────────────────────

def add_http_baseline(doc):
    section_heading(doc, "D", "HTTP/HTTPS Baseline")
    p = doc.add_paragraph()
    r = p.add_run("Command: ")
    r.bold = True; r.font.size = Pt(9.5); r.font.name = "Times New Roman"
    r2 = p.add_run("curl -I https://nyamankost.ours.web.id  |  curl -I http://nyamankost.ours.web.id")
    r2.font.size = Pt(9); r2.font.name = "Courier New"
    rows = [
        ("URL", "https://nyamankost.ours.web.id"),
        ("HTTP Status", "HTTP/2 200 OK (HTTPS)  |  HTTP/1.1 301 Moved Permanently (HTTP)"),
        ("Redirect", "HTTP port 80 ke HTTPS port 443: 301 Moved Permanently ke https://nyamankost.ours.web.id/"),
        ("Server Header", "cloudflare (reverse proxy)  |  X-Turbo-Charged-By: LiteSpeed (web server backend)"),
        ("Content-Type", "text/html; charset=utf-8"),
        ("Cookie / Security Attributes", "XSRF-TOKEN: path=/; secure; samesite=lax  [TANPA HttpOnly - RISIKO XSS+CSRF]\nnyamankost-session: path=/; httponly; secure; samesite=lax  [Konfigurasi OK]"),
        ("Teknologi Teridentifikasi", "PHP/8.5.11, HTML5, Cloudflare CDN, LiteSpeed Web Server"),
    ]
    build_table(doc, ["Parameter", "Hasil"], rows, col_widths_cm=[4, 12.5], font_size=9)
    p2 = doc.add_paragraph()
    r3 = p2.add_run("Interpretasi: ")
    r3.bold = True; r3.font.size = Pt(9.5); r3.font.name = "Times New Roman"
    interp_lines = [
        "[OK] HTTPS aktif dan redirect HTTP ke HTTPS sudah dikonfigurasi dengan benar.",
        "[PERHATIAN] Header X-Powered-By: PHP/8.5.11 mengekspos versi PHP secara spesifik - memudahkan attacker mencari CVE.",
        "[PERHATIAN] Cookie XSRF-TOKEN tidak memiliki flag HttpOnly - dapat dibaca JavaScript, risiko XSS + CSRF chain.",
        "[OK] Cookie nyamankost-session sudah memiliki httponly dan secure.",
        "[PERHATIAN] Tidak ditemukan header keamanan: Content-Security-Policy, X-Frame-Options, X-Content-Type-Options.",
        "[INFO] Header server: cloudflare + cf-ray mengkonfirmasi seluruh traffic melewati Cloudflare edge network.",
    ]
    for line in interp_lines:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(line)
        r.font.size = Pt(9); r.font.name = "Times New Roman"
    doc.add_paragraph()

# ─── E. Fingerprinting ──────────────────────────────────────────────────────

def add_fingerprinting(doc):
    section_heading(doc, "E", "Fingerprinting Teknologi")
    p = doc.add_paragraph()
    r = p.add_run("Command: ")
    r.bold = True; r.font.size = Pt(9.5); r.font.name = "Times New Roman"
    r2 = p.add_run("whatweb https://nyamankost.ours.web.id")
    r2.font.size = Pt(9); r2.font.name = "Courier New"
    rows = [
        ("Web Server", "LiteSpeed (backend) / Cloudflare (reverse proxy/CDN)", "E-01: X-Turbo-Charged-By: LiteSpeed; E-03: server: cloudflare", "Tinggi"),
        ("Framework", "Kemungkinan Laravel (indikasi: XSRF-TOKEN, pola session, Tailwind CSS di error page)", "E-01, E-03, E-05.1", "Sedang"),
        ("CMS", "Tidak ada CMS - bukan WordPress, Joomla, atau CMS umum lainnya", "E-06: /wp-admin ke HTTP 404", "Tinggi"),
        ("Language/Runtime", "PHP 8.5.11", "E-01 & E-03: Header X-Powered-By: PHP/8.5.11", "Tinggi"),
        ("Reverse Proxy/CDN", "Cloudflare - IP 104.21.92.41 & 172.67.186.51 (anycast)", "E-01: server: cloudflare, cf-ray, nel; E-07: IP Cloudflare", "Tinggi"),
        ("JavaScript Library", "Script type=module (modern JS module bundler)", "E-03: WhatWeb Script[module]", "Sedang"),
    ]
    build_table(doc, ["Komponen", "Hasil", "Evidence", "Tingkat Keyakinan"],
                rows, col_widths_cm=[3, 5.5, 5, 2.5], font_size=8.5)

# ─── F. Port Scanning ────────────────────────────────────────────────────────

def add_port_scanning(doc):
    section_heading(doc, "F", "Port dan Service Scanning")
    warning_box(doc, "Aktivitas port scanning menggunakan Nmap (E-07) secara eksplisit DILARANG dalam RoE Bagian 5 (Exclusion List) karena hosting menggunakan layanan shared (Rumah Web). Evidence E-07 tetap didokumentasikan sebagai catatan faktual, namun mahasiswa mengakui aktivitas ini berada di luar scope yang telah disepakati dan tidak akan diulang.")
    p = doc.add_paragraph()
    r = p.add_run("Command persis: ")
    r.bold = True; r.font.size = Pt(9.5); r.font.name = "Times New Roman"
    r2 = p.add_run("nmap -sV -sC -p 80,443,22 nyamankost.ours.web.id")
    r2.font.size = Pt(9); r2.font.name = "Courier New"
    rows = [
        ("22", "tcp", "filtered", "ssh", "Tidak terdeteksi - diblokir Cloudflare/firewall hosting", "E-07"),
        ("80", "tcp", "open", "http", "Cloudflare http proxy | redirect ke HTTPS", "E-07"),
        ("443", "tcp", "open", "ssl/http", "Cloudflare http proxy + SSL | cert wildcard *.ours.web.id | valid s.d. 27 Des 2026", "E-07"),
    ]
    build_table(doc, ["Port", "Proto", "Status", "Service", "Version / Info", "Evidence"],
                rows, col_widths_cm=[1, 1, 1.5, 1.5, 9, 2], font_size=9)

# ─── G. Interpretasi Port ─────────────────────────────────────────────────────

def add_port_interp(doc):
    section_heading(doc, "G", "Interpretasi Status Port")
    rows = [
        ("open", "Port 80 & 443", "Port 80 dan 443 aktif, diproksikan oleh Cloudflare. Port 80 redirect 301 ke port 443 (HTTPS). Port 443 melayani HTTPS dengan SSL wildcard aktif. Server backend (LiteSpeed) tidak dapat diakses langsung karena semua traffic difilter Cloudflare."),
        ("filtered", "Port 22 (SSH)", "Port 22 tidak merespons - diblokir oleh Cloudflare atau firewall hosting. Status filtered TIDAK SAMA dengan closed: SSH mungkin aktif di backend namun tidak dapat diakses dari internet. IP yang discan (172.67.186.51) adalah IP Cloudflare anycast, bukan IP server origin."),
        ("closed", "(tidak ditemukan)", "Tidak ada port berstatus closed dalam scan ini. Cloudflare memfilter semua akses sehingga status closed tidak dapat dikonfirmasi dari luar jaringan."),
    ]
    build_table(doc, ["Status Port", "Port yang Ditemukan", "Interpretasi Mahasiswa"],
                rows, col_widths_cm=[2, 3, 11.5], font_size=9)

# ─── H. Enumerasi Endpoint ───────────────────────────────────────────────────

def add_enumeration(doc):
    section_heading(doc, "H", "Enumerasi Endpoint/Service")
    rows = [
        ("1", "/ (root)", "curl -I + WhatWeb", "HTTP/2 200; PHP/8.5.11; Cloudflare; XSRF-TOKEN (no HttpOnly); LiteSpeed; Title: NyamanKost - Platform Sewa Kos Terpercaya", "E-01, E-03", "Halaman utama aktif, stack teknologi teridentifikasi lengkap"),
        ("2", "http://... (HTTP)", "curl -I", "301 redirect ke HTTPS, Server: cloudflare, keep-alive", "E-02", "Redirect HTTP ke HTTPS dikonfigurasi dengan benar"),
        ("3", "/robots.txt", "curl GET", "User-agent: *  Disallow: (kosong - tidak ada path yang diblokir)", "E-04", "robots.txt ada tapi kosong; tidak ada petunjuk direktori tersembunyi"),
        ("4", "/sitemap.xml", "curl GET", "404 Not Found - HTML error page penuh dengan Tailwind CSS class, judul Not Found", "E-05.1, E-05.2", "Tidak ada sitemap. Halaman 404 mengkonfirmasi framework custom PHP/MVC (indikasi Laravel)"),
        ("5", "/wp-admin", "curl -I", "HTTP/2 404, X-Powered-By: PHP/8.5.11, server: cloudflare", "E-06", "Bukan WordPress. Endpoint tidak ada, platform menggunakan custom framework"),
        ("6", "Port 80 (HTTP)", "Nmap", "Cloudflare http proxy, redirect ke HTTPS, server-header: cloudflare", "E-07", "Traffic HTTP diproksikan Cloudflare, redirect ke HTTPS"),
        ("7", "Port 443 (HTTPS)", "Nmap", "Cloudflare ssl proxy; SSL cert wildcard *.ours.web.id; valid 28 Sep s.d. 27 Des 2026", "E-07", "SSL aktif dan valid. Cloudflare menangani terminasi SSL. Title: NyamanKost"),
        ("8", "Port 22 (SSH)", "Nmap", "filtered - tidak merespons dari internet; commonName=ours.web.id", "E-07", "SSH kemungkinan ada di backend tapi diblokir Cloudflare/hosting firewall"),
    ]
    build_table(doc, ["No", "Endpoint/Service", "Metode", "Informasi Ditemukan", "Evidence", "Interpretasi"],
                rows, col_widths_cm=[0.8, 2.8, 1.8, 4.5, 2, 4.5], font_size=8)

# ─── I. Evidence Register ────────────────────────────────────────────────────

def add_evidence(doc):
    section_heading(doc, "I", "Evidence Register")
    rows = [
        ("E-01", "Screenshot terminal", "curl -I https://nyamankost.ours.web.id: HTTP/2 200, server: cloudflare, PHP/8.5.11, XSRF-TOKEN (no HttpOnly), nyamankost-session (httponly), cf-ray, LiteSpeed", "evidence_pert6/E-01.png", "09 Oct 2026 09:37:03"),
        ("E-02", "Screenshot terminal", "curl -I http://nyamankost.ours.web.id: HTTP/1.1 301 redirect ke HTTPS, Server: cloudflare, Connection: keep-alive", "evidence_pert6/E-02.png", "09 Oct 2026 09:39:03"),
        ("E-03", "Screenshot terminal", "whatweb https://nyamankost.ours.web.id: 200 OK, PHP 8.5.11, Cloudflare, IP 104.21.92.41, cookies, Script[module], HTML5, HttpOnly[nyamankost-session], Title[NyamanKost]", "evidence_pert6/E-03.png", "09 Oct 2026 ~09:40"),
        ("E-04", "Screenshot terminal", "curl https://nyamankost.ours.web.id/robots.txt: output: User-agent: * / Disallow: (kosong, tidak ada path yang diblokir untuk crawler)", "evidence_pert6/E-04.png", "09 Oct 2026 ~09:45"),
        ("E-05.1", "Screenshot terminal", "curl https://nyamankost.ours.web.id/sitemap.xml (bagian 1): HTML 404 Not Found dengan Tailwind CSS class dan struktur MVC (indikasi Laravel framework)", "evidence_pert6/E-05.1.png", "09 Oct 2026 ~09:46"),
        ("E-05.2", "Screenshot terminal", "curl sitemap.xml (bagian 2 - lanjutan): akhir respons HTML 404: h1=404, div=Not Found, closing tags body dan html", "evidence_pert6/E-05.2.png", "09 Oct 2026 ~09:46"),
        ("E-06", "Screenshot terminal", "curl -I https://nyamankost.ours.web.id/wp-admin: HTTP/2 404, PHP/8.5.11 - konfirmasi tidak menggunakan WordPress CMS", "evidence_pert6/E-06.png", "09 Oct 2026 09:48:28"),
        ("E-07", "Screenshot terminal", "nmap -sV -sC -p 80,443,22: Port 22 filtered, 80 & 443 open via Cloudflare; SSL cert wildcard *.ours.web.id; IP 172.67.186.51 (Cloudflare anycast)", "evidence_pert6/E-07.png", "09 Oct 2026 16:50"),
    ]
    build_table(doc, ["ID", "Jenis", "Deskripsi", "Lokasi File", "Timestamp"],
                rows, col_widths_cm=[1.2, 2.5, 6.5, 3.5, 2.8], font_size=8)

# ─── J. Threat Modeling ──────────────────────────────────────────────────────

def add_threat_modeling(doc):
    section_heading(doc, "J", "Threat Modeling")
    p = doc.add_paragraph()
    r = p.add_run("Skala Kemungkinan & Dampak: 1=Rendah, 2=Sedang, 3=Tinggi. Setiap baris memiliki bukti yang dapat dirujuk ke Evidence Register.")
    r.font.size = Pt(9); r.font.name = "Times New Roman"; r.italic = True
    rows = [
        ("1", "Cookie XSRF-TOKEN (tanpa HttpOnly)", "Tinggi", "Pencurian CSRF token via JavaScript (XSS + CSRF chain)", "2", "3", "Tinggi", "E-01"),
        ("2", "Versi PHP terekspos (PHP/8.5.11)", "Sedang", "Eksploitasi CVE pada versi PHP yang diketahui spesifik", "2", "3", "Tinggi", "E-01, E-03"),
        ("3", "Mekanisme autentikasi/login", "Tinggi", "Brute force credential / credential stuffing (rate limiting belum diuji)", "2", "3", "Tinggi", "E-01 (session aktif)"),
        ("4", "Tidak ada header Content-Security-Policy", "Sedang", "XSS stored/reflected - tidak ada pembatasan sumber skrip", "2", "2", "Sedang", "E-01"),
        ("5", "Tidak ada header X-Frame-Options", "Sedang", "Clickjacking - halaman dapat di-embed dalam iframe pihak lain", "2", "2", "Sedang", "E-01"),
        ("6", "Framework PHP/Laravel (terindikasi)", "Sedang", "Debug mode aktif / route enumeration / mass assignment", "1", "3", "Sedang", "E-01, E-05.1"),
        ("7", "robots.txt kosong (Disallow kosong)", "Rendah", "Tidak ada pembatasan direktori - semua path dapat dicoba attacker", "1", "2", "Rendah", "E-04"),
        ("8", "LiteSpeed Web Server (versi tak terekspos)", "Rendah", "Kerentanan LiteSpeed belum dapat dikuantifikasi karena versi tidak diketahui", "1", "2", "Rendah", "E-01"),
    ]
    build_table(doc, ["No", "Aset", "Nilai Aset", "Ancaman Relevan", "Kemung-kinan", "Dampak", "Prioritas", "Evidence"],
                rows, col_widths_cm=[0.8, 3.2, 2, 4.5, 1.3, 1.2, 1.5, 2], font_size=8)

# ─── K. Justifikasi ──────────────────────────────────────────────────────────

def add_justifikasi(doc):
    section_heading(doc, "K", "Justifikasi Prioritas")
    rows = [
        ("Tinggi", "Cookie XSRF-TOKEN - XSS + CSRF Token Theft", "Cookie CSRF token yang dapat dibaca JavaScript (tidak ada HttpOnly) membuka jalur pencurian token. Kondisi sudah terkonfirmasi dari evidence, tidak memerlukan asumsi tambahan.", "E-01"),
        ("Tinggi", "PHP/8.5.11 terekspos - CVE Exploitation", "Versi spesifik PHP terekspos di header X-Powered-By. Attacker dapat langsung mencari CVE di NVD. Informasi ini konkret dan actionable.", "E-01, E-03"),
        ("Tinggi", "Login/Autentikasi - Brute Force", "Session cookie aktif mengindikasikan ada mekanisme login. Belum ada bukti rate limiting. Perlu diuji pada pertemuan berikutnya.", "E-01"),
        ("Sedang", "Tidak ada CSP - XSS", "Tanpa Content-Security-Policy, browser tidak memiliki pembatasan skrip. Meningkatkan dampak jika ada XSS. Perlu dicari celah input dulu.", "E-01"),
        ("Sedang", "Tidak ada X-Frame-Options - Clickjacking", "Mudah diverifikasi dan dieksploitasi, namun memerlukan interaksi korban. Risiko nyata tapi dampak lebih rendah dari XSS.", "E-01"),
        ("Rendah", "robots.txt kosong", "Tidak ada info sensitif, tidak ada path yang terekspos secara tidak sengaja. Kontribusi minor ke attack surface.", "E-04"),
    ]
    build_table(doc, ["Prioritas", "Aset/Ancaman", "Alasan Teknis", "Bukti Pendukung"],
                rows, col_widths_cm=[2, 4, 9, 1.5], font_size=8.5)

# ─── L. Rencana ──────────────────────────────────────────────────────────────

def add_rencana(doc):
    section_heading(doc, "L", "Rencana Pengujian Berikutnya")
    rows = [
        ("1", "Cookie XSRF-TOKEN / Form input", "Apakah input form rentan XSS? Jika ya, apakah CSRF token dapat dicuri via document.cookie?", "Injeksi payload XSS sederhana di semua form input; baca cookie via JS jika berhasil", "Izin RoE Bagian 4 - diizinkan (input validation & injection)"),
        ("2", "PHP/8.5.11 runtime", "Apakah versi ini memiliki CVE aktif yang dapat dieksploitasi dari lapisan aplikasi?", "Lookup NVD/CVE database untuk PHP 8.5.11; analisis path eksploitasi", "Tidak perlu izin tambahan - analisis pasif"),
        ("3", "Endpoint autentikasi/login", "Apakah ada proteksi rate limiting pada form login? Apakah lockout mechanism ada?", "Identifikasi form login; uji respons terhadap login gagal berulang; cek header respons", "Izin RoE Bagian 4 - diizinkan (autentikasi & manajemen sesi)"),
        ("4", "Header keamanan (CSP, X-Frame-Options)", "Apakah halaman rentan terhadap clickjacking dan eksekusi skrip eksternal?", "Buat halaman HTML lokal dengan iframe ke target; uji embed; cek CSP di DevTools", "Diizinkan - pengujian konfigurasi keamanan dari luar"),
        ("5", "Framework routes / endpoint tersembunyi", "Apakah ada endpoint/route yang tidak tampil di UI namun dapat diakses?", "Path fuzzing ringan dengan wordlist framework-specific (Laravel routes umum)", "Diizinkan jika tidak aggressive; perhatikan rate limit"),
    ]
    build_table(doc, ["Urutan", "Target/Aset", "Hipotesis yang Diuji", "Metode yang Direncanakan", "Prasyarat/Izin"],
                rows, col_widths_cm=[1.2, 3, 4, 4.5, 3.5], font_size=8.5)

# ─── M. Analisis ─────────────────────────────────────────────────────────────

def add_analisis(doc):
    section_heading(doc, "M", "Analisis Mahasiswa")
    qa = [
        ("1. Apa aset paling bernilai yang ditemukan?",
         "Aset paling bernilai adalah mekanisme autentikasi dan session management aplikasi. Hal ini terbukti dari keberadaan cookie nyamankost-session dan XSRF-TOKEN pada setiap respons (E-01), yang mengindikasikan sistem login aktif. Akses tidak sah ke sesi pengguna atau admin berpotensi memengaruhi seluruh data kost dan pengguna platform."),
        ("2. Temuan apa yang paling penting dan mengapa?",
         "Temuan paling penting adalah cookie XSRF-TOKEN yang tidak memiliki flag HttpOnly (E-01). Cookie CSRF token yang dapat dibaca JavaScript secara langsung melemahkan proteksi CSRF. Jika terdapat celah XSS di bagian manapun aplikasi, attacker dapat mencuri token ini dan melakukan aksi palsu atas nama pengguna yang sedang login. Selain itu, eksposur versi PHP/8.5.11 (E-01, E-03) memberikan informasi teknis spesifik yang membantu attacker dalam reconnaissance."),
        ("3. Apa perbedaan antara data yang benar-benar terobservasi dan asumsi?",
         "Terobservasi (fakta): Server cloudflare, PHP/8.5.11, LiteSpeed, XSRF-TOKEN tanpa HttpOnly, redirect HTTP ke HTTPS, robots.txt kosong, tidak ada sitemap.xml, /wp-admin 404, port 22 filtered, 80 & 443 open, SSL wildcard *.ours.web.id.\nAsumsi (hipotesis): Framework adalah Laravel - hanya indikasi dari pola cookie dan Tailwind CSS, belum dikonfirmasi. Database kemungkinan MySQL - belum ada evidence. Ada form login - belum dikonfirmasi, hanya terindikasi dari session cookie aktif."),
        ("4. Mengapa suatu aset diberi prioritas Tinggi/Sedang/Rendah?",
         "Prioritas Tinggi diberikan pada ancaman yang (1) kondisinya sudah terkonfirmasi dari evidence nyata, DAN (2) memiliki kemungkinan >= 2 serta dampak = 3. Cookie XSRF-TOKEN tanpa HttpOnly diprioritaskan Tinggi karena langsung terobservasi dari E-01. Ancaman Sedang memerlukan kondisi tambahan atau kemungkinan lebih rendah. Ancaman Rendah berkontribusi pada attack surface namun tidak langsung mengakibatkan kompromi."),
        ("5. Apa keterbatasan hasil scanning/enumeration Anda?",
         "Semua traffic melewati Cloudflare - server origin tidak dapat diakses langsung, fingerprinting backend bersifat parsial. Tidak ada enumeration fitur fungsional aplikasi (form, API, endpoint login) - recon terbatas pada header HTTP dan tool fingerprinting. Nmap dilakukan di luar scope RoE. Belum ada analisis konten halaman yang sebenarnya - aset bisnis belum dapat diidentifikasi secara konkret."),
    ]
    for q, a in qa:
        p = doc.add_paragraph()
        r = p.add_run(q)
        r.bold = True; r.font.size = Pt(10); r.font.name = "Times New Roman"
        p.paragraph_format.space_after = Pt(2)
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Cm(0.5)
        p2.paragraph_format.space_after = Pt(8)
        r2 = p2.add_run(a)
        r2.font.size = Pt(9.5); r2.font.name = "Times New Roman"

# ─── N. Checklist ────────────────────────────────────────────────────────────

def add_checklist(doc):
    section_heading(doc, "N", "Checklist Kepatuhan")
    items = [
        "Target memiliki izin (RoE ditandatangani 25/09/2026).",
        "Semua aktivitas berada dalam scope (kecuali Nmap yang telah didokumentasikan pelanggarannya secara transparan).",
        "Tidak melakukan brute force atau DoS.",
        "Tidak mengeksploitasi temuan tanpa izin.",
        "Data sensitif telah disunting (nilai cookie dipotong di evidence).",
        "Command dan evidence lengkap (E-01 s.d. E-07 + E-04 diperbarui).",
        "Threat model terhubung dengan evidence (setiap ancaman memiliki ID evidence).",
    ]
    for text in items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run("[V]  ")
        r1.bold = True; r1.font.size = Pt(10.5); r1.font.name = "Times New Roman"
        r1.font.color.rgb = RGBColor(0x1B, 0x7A, 0x1B)
        r2 = p.add_run(text)
        r2.font.size = Pt(10); r2.font.name = "Times New Roman"
    doc.add_paragraph()

# ─── O. Pernyataan ───────────────────────────────────────────────────────────

def add_pernyataan(doc):
    section_heading(doc, "O", "Pernyataan Individu")
    p = doc.add_paragraph()
    r = p.add_run(
        "Saya menyatakan bahwa seluruh aktivitas praktikum yang saya dokumentasikan dilakukan terhadap target "
        "yang telah diberi izin, sesuai scope dan batasan pengujian sebagaimana tercantum dalam RoE Pentest "
        "KSI 5A 2026. Saya tidak memperluas target atau metode pengujian tanpa otorisasi. Aktivitas port "
        "scanning (Nmap) yang tercatat dalam E-07 diakui berada di luar Exclusion List RoE dan telah "
        "didokumentasikan secara transparan dalam Bagian F dan Checklist Kepatuhan."
    )
    r.font.size = Pt(10); r.font.name = "Times New Roman"
    p.paragraph_format.space_after = Pt(16)
    tbl = doc.add_table(rows=3, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (k, v) in enumerate([("Nama", "M. Arifin Ilham"), ("Tanda Tangan", ""), ("Tanggal", "09/10/2026")]):
        kc = tbl.rows[i].cells[0]
        vc = tbl.rows[i].cells[1]
        kc.width = Cm(4); vc.width = Cm(6)
        set_cell_bg(kc, "E8EDF7")
        set_borders(kc); set_borders(vc)
        cell_text(kc, k, bold=True, size=10)
        cell_text(vc, v, size=10)
    doc.add_paragraph()

# ─── Pendalaman Threat Modeling ───────────────────────────────────────────────

def add_pendalaman(doc):
    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(14)
    r = p_title.add_run("PENDALAMAN THREAT MODELING - Output Wajib Bagian H")
    r.bold = True; r.font.size = Pt(12); r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0x1F, 0x3D, 0x7A)
    pPr = p_title._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    for side in ["top", "bottom"]:
        b = OxmlElement(f"w:{side}")
        b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "8")
        b.set(qn("w:space"), "1"); b.set(qn("w:color"), "1F3D7A")
        pBdr.append(b)
    pPr.append(pBdr)

    # 1. Inventarisasi Aset
    sub_heading(doc, "1. Inventarisasi Aset")
    build_table(doc,
        ["No", "Aset/Endpoint", "Fungsi", "Data/Fungsi Penting?", "Evidence ID"],
        [
            ("1", "Halaman utama (/)", "Entry point platform sewa kost", "Ya - title: Platform Sewa Kos Terpercaya", "E-01, E-03"),
            ("2", "Session management (nyamankost-session)", "Autentikasi & otorisasi pengguna", "Ya - mengelola identitas login", "E-01"),
            ("3", "CSRF Token (XSRF-TOKEN, no HttpOnly)", "Proteksi dari CSRF attack", "Ya - kritis; TIDAK ada HttpOnly", "E-01"),
            ("4", "Web server LiteSpeed", "Melayani konten web dari backend", "Ya - infrastruktur utama", "E-01, E-03"),
            ("5", "Cloudflare CDN/Proxy", "DDoS protection, SSL termination, caching", "Ya - keamanan lapisan jaringan", "E-01, E-02, E-07"),
            ("6", "PHP Runtime v8.5.11", "Menjalankan logika aplikasi backend", "Ya - runtime utama; versi terekspos", "E-01, E-03"),
            ("7", "robots.txt", "Instruksi untuk web crawler", "Tidak kritis - kosong", "E-04"),
            ("8", "Framework backend (kemungkinan Laravel)", "Routing, DB, autentikasi, business logic", "Ya - fondasi seluruh aplikasi", "E-01, E-05.1"),
        ],
        col_widths_cm=[0.8, 3.5, 3.5, 5, 2.5], font_size=8.5)

    # 2. Nilai Aset
    sub_heading(doc, "2. Nilai Aset")
    build_table(doc,
        ["Aset", "Nilai (1-3)", "Alasan Penilaian"],
        [
            ("Session management", "3 (Tinggi)", "Kompromi session = akses penuh ke akun pengguna"),
            ("CSRF Token (XSRF-TOKEN)", "3 (Tinggi)", "Kegagalan CSRF protection = aksi tidak sah atas nama pengguna"),
            ("PHP Runtime", "2 (Sedang)", "Versi terekspos membantu attacker, namun eksploitasi butuh CVE spesifik"),
            ("Framework backend", "2 (Sedang)", "Kerentanan framework bisa berdampak luas namun butuh konfirmasi versi"),
            ("Cloudflare CDN", "2 (Sedang)", "Melindungi infrastruktur - bukan aset yang bisa diserang dari lapisan aplikasi"),
            ("Halaman utama", "2 (Sedang)", "Entry point penting namun tidak langsung menyimpan data sensitif"),
            ("LiteSpeed Web Server", "1 (Rendah)", "Versi tidak terekspos - risiko belum dapat dikuantifikasi"),
            ("robots.txt", "1 (Rendah)", "Kosong - tidak ada informasi sensitif"),
        ],
        col_widths_cm=[5, 2.5, 9], font_size=8.5)

    # 3. Identifikasi Ancaman
    sub_heading(doc, "3. Identifikasi Ancaman")
    build_table(doc,
        ["Aset", "Evidence", "Ancaman Relevan", "Mengapa Ancaman Ini Relevan?"],
        [
            ("XSRF-TOKEN (tanpa HttpOnly)", "E-01", "Pencurian token CSRF via JS (XSS + CSRF chain)", "Cookie dapat diakses via document.cookie - jika ada XSS, token langsung bisa dicuri untuk aksi palsu"),
            ("PHP/8.5.11", "E-01, E-03", "Eksploitasi CVE versi PHP yang diketahui", "Versi spesifik diketahui - attacker dapat lookup CVE database secara langsung"),
            ("Tidak ada CSP header", "E-01", "XSS stored/reflected", "Tanpa CSP, tidak ada kontrol atas skrip yang dapat dieksekusi di browser korban"),
            ("Tidak ada X-Frame-Options", "E-01", "Clickjacking", "Halaman dapat dimuat dalam iframe untuk mengelabui pengguna melakukan aksi tidak disadari"),
            ("Session cookie aktif", "E-01", "Brute force login / session fixation", "Session aktif mengindikasikan login ada; belum ada bukti rate limiting"),
            ("Framework Laravel (terindikasi)", "E-05.1", "Debug mode aktif / route disclosure", "Framework PHP sering memiliki debug mode yang tidak dinonaktifkan di production"),
        ],
        col_widths_cm=[3, 2, 4, 7.5], font_size=8.5)

    # 4. Penilaian
    sub_heading(doc, "4. Penilaian Kemungkinan dan Dampak")
    build_table(doc,
        ["Aset/Ancaman", "Kemungkinan (1-3)", "Dampak (1-3)", "Alasan"],
        [
            ("XSRF-TOKEN - XSS + CSRF", "2", "3", "Perlu ada celah XSS dulu (kemungkinan sedang), tapi dampak pencurian sesi sangat tinggi"),
            ("PHP 8.5.11 - CVE exploitation", "2", "3", "Bergantung pada apakah CVE aktif ada untuk versi ini - belum diverifikasi"),
            ("Tanpa CSP - XSS", "2", "2", "Perlu input tidak tersanitasi - kemungkinan sedang, dampak sedang"),
            ("Tanpa X-Frame-Options - Clickjacking", "2", "2", "Mudah dieksploitasi namun membutuhkan interaksi korban"),
            ("Login - Brute force", "2", "3", "Bergantung apakah ada rate limiting - belum diuji pada pertemuan ini"),
            ("Framework - debug/route disclosure", "1", "3", "Kemungkinan rendah jika production setup benar, tapi dampak besar jika aktif"),
        ],
        col_widths_cm=[5, 2.5, 2.5, 6.5], font_size=8.5)

    # 5. Tabel Prioritas
    sub_heading(doc, "5. Tabel Prioritas Threat Model")
    build_table(doc,
        ["No", "Aset", "Ancaman", "Evidence", "Nilai Aset", "Kemung-kinan", "Dampak", "Prioritas", "Alasan"],
        [
            ("1", "XSRF-TOKEN", "XSS + CSRF token theft", "E-01", "3", "2", "3", "Tinggi", "Cookie kritis tanpa HttpOnly - kondisi sudah terbukti dari evidence"),
            ("2", "PHP/8.5.11", "CVE exploitation", "E-01, E-03", "2", "2", "3", "Tinggi", "Versi spesifik terekspos - actionable untuk attacker"),
            ("3", "Login/Auth", "Brute force credential", "E-01", "3", "2", "3", "Tinggi", "Session aktif terdeteksi - login endpoint perlu diuji"),
            ("4", "Tanpa CSP", "XSS reflected/stored", "E-01", "2", "2", "2", "Sedang", "Tidak ada pertahanan CSP - perlu uji input dulu"),
            ("5", "Tanpa X-Frame-Options", "Clickjacking", "E-01", "2", "2", "2", "Sedang", "Mudah dieksploitasi namun perlu interaksi korban"),
            ("6", "Framework Laravel", "Debug/route enumeration", "E-05.1", "2", "1", "3", "Sedang", "Kemungkinan rendah, tapi dampak besar jika debug aktif"),
            ("7", "robots.txt kosong", "Crawling direktori", "E-04", "1", "1", "2", "Rendah", "Kontribusi minor ke attack surface"),
            ("8", "LiteSpeed server", "Kerentanan server", "E-01", "1", "1", "2", "Rendah", "Versi tidak terekspos - risiko tidak dapat dikuantifikasi"),
        ],
        col_widths_cm=[0.8, 2.5, 3, 2, 1.5, 1.3, 1.2, 1.5, 3], font_size=8)

    # 6. Attack Surface Map
    sub_heading(doc, "6. Attack Surface Map Sederhana")
    build_table(doc,
        ["Entry Point", "Aset/Fungsi", "Ancaman", "Prioritas", "Evidence"],
        [
            ("Setiap halaman web (browser)", "Cookie XSRF-TOKEN (no HttpOnly)", "XSS ke Pencurian CSRF Token ke Aksi palsu atas nama pengguna", "Tinggi", "E-01"),
            ("Response HTTP header", "PHP/8.5.11 terekspos", "Reconnaissance ke CVE Lookup ke Exploitation via kerentanan PHP", "Tinggi", "E-01, E-03"),
            ("Form input (belum dikonfirmasi)", "Database / logika aplikasi", "SQL Injection / XSS stored pada form pencarian atau input lain", "Tinggi", "E-01 (session aktif = ada interaksi DB)"),
            ("URL bar / iframe (no X-Frame-Options)", "Halaman utama aplikasi", "Clickjacking - pengguna melakukan aksi tanpa sadar dalam iframe", "Sedang", "E-01"),
            ("HTTP response (tanpa CSP)", "Browser pengguna", "Eksekusi skrip pihak ketiga / XSS reflected tanpa pembatasan sumber", "Sedang", "E-01"),
        ],
        col_widths_cm=[3.5, 3.5, 5, 2, 2.5], font_size=8.5)

    # 7. Testing Priority List
    sub_heading(doc, "7. Testing Priority List")
    build_table(doc,
        ["Urutan", "Target/Aset", "Hipotesis", "Evidence", "Alasan Diprioritaskan", "Metode yang Direncanakan"],
        [
            ("1", "Cookie XSRF-TOKEN / Form input", "CSRF token dapat dicuri via XSS karena tidak ada HttpOnly", "E-01", "Kondisi sudah terkonfirmasi dari evidence langsung", "Uji XSS di semua form input; jika berhasil baca cookie via JS"),
            ("2", "PHP/8.5.11 runtime", "Versi PHP ini memiliki CVE yang bisa dieksploitasi", "E-01, E-03", "Versi spesifik sudah diketahui - langsung cari di NVD", "Lookup NVD untuk PHP 8.5.11; analisis path eksploitasi"),
            ("3", "Endpoint autentikasi/login", "Tidak ada rate limiting pada form login", "E-01", "Session aktif terdeteksi - login endpoint kemungkinan ada", "Identifikasi form login; uji respons login gagal berulang"),
            ("4", "Security header (CSP, X-Frame-Options)", "Halaman rentan clickjacking dan XSS", "E-01", "Header tidak ada - mudah diverifikasi", "Buat halaman HTML lokal dengan iframe ke target; cek DevTools"),
            ("5", "Framework routes / endpoint tersembunyi", "Ada endpoint sensitif yang tidak tampil di UI", "E-05.1", "Framework MVC biasanya punya route tersembunyi", "Path fuzzing ringan dengan wordlist Laravel-specific"),
        ],
        col_widths_cm=[1.2, 3, 3, 2, 3.5, 4], font_size=8)

    # 8. Refleksi
    sub_heading(doc, "8. Refleksi Threat Modeling")
    refleksi = [
        ("Apa aset paling bernilai pada target Anda? Jelaskan berdasarkan evidence.",
         "Cookie nyamankost-session dan XSRF-TOKEN adalah aset paling bernilai yang teridentifikasi. Keduanya terhubung langsung ke mekanisme autentikasi dan proteksi CSRF. Evidence E-01 secara langsung mengkonfirmasi keberadaan dan konfigurasi cookie ini - ini adalah fakta observasi, bukan asumsi."),
        ("Ancaman apa yang paling relevan terhadap aset tersebut? Mengapa?",
         "Ancaman paling relevan adalah chaining XSS + CSRF token theft. Alasan: (1) cookie XSRF-TOKEN tidak memiliki flag HttpOnly (terkonfirmasi E-01) - kondisi teknis eksploitasi sudah terpenuhi; (2) jika XSS ditemukan di manapun, token ini dapat langsung dicuri untuk melakukan aksi palsu atas nama pengguna."),
        ("Mengapa aset prioritas pertama harus diuji lebih dahulu?",
         "XSRF-TOKEN tanpa HttpOnly diuji pertama karena kondisinya sudah terkonfirmasi dari evidence tanpa memerlukan scanning tambahan. Pengujian XSS pada input form adalah langkah alami berikutnya yang sesuai scope RoE dan langsung membuktikan atau menyangkal hipotesis."),
        ("Apa informasi yang masih belum diketahui dan perlu diverifikasi pada tahap berikutnya?",
         "Apakah ada form input pengguna (login, pencarian, kontak)? Versi framework Laravel - menentukan CVE spesifik. Apakah ada rate limiting pada login? Apakah debug mode framework aktif di production? Apakah ada endpoint API yang tidak terdokumentasi?"),
        ("Apa perbedaan antara fakta hasil recon dan hipotesis ancaman Anda?",
         "Fakta: XSRF-TOKEN tidak ada HttpOnly (E-01). PHP/8.5.11 terekspos (E-01). Tidak ada CSP/X-Frame-Options (E-01). robots.txt kosong (E-04). /wp-admin 404 (E-06). SSL wildcard valid (E-07).\nHipotesis: Framework adalah Laravel - belum dikonfirmasi. Ada form login - belum dikonfirmasi. CVE aktif untuk PHP 8.5.11 - belum diverifikasi. XSS ada di aplikasi - belum diuji."),
    ]
    for q, a in refleksi:
        p = doc.add_paragraph()
        r = p.add_run(q)
        r.bold = True; r.font.size = Pt(9.5); r.font.name = "Times New Roman"
        p.paragraph_format.space_after = Pt(2)
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Cm(0.5)
        p2.paragraph_format.space_after = Pt(6)
        r2 = p2.add_run(a)
        r2.font.size = Pt(9); r2.font.name = "Times New Roman"

    # 9. Output checklist
    sub_heading(doc, "9. Output Akhir yang Harus Ada")
    for o in [
        "Inventaris aset (8 aset teridentifikasi)                    [V]",
        "Nilai aset (skala 1-3 dengan justifikasi)                   [V]",
        "Ancaman relevan (berbasis evidence nyata)                    [V]",
        "Evidence untuk setiap keputusan penting                     [V]",
        "Penilaian kemungkinan dan dampak (skala 1-3 dengan alasan)  [V]",
        "Prioritas Tinggi/Sedang/Rendah                              [V]",
        "Attack surface map sederhana (5 entri)                      [V]",
        "Testing Priority List (5 target)                            [V]",
        "Refleksi dan keterbatasan                                   [V]",
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(o)
        r.font.size = Pt(10); r.font.name = "Times New Roman"
        r.font.color.rgb = RGBColor(0x1B, 0x7A, 0x1B)

# ─── Footer ──────────────────────────────────────────────────────────────────

def add_footer(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(14)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    top = OxmlElement("w:top")
    top.set(qn("w:val"), "single"); top.set(qn("w:sz"), "6")
    top.set(qn("w:space"), "1"); top.set(qn("w:color"), "1F3D7A")
    pBdr.append(top); pPr.append(pBdr)
    r = p.add_run("Lembar Kerja Pertemuan 6 Penetration Testing  |  M. Arifin Ilham (6404240008)  |  KSI 5A  |  Politeknik Negeri Bengkalis  |  2026")
    r.font.size = Pt(8); r.font.name = "Times New Roman"
    r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    doc = Document()
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(3)
        section.right_margin  = Cm(2)
    doc.styles["Normal"].font.name = "Times New Roman"
    doc.styles["Normal"].font.size = Pt(11)

    add_header(doc)
    add_title(doc)
    add_tujuan(doc)
    add_scope(doc)
    add_log(doc)
    add_http_baseline(doc)
    add_fingerprinting(doc)
    add_port_scanning(doc)
    add_port_interp(doc)
    add_enumeration(doc)
    add_evidence(doc)
    add_threat_modeling(doc)
    add_justifikasi(doc)
    add_rencana(doc)
    add_analisis(doc)
    add_checklist(doc)
    add_pernyataan(doc)
    add_pendalaman(doc)
    add_footer(doc)

    output = r"c:\laragon\www\usaha\print memorie's\tugas\Penetration Testing\Lembar_Kerja_Pert6_M_Arifin_Ilham.docx"
    doc.save(output)
    print(f"Dokumen berhasil disimpan: {output}")

if __name__ == "__main__":
    main()
