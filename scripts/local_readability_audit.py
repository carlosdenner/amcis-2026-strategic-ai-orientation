"""
Local readability audit — no LLM needed.
Runs the computational parts of Step 6 and identifies problem sentences.
"""

import os, sys, re, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from scripts.agents.step6_writing_quality import (
    _strip_markdown, _sentences, _words, _syllable_count,
    _compute_readability, _detect_passive_voice, _extract_sections
)

PAPER_PATH = os.path.join(BASE, "paper", "paper.md")

with open(PAPER_PATH, "r", encoding="utf-8") as f:
    raw = f.read()

plain = _strip_markdown(raw)
sections = _extract_sections(raw)

# ── 1. Overall readability ───────────────────────────────────────────────────
print("=" * 70)
print("READABILITY AUDIT — paper.md (v4)")
print("=" * 70)

overall = _compute_readability(plain)
print("\n  OVERALL METRICS")
for k, v in overall.items():
    print(f"    {k:<30} {v}")

# ── 2. Per-section readability ───────────────────────────────────────────────
print("\n  PER-SECTION METRICS")
print(f"  {'Section':<45} {'Words':>6} {'AvgSL':>6} {'MaxSL':>6} {'FK':>6} {'Fog':>6} {'>40w':>5}")
print("  " + "-" * 80)

sec_data = {}
for name, text in sections.items():
    if name in ("Front Matter", "References") or name.startswith(":::"):
        continue
    sec_plain = _strip_markdown(text)
    if len(sec_plain) < 100:
        continue
    m = _compute_readability(sec_plain)
    if "error" in m:
        continue
    sec_data[name] = m
    print(f"  {name:<45} {m['total_words']:>6} {m['avg_sentence_length']:>6.1f} "
          f"{m['max_sentence_length']:>6} {m['flesch_kincaid_grade']:>6.1f} "
          f"{m['gunning_fog_index']:>6.1f} {m['sentences_over_40_words']:>5}")

# ── 3. Passive voice ────────────────────────────────────────────────────────
print("\n  PASSIVE VOICE ANALYSIS")
pv = _detect_passive_voice(plain)
print(f"    Passive: {pv['passive_pct']}% ({pv['passive_sentences']}/{pv['total_sentences']})")
print(f"    Target:  {pv['target_range']}")

# ── 4. Longest sentences (the actionable part) ──────────────────────────────
print("\n  TOP 15 LONGEST SENTENCES (candidates for splitting)")
print("  " + "-" * 70)

all_sents = _sentences(plain)
sent_with_len = [(len(_words(s)), s) for s in all_sents]
sent_with_len.sort(reverse=True)

for rank, (wc, sent) in enumerate(sent_with_len[:15], 1):
    # Truncate display at 200 chars
    display = sent[:200] + ("..." if len(sent) > 200 else "")
    print(f"\n  [{rank}] {wc} words")
    print(f"      {display}")

# ── 5. Complex-word-heavy sentences ─────────────────────────────────────────
print("\n\n  TOP 10 MOST JARGON-DENSE SENTENCES (highest % complex words)")
print("  " + "-" * 70)

sent_complexity = []
for s in all_sents:
    ws = _words(s)
    if len(ws) < 10:
        continue
    n_complex = sum(1 for w in ws if _syllable_count(w) >= 3)
    pct = 100 * n_complex / len(ws)
    sent_complexity.append((pct, len(ws), s))

sent_complexity.sort(reverse=True)
for rank, (pct, wc, sent) in enumerate(sent_complexity[:10], 1):
    display = sent[:200] + ("..." if len(sent) > 200 else "")
    print(f"\n  [{rank}] {pct:.0f}% complex words ({wc} words total)")
    print(f"      {display}")

# ── 6. Save JSON ────────────────────────────────────────────────────────────
output = {
    "overall": overall,
    "per_section": sec_data,
    "passive_voice": pv,
    "longest_sentences": [{"words": wc, "text": s} for wc, s in sent_with_len[:20]],
    "most_complex_sentences": [{"complex_pct": round(p, 1), "words": wc, "text": s}
                                for p, wc, s in sent_complexity[:15]],
}
out_path = os.path.join(BASE, "data", "processed", "enriched", "step6_local_readability.json")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
print(f"\n\n  Full results saved: {out_path}")
