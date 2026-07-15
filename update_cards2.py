# -*- coding: utf-8 -*-
import re

urls = [
    ('https://undanganpernikahantyo-juli.vercel.app/', 'Tyo & Juli'),
    ('https://undangan-wawan-nelta-wine.vercel.app/', 'Wawan & Nelta'),
    ('https://undangan-nelta-wawan.vercel.app/', 'Nelta & Wawan'),
    ('https://undangan-yunia-khambali.vercel.app/', 'Yunia & Khambali'),
    ('https://undanganhengky-endang.vercel.app/', 'Hengky & Endang'),
    ('https://undangan-juli-tyo.vercel.app/', 'Juli & Tyo'),
    ('https://undangan-pernikahan-red.vercel.app/', 'Tema Merah'),
    ('https://undangan4-seven.vercel.app/', 'Undangan Spesial'),
    ('https://undangan-hengky-endang-y4qs.vercel.app/', 'Hengky & Endang 2')
]

cards_html = ''
for i in range(1, 13):
    delay = (i - 1) % 3 + 1
    if i <= 9:
        url, title = urls[i-1]
        cards_html += f'''
        <!-- Card {i} -->
        <div class="portfolio-card fade-up delay-{delay}">
          <div class="portfolio-preview">
            <iframe src="{url}" title="Preview Undangan — {title}"
              loading="lazy" sandbox="allow-scripts allow-same-origin"></iframe>
            <div class="portfolio-preview-overlay">
              <a href="{url}" target="_blank" rel="noopener noreferrer"
                class="portfolio-preview-btn" id="portfolio-demo-{i}">
                👁️ Lihat Demo
              </a>
            </div>
          </div>
          <div class="portfolio-info">
            <p class="portfolio-label">Tema Elegan</p>
            <h3>Undangan {title}</h3>
            <p>Desain modern dan interaktif untuk momen spesial Anda.</p>
            <div class="portfolio-tags">
              <span class="portfolio-tag">✨ Mewah</span>
              <span class="portfolio-tag">⏳ Countdown</span>
            </div>
            <a href="{url}" target="_blank" rel="noopener noreferrer"
              class="portfolio-link-btn">
              🔗 Buka Demo →
            </a>
          </div>
        </div>
'''
    else:
        cards_html += f'''
        <!-- Card {i} -->
        <div class="portfolio-card fade-up delay-{delay}">
          <div class="portfolio-preview">
            <div class="portfolio-preview-placeholder">
              <span class="preview-icon">👑</span>
              <p>Demo Undangan #{i}</p>
            </div>
            <div class="portfolio-preview-overlay">
              <a href="https://wa.me/6281234567890?text=Halo%2C%20saya%20tertarik%20dengan%20tema%20ini" target="_blank" rel="noopener noreferrer"
                class="portfolio-preview-btn" id="portfolio-demo-{i}">
                💬 Tanya Tema Ini
              </a>
            </div>
          </div>
          <div class="portfolio-info">
            <p class="portfolio-label">Tema Modern</p>
            <h3>Segera Hadir</h3>
            <p>Tema baru sedang dalam tahap desain oleh tim kami.</p>
            <div class="portfolio-tags">
              <span class="portfolio-tag">🎨 Desain Baru</span>
            </div>
            <a href="https://wa.me/6281234567890?text=Halo%20Print%20Memorie%27s" target="_blank" rel="noopener noreferrer"
              class="portfolio-link-btn">
              💬 Konsultasi Tema →
            </a>
          </div>
        </div>
'''

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '<div class="portfolio-grid hide-more" id="portfolioGrid">'
end_marker = '<div class="portfolio-cta fade-up">'

start_idx = html.find(start_marker) + len(start_marker)
end_idx = html.find(end_marker)

if start_idx != -1 and end_idx != -1:
    # Need to keep the closing div for portfolioGrid before portfolio-cta
    new_html = html[:start_idx] + '\n' + cards_html + '\n      </div>\n\n      ' + html[end_idx:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print('Successfully replaced cards')
else:
    print('Could not find markers')
