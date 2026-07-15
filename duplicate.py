import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

grid_start_idx = html.find('<div class=\"portfolio-grid\">')
grid_end_idx = html.find('</div>\n\n    <div class=\"portfolio-cta')

if grid_start_idx != -1 and grid_end_idx != -1:
    grid_content = html[grid_start_idx:grid_end_idx]
    
    card3_match = re.search(r'<!-- Card 3 -->.*?</div>\s*</div>', grid_content, re.DOTALL)
    if card3_match:
        card3_html = card3_match.group(0)
        
        new_cards = []
        for i in range(4, 16):
            new_card = card3_html.replace('Card 3', f'Card {i}').replace('Demo Undangan #3', f'Demo Undangan #{i}')
            delay = (i % 3) + 1
            new_card = re.sub(r'delay-\d', f'delay-{delay}', new_card)
            new_cards.append(new_card)
            
        updated_grid = grid_content + '\n\n      ' + '\n\n      '.join(new_cards) + '\n    '
        new_html = html[:grid_start_idx] + updated_grid + html[grid_end_idx:]
        new_html = new_html.replace('<div class=\"portfolio-grid\">', '<div class=\"portfolio-grid hide-more-mobile\" id=\"portfolioGrid\">')
        
        old_btn = '''<a href=\"https://wa.me/6281234567890?text=Halo%20Print%20Memorie%27s%2C%20saya%20ingin%20melihat%20lebih%20banyak%20contoh%20undangan\"
         target=\"_blank\" rel=\"noopener noreferrer\"
         class=\"btn btn-outline\"
         id=\"portfolio-more-btn\">
        ?? Lihat Lebih Banyak Tema
      </a>'''
        new_btn = '''<button class=\"btn btn-outline\" id=\"portfolio-more-btn\">
        ?? Lihat Lebih Banyak Tema
      </button>'''
        new_html = new_html.replace(old_btn, new_btn)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        print('Successfully duplicated cards and updated HTML.')
