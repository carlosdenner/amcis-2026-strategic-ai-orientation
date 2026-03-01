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
    """Return list of complete APA reference strings, one per entry."""
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
            raw_lines = f.readlines()
        # pandoc plain wraps each entry across multiple lines separated by blank lines
        # Rejoin each entry into a single string
        current = []
        for line in raw_lines:
            stripped = line.rstrip()
            if stripped:
                current.append(stripped)
            else:
                if current:
                    refs.append(' '.join(current))
                    current = []
        if current:
            refs.append(' '.join(current))
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
# Math/symbol substitution table for Unicode rendering
_MATH_SUBS = [
    (r'\\text\{([^}]+)\}', r'\1'),   # \text{word} -> word
    (r'\\rho',       'ρ'),
    (r'\\chi\^2',    'χ²'),
    (r'\\chi\^\{2\}','χ²'),
    (r'\\times',     '×'),
    (r'\\rightarrow','→'),
    (r'\\to',        '→'),
    (r'\\approx',    '≈'),
    (r'\\leq',       '≤'),
    (r'\\geq',       '≥'),
    (r'\\neq',       '≠'),
    (r'\\alpha',     'α'),
    (r'\\beta',      'β'),
    (r'\\Delta',     'Δ'),
]

def _clean_math(text):
    """Replace LaTeX math commands with Unicode equivalents."""
    for pattern, replacement in _MATH_SUBS:
        text = re.sub(pattern, replacement, text)
    # Handle superscripts like x^2 -> x²  and subscripts
    text = re.sub(r'\^\{([^}]+)\}', lambda m: m.group(1), text)  # remove braces
    text = re.sub(r'\$([^$]+)\$', lambda m: _clean_math(m.group(1)), text)  # recurse on $...$
    return text

# Bare citation author-name lookup (for sentence-opening @key references)
# Format: key -> short author string used in-text
_CITE_NAMES = {
    'teece2007':        'Teece, 2007',
    'milgrom1990':      'Milgrom and Roberts, 1990',
    'meyer1977':        'Meyer and Rowan, 1977',
    'bromley2012':      'Bromley and Powell, 2012',
    'creswell2018':     'Creswell and Plano Clark, 2018',
    'ali2023':          'Ali et al., 2023',
    'chawla2023':       'Chawla et al., 2023',
    'mckinseyai2025':   'Singla et al., 2025',
    'mckinsey2026':     'Reil-Jerenz et al., 2026',
    'bcg2025':          'Bobier et al., 2025',
    'gartner2026':      'Sánchez Reina, 2025',
    'nist2023':         'NIST, 2023',
    'euaiact2024':      'European Parliament and Council, 2024',
    'li2021':           'Li et al., 2021',
    'gregor2006':       'Gregor, 2006',
    'papagiannidis2025':'Papagiannidis et al., 2025',
    'hanelt2025':       'Hanelt et al., 2025',
    'iso42001':         'ISO/IEC 42001, 2023',
    'iso23894':         'ISO/IEC 23894, 2023',
    'pinski2024':       'Pinski et al., 2024',
    'bendig2023':       'Bendig et al., 2023',
}

def _fmt_cite_block(block_inner):
    """Convert '@key1; @key2' inner text to '(Author, year; Author, year)'."""
    keys = re.findall(r'@([\w]+)', block_inner)
    parts = [_CITE_NAMES.get(k, k) for k in keys]
    return '(' + '; '.join(parts) + ')' if parts else ''

def _clean_text(text):
    """Resolve citations, clean escapes, fix spacing artifacts."""
    text = re.sub(r'\\(\*)', r'\1', text)            # unescape \*
    text = re.sub(r'\\([\\])', r'\1', text)          # unescape \\
    # Step 1: Replace bracketed citation blocks with (Author, year) form
    text = re.sub(r'\[([^[\]]*@[\w][^[\]]*)\]',
                  lambda m: _fmt_cite_block(m.group(1)), text)
    # Step 2: Resolve remaining bare @key (sentence-opening) -> "Author (year)"
    def _resolve_bare(m):
        v = _CITE_NAMES.get(m.group(1), '')
        if not v: return ''
        # bare @key renders as "Author (year)" — split at last comma
        if ', ' in v:
            author, year = v.rsplit(', ', 1)
            return f'{author} ({year})'
        return v
    text = re.sub(r'@([\w]+)', _resolve_bare, text)
    # Step 3: Remove any empty brackets left over
    text = re.sub(r'\[\s*\]', '', text)
    # Step 4: Fix space before punctuation artifact: "word ." -> "word."
    text = re.sub(r'\s+([.,;:!?])', r'\1', text)
    # Step 5: Collapse multiple spaces
    text = re.sub(r'  +', ' ', text)
    return text.strip()

def apply_inline(para, text):
    # Pre-process: unescape, strip citations, normalise spaces
    text = _clean_text(text)
    # Split on inline markup — order matters: *** before ** before *
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
            run.text = _clean_math(part[1:-1]); run.italic = True
        else:
            run.text = _clean_math(part)

def _set_col_widths(tbl, widths_twips):
    """Set explicit column widths and borders on a table."""
    from docx.oxml import OxmlElement as _OE
    from docx.oxml.ns import qn as _qn
    tblPr = tbl._tbl.find(_qn('w:tblPr'))

    # Fix tblLook to 0000 (no conditional-format overrides that suppress borders)
    tblLook = tblPr.find(_qn('w:tblLook'))
    if tblLook is None:
        tblLook = _OE('w:tblLook'); tblPr.append(tblLook)
    tblLook.set(_qn('w:val'), '0000')
    for attr in ('w:firstRow','w:lastRow','w:firstColumn','w:lastColumn','w:noHBand','w:noVBand'):
        if tblLook.get(_qn(attr)): del tblLook.attrib[_qn(attr)]

    # Add explicit tblBorders (single line, 0.5pt = sz 4, black)
    tblBorders = tblPr.find(_qn('w:tblBorders'))
    if tblBorders is None:
        tblBorders = _OE('w:tblBorders')
        tblPr.append(tblBorders)
    else:
        for child in list(tblBorders): tblBorders.remove(child)
    for border_name in ('top','left','bottom','right','insideH','insideV'):
        b = _OE(f'w:{border_name}')
        b.set(_qn('w:val'), 'single')
        b.set(_qn('w:sz'), '4')
        b.set(_qn('w:space'), '0')
        b.set(_qn('w:color'), '000000')
        tblBorders.append(b)

    # Set fixed layout
    tblLayout = tblPr.find(_qn('w:tblLayout'))
    if tblLayout is None:
        tblLayout = _OE('w:tblLayout'); tblPr.append(tblLayout)
    tblLayout.set(_qn('w:type'), 'fixed')

    # Set total width
    tblW = tblPr.find(_qn('w:tblW'))
    if tblW is None:
        tblW = _OE('w:tblW'); tblPr.append(tblW)
    total = str(sum(widths_twips))
    tblW.set(_qn('w:w'), total); tblW.set(_qn('w:type'), 'dxa')

    # Remove existing tblGrid and replace
    old_grid = tbl._tbl.find(_qn('w:tblGrid'))
    if old_grid is not None:
        tbl._tbl.remove(old_grid)
    tblGrid = _OE('w:tblGrid')
    for w in widths_twips:
        col = _OE('w:gridCol'); col.set(_qn('w:w'), str(w))
        tblGrid.append(col)
    tbl._tbl.insert(list(tbl._tbl).index(tblPr) + 1, tblGrid)

    # Set each cell width
    for row in tbl.rows:
        for i, cell in enumerate(row.cells):
            if i < len(widths_twips):
                tcPr = cell._tc.get_or_add_tcPr()
                tcW = tcPr.find(_qn('w:tcW'))
                if tcW is None:
                    tcW = _OE('w:tcW'); tcPr.insert(0, tcW)
                tcW.set(_qn('w:w'), str(widths_twips[i]))
                tcW.set(_qn('w:type'), 'dxa')

# Column width presets (in twips, 1 inch = 1440 twips, page width 6.5in = 9360 twips)
# Table 1: 4 cols — Source | Records | Coverage | Licence
_COL_WIDTHS_T1 = [1800, 2000, 3060, 1500]   # total 8360
# Table 2: 5 cols — Variable | M1 | M2 | M3 | M4
_COL_WIDTHS_T2 = [1800, 1800, 1800, 1800, 1800]  # total 9000
# Table 3: 3 cols — ID | Proposition | Primary Evidence Anchor
_COL_WIDTHS_T3 = [480, 4560, 4320]  # total 9360
_TABLE_COL_WIDTHS = [_COL_WIDTHS_T1, _COL_WIDTHS_T2, _COL_WIDTHS_T3]
_table_count = [0]  # mutable counter

def add_table(doc, rows):
    if not rows: return
    from docx.oxml import OxmlElement as _OE
    from docx.oxml.ns import qn as _qn

    header = [c.strip() for c in rows[0].strip('|').split('|')]
    data   = [[c.strip() for c in r.strip('|').split('|')] for r in rows[1:]]
    ncols  = len(header)

    tbl = doc.add_table(rows=1 + len(data), cols=ncols)

    # Apply Table1 style (AMCIS bordered style)
    tbl.style = 'TableNormal'
    tblPr = tbl._tbl.find(_qn('w:tblPr'))
    # Set Table1 style reference
    tblStyle = tblPr.find(_qn('w:tblStyle'))
    if tblStyle is None:
        tblStyle = _OE('w:tblStyle'); tblPr.insert(0, tblStyle)
    tblStyle.set(_qn('w:val'), 'Table1')
    # Center the table
    jc = tblPr.find(_qn('w:jc'))
    if jc is None:
        jc = _OE('w:jc'); tblPr.append(jc)
    jc.set(_qn('w:val'), 'center')

    # Apply column widths for the known tables
    idx = _table_count[0]
    if idx < len(_TABLE_COL_WIDTHS):
        _set_col_widths(tbl, _TABLE_COL_WIDTHS[idx])
    _table_count[0] += 1

    # Helper: fill a cell with text using Table Text paragraph style
    def fill_cell(cell, txt, bold=False):
        cell.text = ''
        # Change paragraph style to Table Text
        p = cell.paragraphs[0]
        p.style = doc.styles['Table Text']
        apply_inline(p, txt)
        for run in p.runs:
            run.font.size = Pt(9)
            if bold:
                run.bold = True

    # Header row
    for j, txt in enumerate(header):
        fill_cell(tbl.rows[0].cells[j], txt, bold=True)

    # Data rows
    for i, rdata in enumerate(data):
        for j, txt in enumerate(rdata[:ncols]):
            fill_cell(tbl.rows[i+1].cells[j], txt, bold=False)

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
    cr = cp.add_run(caption)
    cr.bold = True
    cr.font.size = Pt(11)
    cr.font.name = 'Georgia'

# ── 6. Short title in page header ────────────────────────────────────────────
SHORT_TITLE = 'Governance Readiness Gaps in AI Deployment'  # max 8 words

def _set_header_text(doc, text):
    """Set the default page header to the short title."""
    from docx.oxml import OxmlElement as _OE
    from docx.oxml.ns import qn as _qn
    section = doc.sections[0]
    section.different_first_page_header_footer = False
    header = section.header
    # Clear existing paragraphs
    for p in header.paragraphs:
        p.clear()
    if header.paragraphs:
        hp = header.paragraphs[0]
    else:
        hp = header.add_paragraph()
    hp.style = doc.styles['Header']
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = hp.add_run(text)
    run.font.name = 'Georgia'
    run.font.size = Pt(10)

_set_header_text(doc, SHORT_TITLE)

# ── 7 (was 6). Title block ────────────────────────────────────────────────────
p = doc.add_paragraph(style='Title'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run('Governance Readiness Gaps in Organizational AI Deployment: '
              'A Triangulated Analysis of Threats, Incidents, and Practice')
r.font.size = Pt(20); r.bold = True

p = doc.add_paragraph(style='normal'); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p.add_run('Full Paper'); r2.bold = True; r2.italic = True

def _add_table_caption(doc, text):
    """Add a table caption paragraph (bold, left-aligned, Table Text style)."""
    from docx.oxml import OxmlElement as _OE
    from docx.oxml.ns import qn as _qn
    cp = doc.add_paragraph(style='TableCaption')
    cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    apply_inline(cp, text)

def _add_ref_entries(doc, ref_entries):
    from docx.oxml import OxmlElement as _OE
    from docx.oxml.ns import qn as _qn
    for ref in ref_entries:
        rp = doc.add_paragraph(style='References')
        pPr = rp._p.get_or_add_pPr()
        ind = _OE('w:ind')
        ind.set(_qn('w:left'), '720')
        ind.set(_qn('w:hanging'), '720')
        pPr.append(ind)
        rp.add_run(ref)

# ── 7. Body ──────────────────────────────────────────────────────────────────
# Table captions in the markdown appear BEFORE the table rows.
# We buffer them and emit AFTER the table.
_pending_table_caption = [None]

for block in blocks:
    btype = block[0]
    if btype == 'title':
        continue
    elif btype == 'h1':
        sec = block[1]
        if sec.lower() == 'references':
            p = doc.add_paragraph(style='Heading 1')
            r = p.add_run('References'); r.font.size = Pt(13); r.bold = True
            _add_ref_entries(doc, ref_entries)
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
        _, rows = block
        add_table(doc, rows)
        # Emit buffered caption BELOW the table
        if _pending_table_caption[0]:
            _add_table_caption(doc, _pending_table_caption[0])
            _pending_table_caption[0] = None
    elif btype == 'para':
        text = block[1].strip()
        if not text: continue
        if re.match(r'^\*\*Table\s+\d+\.\*\*', text):
            # Buffer the caption — will be emitted after the next table block
            _pending_table_caption[0] = text
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
