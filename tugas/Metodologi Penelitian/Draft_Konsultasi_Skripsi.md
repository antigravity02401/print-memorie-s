# DRAFT KONSULTASI SKRIPSI

**Nama       :** (isi nama kamu)
**NIM        :** (isi NIM kamu)
**Prodi      :** Keamanan Sistem Informasi
**Semester   :** 5

---

## Judul

**"Pengujian Keamanan Input Validation pada Aplikasi Web Undangan Digital Menggunakan Metode OWASP Web Security Testing Guide (WSTG) v4.2: Studi Kasus Print Memorie's"**

---

## Latar Belakang

Perkembangan teknologi digital telah mengubah cara masyarakat Indonesia dalam menyebarkan undangan pernikahan. Platform undangan pernikahan digital semakin populer karena lebih efisien, hemat biaya, dan mudah dibagikan melalui media sosial maupun aplikasi pesan instan.

Namun, platform undangan digital umumnya mengumpulkan **data pribadi pengguna** seperti nama lengkap, alamat, nomor telepon, dan konfirmasi kehadiran (RSVP). Data-data ini dimasukkan melalui berbagai form input yang tersedia di platform. Jika form input tersebut tidak diamankan dengan baik, platform rentan terhadap serangan seperti **Cross-Site Scripting (XSS)** dan **SQL Injection** yang dapat menyebabkan kebocoran data, manipulasi konten, hingga pengambilalihan sistem.

**Print Memorie's** adalah platform undangan pernikahan digital yang dibangun menggunakan teknologi web modern (HTML, CSS, JavaScript) dengan backend serverless (Vercel) dan database PostgreSQL (Neon). Platform ini memiliki beberapa titik input pengguna seperti form testimoni dan API endpoint yang memproses data dari pengguna. Platform ini merupakan milik peneliti sendiri sehingga pengujian dapat dilakukan secara menyeluruh dengan pendekatan grey-box testing.

Oleh karena itu, penelitian ini bertujuan untuk melakukan pengujian keamanan pada aspek input validation platform Print Memorie's menggunakan metode **OWASP Web Security Testing Guide (WSTG) v4.2**.

---

## Rumusan Masalah

1. Kerentanan input validation apa saja yang terdapat pada platform undangan digital Print Memorie's berdasarkan pengujian OWASP WSTG v4.2?
2. Bagaimana tingkat keparahan (severity) dari setiap kerentanan yang ditemukan berdasarkan CVSS v3.1?
3. Bagaimana rekomendasi dan implementasi perbaikan untuk mengatasi kerentanan yang ditemukan?

---

## Tujuan Penelitian

1. Mengidentifikasi kerentanan input validation pada platform Print Memorie's menggunakan metode OWASP WSTG v4.2.
2. Mengukur tingkat keparahan setiap kerentanan menggunakan CVSS v3.1.
3. Memberikan rekomendasi perbaikan dan mengimplementasikan mitigasi terhadap kerentanan yang ditemukan.

---

## Batasan Masalah

1. Pengujian dilakukan pada platform Print Memorie's (print-memorie-s-two.vercel.app).
2. Fokus pada kategori Input Validation Testing (WSTG-INPV) dan Client-Side Testing (WSTG-CLNT).
3. Test case yang diuji:
   - WSTG-INPV-01 : Reflected Cross-Site Scripting
   - WSTG-INPV-02 : Stored Cross-Site Scripting
   - WSTG-INPV-05 : SQL Injection
   - WSTG-INPV-06 : HTTP Parameter Pollution
   - WSTG-CLNT-01 : DOM-based Cross-Site Scripting
   - WSTG-CLNT-09 : Clickjacking
4. Pengujian menggunakan pendekatan grey-box testing.
5. Penilaian kerentanan menggunakan CVSS v3.1.

---

## Metode Penelitian

**OWASP Web Security Testing Guide (WSTG) v4.2** — panduan pengujian keamanan aplikasi web dari OWASP Foundation yang berisi prosedur pengujian terstruktur dengan kode unik per test case.

---

## Referensi Awal

1. OWASP Foundation. (2023). *OWASP Web Security Testing Guide v4.2*. https://owasp.org/www-project-web-security-testing-guide/
2. FIRST.org. (2019). *Common Vulnerability Scoring System v3.1 Specification*. https://www.first.org/cvss/v3.1/specification-document
3. (tambahkan 2-3 jurnal dari Google Scholar)

