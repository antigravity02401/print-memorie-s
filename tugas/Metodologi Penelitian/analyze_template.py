import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

from docx import Document

path = r"c:\laragon\www\usaha\print memorie's\tugas\Metodologi Penelitian\Format Rancangan Penelitian KSI.docx"
doc = Document(path)

print("=== PARAGRAPHS ===")
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if text:
        style = p.style.name if p.style else "None"
        align = str(p.alignment) if p.alignment else "None"
        print(f"P{i}: style={style}, align={align}")
        print(f"  text: {text[:250]}")
        for j, r in enumerate(p.runs[:4]):
            fn = r.font.name
            fs = r.font.size
            print(f"  run{j}: bold={r.bold} italic={r.italic} font={fn} size={fs} text='{r.text[:80]}'")

print()
print("=== TABLES ===")
for ti, t in enumerate(doc.tables):
    print(f"Table {ti}: rows={len(t.rows)}, cols={len(t.columns)}")
    for ri, row in enumerate(t.rows):
        cells = [c.text.strip()[:60] for c in row.cells]
        print(f"  Row {ri}: {cells}")

print()
print("=== SECTIONS ===")
for si, sec in enumerate(doc.sections):
    print(f"Section {si}: width={sec.page_width}, height={sec.page_height}")
    print(f"  margins: top={sec.top_margin}, bottom={sec.bottom_margin}, left={sec.left_margin}, right={sec.right_margin}")
