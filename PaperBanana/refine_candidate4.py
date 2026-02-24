"""
Refine framework_candidate_4 — fix spelling, alignment, and spacing.
Generates 3 polished variants via gpt-image-1.
"""

import asyncio, base64, os, sys
from pathlib import Path
from openai import AsyncOpenAI

OUTPUT_DIR = Path(__file__).parent.parent / "paper" / "figures"

# The refined description (based on candidate 4's critic-refined version)
# with EXPLICIT corrections for every known issue.
REFINED_PROMPT = """
Generate a professional, publication-quality academic conceptual framework
diagram on a PURE WHITE background.  The diagram must be crisp, perfectly
aligned, and free of ANY spelling errors.  Use a clean sans-serif font
(like Helvetica or Arial) throughout.

=== EXACT LAYOUT (top to bottom, centered) ===

1. TOP — CIO-Driven AI Orientation
   • A stylized icon: silhouette of a person with a gear/cog above their head.
   • Below the icon, bold navy-blue text: "CIO-Driven AI Orientation"
     (spelled exactly like this — no typos).
   • A solid dark arrow points straight down from this label.

2. MIDDLE — Two side-by-side boxes of EQUAL width, perfectly aligned
   horizontally, with a small gap between them:

   LEFT BOX — Trust Readiness (TR)
   • Light green background, rounded corners.
   • Top-left corner: a small shield icon (✓ check inside).
   • Header in bold dark-green: "Trust Readiness (TR)"
   • Bullet list in dark text, each on its own line:
       – Risk Management
       – Compliance
       – Threat Modeling
       – Incident Response
       – Stakeholder Accountability
     (All words spelled correctly.)

   RIGHT BOX — Integration Readiness (IR)  ← note "Readiness" not "Readines"
   • Light blue background, rounded corners, same height as left box.
   • Top-left corner: a small cloud/network icon.
   • Header in bold deep-blue: "Integration Readiness"
   • Bullet list in dark text:
       – Data Pipeline Governance
       – Evaluation Infrastructure
       – Deployment Controls
       – Code/Model Accessibility
     (Spell "Accessibility" correctly — two 's', two 'i'.)

   BETWEEN the two boxes, a double-headed dashed arrow labeled:
       "TR × IR"   (on first line)
       "Conditional on Governance Maturity"  (on second line, italic, smaller)

3. BELOW the two boxes — Opacity Barrier
   • A grey rounded rectangle with a closed padlock icon.
   • Text inside: "Opacity Barrier" (bold)
   • Smaller text below or inside: "Commercial Procurement"
   • A solid arrow goes from the middle section down into this barrier box.

4. BELOW the barrier — Governance Theater callout
   • A red/coral dashed-border annotation near the barrier reads
     "Governance Theater" in red italic font.
   • Optionally a curly brace or bracket connecting it to the barrier.

5. BELOW — Empirical Triangulation (three items in a row, evenly spaced)
   • A label "Empirical Triangulation" centered above them.
   • Three evenly-spaced rounded boxes/circles, each with an icon and label:

     (a) 🔍 MITRE ATLAS Threats — "52 case studies"
     (b) ⚠  AI Incident Database (AIID) — "1,362 incidents"
         ^^^  note: COMMA not period → "1,362"
     (c) 📋 EO 13960 Federal AI Inventory — "1,757 deployments"
         ^^^  note: COMMA not period → "1,757"

   • All three boxes must be the SAME width and aligned on the same baseline.

6. BOTTOM — Realized AI Value
   • A vibrant green bar-chart icon next to bold text: "Realized AI Value"
   • Connected from the empirical section with solid lines/arrows.

=== CRITICAL QUALITY REQUIREMENTS ===
• NO spelling mistakes anywhere: double-check every word.
• ALL boxes and text perfectly horizontally and vertically aligned.
• Consistent margins and padding throughout.
• Professional, academic style — suitable for a peer-reviewed IS journal.
• Aspect ratio approximately 16:9 (landscape).
• No decorative clutter — clean, minimal, information-dense.
• Use thin lines (1–2 pt), not thick ones.
• Numbers use COMMAS as thousand separators (1,362 not 1.362).
"""

NUM_VARIANTS = 3

async def main():
    client = AsyncOpenAI()   # uses OPENAI_API_KEY from env

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  Refining candidate 4 — generating {NUM_VARIANTS} polished variants")
    print(f"{'='*60}\n")

    tasks = []
    for i in range(NUM_VARIANTS):
        tasks.append(generate_one(client, i))

    await asyncio.gather(*tasks)

    print(f"\n{'='*60}")
    print(f"  Done! Check paper/figures/framework_refined_4_*.png")
    print(f"{'='*60}\n")


async def generate_one(client: AsyncOpenAI, idx: int):
    try:
        resp = await client.images.generate(
            model="gpt-image-1",
            prompt=REFINED_PROMPT,
            n=1,
            size="1536x1024",         # landscape ≈ 3:2
            quality="high",
        )
        # gpt-image-1 returns base64 by default
        b64 = resp.data[0].b64_json
        if not b64:
            print(f"  ✗ Variant {idx}: no image data returned")
            return

        img_bytes = base64.b64decode(b64)
        out_path = OUTPUT_DIR / f"framework_refined_4_{idx}.png"
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"  ✓ Variant {idx} saved → {out_path.name}  ({len(img_bytes)//1024} KB)")

    except Exception as e:
        print(f"  ✗ Variant {idx} failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
