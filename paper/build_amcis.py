"""
Build AMCIS-compliant docx from paper.md using python-docx.
Populates the AMCIS template with correct styles.
Run: python build_amcis.py
Outputs: paper_amcis.docx, paper_submission.pdf
"""

import re, os, subprocess, time
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

PAPER_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE  = os.path.join(PAPER_DIR, '..', 'AMCIS-2026-Full-ERF-Template_Initial-submission-1.docx')
OUTPUT    = os.path.join(PAPER_DIR, 'paper_amcis.docx')
PDF_OUT   = os.path.join(PAPER_DIR, 'paper_submission.pdf')

# ── 1. Read paper.md ─────────────────────────────────────────────────────────
with open(os.path.join(PAPER_DIR, 'paper.md'), encoding='utf-16') as f:
    md = f.read()

md = re.sub(r'^---.*?---\s*', '', md, flags=re.DOTALL)
md = re.sub(r'<!--.*?-->', '', md, flags=re.DOTALL)
md = re.sub(r'^\s*---\s*$', '', md, flags=re.MULTILINE)
lines = [l.rstrip() for l in md.splitlines()]

# ── 2. Parse into blocks ─────────────────────────────────────────────────────
blocks = []
i = 0
while i < len(lines):
    line = lines[i]
    if not line.strip():
        i += 1; continue
    if line.startswith('# '):
        blocks.append(('title', line[2:].strip()))
    elif line.startswith('## '):
        blocks.append(('h1', line[3:].strip()))
    elif line.startswith('### '):
        blocks.append(('h2', line[4:].strip()))
    elif line.startswith('#### '):
        blocks.append(('h3', line[5:].strip()))
    elif line.startswith('!['):
        m = re.match(r'!\[([^\]]*)\]\(([^)]+)\)(\{.*?\})?', line)
        if m:
            blocks.append(('figure', m.group(1), m.group(2), m.group(3) or ''))
    elif line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].startswith('|'):
            if not re.match(r'^\|[-|: ]+\|$', lines[i]):
                rows.append(lines[i])
            i += 1
        blocks.append(('table', rows))
        continue
    elif re.match(r'^\*Full Paper\*', line):
        i += 1; continue
    elif line.strip() in (':::', '::: {#refs}'):
        i += 1; continue
    else:
        blocks.append(('para', line))
    i += 1

print(f'Parsed {len(blocks)} blocks')

# ── 3. Generate formatted references via pandoc ───────────────────────────────
def get_formatted_references():
    with open(os.path.join(PAPER_DIR, 'paper.md'), encoding='utf-16') as f:
        paper_text = f.read()
    keys = list(dict.fromkeys(re.findall(r'@([\w]+)', paper_text)))
    mini_md = '---\nbibliography: references.bib\ncsl: apa.csl\nnocite: |\n'
    for k in keys:
        mini_md += f'  @{k}\n'
    mini_md += '---\n\n::: {#refs}\n:::\n'
    tmp_in  = os.path.join(PAPER_DIR, '_refs_tmp.md')
    tmp_out = os.path.join(PAPER_DIR, '_refs_tmp.txt')
    with open(tmp_in, 'w', encoding='utf-8') as f:
        f.write(mini_md)
    r = subprocess.run(
        ['pandoc', '_refs_tmp.md', '-o', '_refs_tmp.txt', '--citeproc', '-t', 'plain'],
        cwd=PAPER_DIR, capture_output=True, text=True
    )
    refs = []
    if r.returncode == 0 and os.path.exists(tmp_out):
        with open(tmp_out, encoding='utf-8') as f:
            refs = [l.rstrip() for l in f.readlines() if l.strip()]
    for tmp in [tmp_in, tmp_out]:
        if os.path.exists(tmp): os.remove(tmp)
    return refs

print('Generating formatted references...')
ref_entries = get_formatted_references()
print(f'  {len(ref_entries)} reference lines')

# ── 4. Open template, clear body ─────────────────────────────────────────────
doc = Document(TEMPLATE)
body = doc.element.body
sectPr = body.find(qn('w:sectPr'))
for child in list(body):
    if child.tag != qn('w:sectPr'):
        body.remove(child)

# ── 5. Helpers ───────────────────────────────────────────────────────────────
def apply_inline(para, text):
    text = re.sub(r'\\(\*)', r'\1', text)
    pattern = re.compile(r'(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\$[^$]+\$)')
    parts = pattern.split(text)
    for part in parts:
        if not part: continue
        run = para.add_run()
        if part.startswith('***') and part.endswith('***'):
            run.text = part[3:-3]; run.bold = True; run.italic = True
        elif part.startswith('**') and part.endswith('**'):
            run.text = part[2:-2]; run.bold = True
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            run.text = part[1:-1]; run.italic = True
        elif part.startswith('`') and part.endswith('`'):
            run.text = part[1:-1]; run.font.name = 'Courier New'
        elif part.startswith('$') and part.endswith('$'):
            run.text = part[1:-1]; run.italic = True
        else:
            cleaned = re.sub(r'\[[@\w;,\s]+\]', '', part)
            cleaned = re.sub(r'@[\w]+', '', cleaned)
            run.text = cleaned

def add_table(doc, rows):
    if not rows: return
    header = [c.strip() for c in rows[0].strip('|').split('|')]
    data   = [[c.strip() for c in r.strip('|').split('|')] for r in rows[1:]]
    ncols  = len(header)
    tbl = doc.add_table(rows=1 + len(data), cols=ncols)
    tbl.style = 'TableNormal'
    for j, txt in enumerate(header):
        cell = tbl.rows[0].cells[j]; cell.text = ''
        r = cell.paragraphs[0].add_run(txt); r.bold = True; r.font.size = Pt(9)
    for i, rdata in enumerate(data):
        for j, txt in enumerate(rdata[:ncols]):
            cell = tbl.rows[i+1].cells[j]; cell.text = ''
            r = cell.paragraphs[0].add_run(txt); r.font.size = Pt(9)

def add_figure(doc, caption, path, attrs):
    img = os.path.join(PAPER_DIR, path)
    if not os.path.exists(img):
        print(f'  WARN: missing image {path}'); return
    width = Inches(5.5)
    wm = re.search(r'width=(\d+)%', attrs)
    if wm: width = Inches(6.5 * int(wm.group(1)) / 100)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    try: p.add_run().add_picture(img, width=width)
    except Exception as e: print(f'  WARN: {e}')
    cp = doc.add_paragraph(style='FigureCaption')
    cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cr = cp.add_run(caption); cr.bold = True; cr.font.size = Pt(10)

# ── 6. Title block ───────────────────────────────────────────────────────────
p = doc.add_paragraph(style='Title'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('AMCIS 2026 Reno'); r.font.size = Pt(20); r.bold = True

p = doc.add_paragraph(style='Title'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Governance Readiness Gaps in Organizational AI Deployment: '
              'A Triangulated Analysis of Threats, Incidents, and Practice')
r.font.size = Pt(20); r.bold = True

p = doc.add_paragraph(style='normal'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r1 = p.add_run('Indicate Submission Type: '); r1.bold = True; r1.italic = True
r2 = p.add_run('Full Paper'); r2.italic = True
r2.font.color.rgb = RGBColor(0xC0, 0x50, 0x00)

# ── 7. Body ──────────────────────────────────────────────────────────────────
for block in blocks:
    btype = block[0]
    if btype == 'title':
        continue
    elif btype == 'h1':
        sec = block[1]
        if sec.lower() == 'references':
            p = doc.add_paragraph(style='Heading 1'); p.add_run('References')
            for ref in ref_entries:
                rp = doc.add_paragraph(style='References'); rp.add_run(ref)
        else:
            p = doc.add_paragraph(style='Heading 1'); apply_inline(p, sec)
    elif btype == 'h2':
        p = doc.add_paragraph(style='Heading 2'); apply_inline(p, block[1])
    elif btype == 'h3':
        p = doc.add_paragraph(style='Heading 3'); apply_inline(p, block[1])
    elif btype == 'figure':
        _, caption, path, attrs = block
        add_figure(doc, caption, path, attrs)
    elif btype == 'table':
        _, rows = block; add_table(doc, rows)
    elif btype == 'para':
        text = block[1].strip()
        if not text: continue
        if re.match(r'^\*\*Table\s+\d+', text):
            p = doc.add_paragraph(style='TableCaption')
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT; apply_inline(p, text)
        else:
            p = doc.add_paragraph(style='normal'); apply_inline(p, text)

if sectPr is not None:
    body.append(sectPr)

doc.save(OUTPUT)
print(f'Saved docx: {OUTPUT}  ({os.path.getsize(OUTPUT):,} bytes)')

# ── 8. Export PDF via Word ────────────────────────────────────────────────────
print('Exporting PDF via Word...')
try:
    import win32com.client
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    wd = word.Documents.Open(os.path.abspath(OUTPUT))
    time.sleep(2)
    wd.SaveAs(os.path.abspath(PDF_OUT), FileFormat=17)
    wd.Close(False)
    word.Quit()
    print(f'Saved pdf:  {PDF_OUT}  ({os.path.getsize(PDF_OUT):,} bytes)')
except Exception as e:
    print(f'PDF export failed (Word not available): {e}')
    print('Falling back to lualatex...')
    utf8 = os.path.join(PAPER_DIR, 'paper_utf8.md')
    with open(os.path.join(PAPER_DIR, 'paper.md'), encoding='utf-16') as f:
        txt = f.read()
    with open(utf8, 'w', encoding='utf-8') as f:
        f.write(txt)
    subprocess.run(
        ['pandoc', 'paper_utf8.md', '-o', 'paper_submission.pdf',
         '--citeproc', '--pdf-engine=lualatex',
         '-V', 'geometry:margin=1in', '-V', 'fontsize=10pt',
         '-V', 'mainfont=Times New Roman'],
        cwd=PAPER_DIR
    )
    if os.path.exists(utf8):
        os.remove(utf8)
