# -*- coding: utf-8 -*-
import re

urls = [
    ('https://undanganpernikahantyo-juli.vercel.app/', 'Tyo & Juli'),
    ('https://undangan-wawan-nelta-wine.vercel.app/', 'Wawan & Nelta'),
    ('https://undangan-nelta-wawan.vercel.app/', 'Nelta & Wawan'),
    ('https://undangan-yunia-khambali.vercel.app/', 'Yunia & Khambali'),
    ('https://undanganhengky-endang.vercel.app/', 'Hengky & Endang'),
    ('https://undangan-juli-tyo.vercel.app/', 'Juli & Tyo'),
    ('https://undangan-pernikahan-red.vercel.app/', 'Pernikahan Tema Merah'),
    ('https://undangan4-seven.vercel.app/', 'Undangan Spesial'),
    ('https://undangan-hengky-endang-y4qs.vercel.app/', 'Hengky & Endang')
]

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for i, (url, title) in enumerate(urls, 1):
    card_marker = f'<!-- Card {i} -->'
    next_card_marker = f'<!-- Card {i+1} -->'
    if i == 15:
        next_card_marker = '<div class="portfolio-cta"'
    
    start_idx = html.find(card_marker)
    end_idx = html.find(next_card_marker)
    
    if start_idx == -1 or end_idx == -1:
        print(f'Could not find bounds for Card {i}')
        continue
        
    card_html = html[start_idx:end_idx]
    
    # Replace preview section
    preview_pattern = re.compile(r'<div class="portfolio-preview">.*?</div>\s*</div>', re.DOTALL)
    new_preview = f'''<div class="portfolio-preview">
            <iframe src="{url}" title="Preview Undangan — {title}"
              loading="lazy" sandbox="allow-scripts allow-same-origin"></iframe>
            <div class="portfolio-preview-overlay">
              <a href="{url}" target="_blank" rel="noopener noreferrer"
                class="portfolio-preview-btn" id="portfolio-demo-{i}">
                👁️ Lihat Demo
              </a>
            </div>
          </div>'''
    card_html = preview_pattern.sub(new_preview, card_html)
    
    # Replace title
    title_pattern = re.compile(r'<h3>.*?</h3>', re.DOTALL)
    card_html = title_pattern.sub(f'<h3>Undangan {title}</h3>', card_html, count=1)
    
    # Replace link-btn
    link_pattern = re.compile(r'<a href="[^"]*"[^>]*class="portfolio-link-btn"[^>]*>.*?</a>', re.DOTALL)
    new_link = f'''<a href="{url}" target="_blank" rel="noopener noreferrer"
              class="portfolio-link-btn">
              🔗 Buka Demo →
            </a>'''
    card_html = link_pattern.sub(new_link, card_html)
    
    html = html[:start_idx] + card_html + html[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated index.html')
