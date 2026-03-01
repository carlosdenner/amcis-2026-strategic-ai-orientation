"""Extract reviewer comments from a .docx file."""
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

DOCX = Path(r"C:\Users\carlo\Dropbox\Projeto - Universite de Sherbrooke\AMCIS 2026\paper-review_revEM.docx")
NS = {
    "w":  "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
}

def get_xml(zf, name):
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None

def extract_text(elem):
    """Recursively extract all text from an XML element."""
    parts = []
    for t in elem.iter(f'{{{NS["w"]}}}t'):
        if t.text:
            parts.append(t.text)
    return "".join(parts)

def extract_comments(docx_path):
    with zipfile.ZipFile(docx_path) as zf:
        # --- Parse comments ---
        comments_xml = get_xml(zf, "word/comments.xml")
        if comments_xml is None:
            print("No comments.xml found - the file may have no comments.")
            return

        comments = {}
        for c in comments_xml.findall(".//w:comment", NS):
            cid = c.get(f'{{{NS["w"]}}}id')
            author = c.get(f'{{{NS["w"]}}}author', "Unknown")
            date = c.get(f'{{{NS["w"]}}}date', "")
            text = extract_text(c)
            comments[cid] = {"author": author, "date": date, "text": text}

        # --- Parse document to find commented ranges ---
        doc_xml = get_xml(zf, "word/document.xml")
        if doc_xml is None:
            print("No document.xml found.")
            return

        # Walk all elements to reconstruct commented ranges
        body = doc_xml.find(f'{{{NS["w"]}}}body')
        range_texts = {}  # comment_id -> list of text chunks

        active_ids = set()
        for elem in body.iter():
            tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag == "commentRangeStart":
                cid = elem.get(f'{{{NS["w"]}}}id')
                active_ids.add(cid)
                if cid not in range_texts:
                    range_texts[cid] = []
            elif tag == "commentRangeEnd":
                cid = elem.get(f'{{{NS["w"]}}}id')
                active_ids.discard(cid)
            elif tag == "t" and active_ids:
                for cid in active_ids:
                    if elem.text:
                        range_texts[cid].append(elem.text)

        # --- Also extract tracked changes (insertions/deletions) ---
        insertions = []
        deletions = []
        for elem in body.iter():
            tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
            if tag == "ins":
                author = elem.get(f'{{{NS["w"]}}}author', "Unknown")
                date = elem.get(f'{{{NS["w"]}}}date', "")
                text = extract_text(elem)
                if text.strip():
                    insertions.append({"author": author, "date": date, "text": text})
            elif tag == "del":
                author = elem.get(f'{{{NS["w"]}}}author', "Unknown")
                date = elem.get(f'{{{NS["w"]}}}date', "")
                # For deletions, look for delText elements
                parts = []
                for dt in elem.iter(f'{{{NS["w"]}}}delText'):
                    if dt.text:
                        parts.append(dt.text)
                text = "".join(parts)
                if text.strip():
                    deletions.append({"author": author, "date": date, "text": text})

        # --- Print comments ---
        print(f"Found {len(comments)} comment(s) in {docx_path.name}")
        print("=" * 80)
        for cid, info in sorted(comments.items(), key=lambda x: x[1]["date"]):
            ref = "".join(range_texts.get(cid, ["(no anchored text found)"]))
            if len(ref) > 300:
                ref = ref[:300] + "..."
            print(f"\n[{info['author']}]  {info['date']}")
            print(f"  Commented on: \"{ref}\"")
            print(f"  Comment:      {info['text']}")
            print("-" * 80)

        # --- Print tracked changes ---
        if insertions:
            print(f"\n\n{'=' * 80}")
            print(f"Found {len(insertions)} tracked INSERTION(s)")
            print("=" * 80)
            for i, ins in enumerate(insertions, 1):
                print(f"\n  [{i}] [{ins['author']}] {ins['date']}")
                text = ins['text']
                if len(text) > 300:
                    text = text[:300] + "..."
                print(f"      Inserted: \"{text}\"")

        if deletions:
            print(f"\n\n{'=' * 80}")
            print(f"Found {len(deletions)} tracked DELETION(s)")
            print("=" * 80)
            for i, d in enumerate(deletions, 1):
                print(f"\n  [{i}] [{d['author']}] {d['date']}")
                text = d['text']
                if len(text) > 300:
                    text = text[:300] + "..."
                print(f"      Deleted: \"{text}\"")

if __name__ == "__main__":
    extract_comments(DOCX)
