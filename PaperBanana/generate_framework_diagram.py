"""
Generate 5 candidate conceptual framework diagrams for the AMCIS 2026 paper.
Uses PaperBanana pipeline with OpenAI gpt-4o + gpt-image-1.
"""

import asyncio
import base64
import json
import sys
from pathlib import Path
from io import BytesIO

# ── Paper content ──────────────────────────────────────────────────────────
METHOD_CONTENT = r"""
## Theoretical Framework

Upper echelons theory posits that organizational outcomes reflect the cognitive orientations of top executives. In AI contexts, the CIO role has evolved from technology steward to strategic partner, and CIO centrality together with board AI awareness significantly influences a firm's strategic AI orientation. We take CIO-driven strategic AI orientation as a contextual assumption; our propositions focus on the downstream capability mechanisms — trust readiness and integration readiness — that convert orientation into realized AI value.

Strategic orientation is necessary but insufficient. The dynamic managerial capabilities (DMC) framework identifies managerial human capital, social capital, and cognition as micro-foundations of capability building. We complement DMC with a governance-as-capability perspective, conceptualizing governance not as a static compliance constraint but as a dynamic organizational capability.

We operationalize this framework through two capability bundles:

**Trust Readiness (TR)** encompasses risk management, compliance, adversarial threat modeling, incident response, and stakeholder accountability. TR spans a continuum from surface compliance (internal review boards, authorization to operate) to substantive safeguards (impact assessment, independent evaluation, bias mitigation). Surface approvals alone cannot interact productively with architecture because they impose no operational demands on the system.

**Integration Readiness (IR)** is the architecture capability bundle encompassing data pipeline governance, evaluation infrastructure, deployment controls, and code/model accessibility. Critically, IR supplies the enforcement hooks that make governance actionable: without telemetry infrastructure, audit logging is impossible; without evaluation pipelines, bias testing cannot be conducted; without code access, independent review is foreclosed. The resulting boundary condition is governance implementability: the degree to which an organization possesses the control rights and technical access needed to execute governance routines.

We theorize that TR and IR are strategic complements: the marginal return to each increases when the other is present. Governance controls require architectural hooks to be enforceable; architectural patterns require governance boundaries to be safe. This complementarity is conditional on governance maturity: when TR remains theatrical (surface compliance without operational substance), it cannot interact productively with IR.

**Commercial Procurement as Opacity Barrier:** When procurement or outsourcing restricts access to model artifacts, telemetry, and evaluation interfaces, governance implementability collapses and decoupling persists even under mandate. Vendor-developed systems are 71% less likely to report impact assessment (OR = 0.29, p < 0.001).

### Propositions
- P1: TR and IR are strategic complements, but complementarity is contingent on governance maturity.
- P2: Under regulatory pressure, risk-tiering does not reliably produce higher deep safeguards; organizations exhibit governance theater.
- P3: Commercially procured AI reduces governance implementability via a transparency deficit.
- E1: AI harms exhibit sector-specific fingerprints that governance investment does not match.

### Empirical Triangulation (three data sources):
1. MITRE ATLAS: 52 adversarial case studies → what CAN go wrong (threat landscape)
2. AI Incident Database: 1,362 incidents → what HAS gone wrong (realized harms)
3. EO 13960 Federal AI Inventory: 1,757 deployments → what IS being done (governance practice)
"""

CAPTION = (
    "Conceptual framework: CIO-driven AI Orientation flows into two capability bundles — "
    "Trust Readiness (TR: governance safeguards from surface compliance to substantive depth) "
    "and Integration Readiness (IR: architecture hooks enabling enforcement). "
    "TR × IR complementarity is conditional on governance maturity. "
    "Commercial procurement creates an opacity barrier that blocks governance implementability. "
    "When TR remains theatrical, governance theater persists as institutional decoupling. "
    "Three empirical lenses triangulate the analysis: MITRE ATLAS (threats), AIID (incidents), "
    "and EO 13960 (practice). The pathway leads to Realized AI Value."
)

NUM_CANDIDATES = 5
OUTPUT_DIR = Path(__file__).parent.parent / "paper" / "figures"

# ── Pipeline ───────────────────────────────────────────────────────────────

async def main():
    # Ensure imports work from PaperBanana dir
    sys.path.insert(0, str(Path(__file__).parent))

    from utils import config
    from utils.paperviz_processor import PaperVizProcessor
    from agents.planner_agent import PlannerAgent
    from agents.visualizer_agent import VisualizerAgent
    from agents.stylist_agent import StylistAgent
    from agents.critic_agent import CriticAgent
    from agents.retriever_agent import RetrieverAgent
    from agents.vanilla_agent import VanillaAgent
    from agents.polish_agent import PolishAgent

    exp_config = config.ExpConfig(
        dataset_name="Demo",
        split_name="demo",
        exp_mode="demo_planner_critic",   # Planner → Visualizer → Critic loop
        retrieval_setting="none",          # No reference dataset needed
        model_name="gpt-4o",
        image_model_name="gpt-image-1",
        work_dir=Path(__file__).parent,
        max_critic_rounds=2,
    )

    processor = PaperVizProcessor(
        exp_config=exp_config,
        vanilla_agent=VanillaAgent(exp_config=exp_config),
        planner_agent=PlannerAgent(exp_config=exp_config),
        visualizer_agent=VisualizerAgent(exp_config=exp_config),
        stylist_agent=StylistAgent(exp_config=exp_config),
        critic_agent=CriticAgent(exp_config=exp_config),
        retriever_agent=RetrieverAgent(exp_config=exp_config),
        polish_agent=PolishAgent(exp_config=exp_config),
    )

    # Build candidate inputs
    data_list = []
    for i in range(NUM_CANDIDATES):
        data_list.append({
            "filename": f"framework_candidate_{i}",
            "caption": CAPTION,
            "content": METHOD_CONTENT,
            "visual_intent": CAPTION,
            "additional_info": {"rounded_ratio": "16:9"},
            "max_critic_rounds": 2,
            "candidate_id": i,
        })

    print(f"\n{'='*60}")
    print(f"  Generating {NUM_CANDIDATES} framework diagram candidates")
    print(f"  Model (text):  {exp_config.model_name}")
    print(f"  Model (image): {exp_config.image_model_name}")
    print(f"  Pipeline:      {exp_config.exp_mode}")
    print(f"  Critic rounds: {exp_config.max_critic_rounds}")
    print(f"{'='*60}\n")

    results = []
    async for result_data in processor.process_queries_batch(
        data_list, max_concurrent=5, do_eval=False
    ):
        results.append(result_data)

    # Save outputs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    saved = 0
    for r in results:
        cid = r.get("candidate_id", saved)
        # Find the best image key
        img_key = r.get("eval_image_field", "")
        b64 = r.get(img_key, "") if img_key else ""

        if not b64 or len(b64) < 100:
            # Fallback: search for any base64 image key
            for k in sorted(r.keys(), reverse=True):
                if k.endswith("_base64_jpg") and r[k] and len(r[k]) > 100:
                    b64 = r[k]
                    img_key = k
                    break

        if b64 and len(b64) > 100:
            out_path = OUTPUT_DIR / f"framework_candidate_{cid}.png"
            img_bytes = base64.b64decode(b64)
            with open(out_path, "wb") as f:
                f.write(img_bytes)
            print(f"  ✓ Saved candidate {cid} → {out_path.name}  ({len(img_bytes)//1024} KB)")
            saved += 1
        else:
            print(f"  ✗ Candidate {cid}: no image produced (key={img_key})")

    # Also dump the planner descriptions for reference
    desc_path = OUTPUT_DIR / "framework_candidates_descriptions.json"
    desc_data = []
    for r in results:
        entry = {"candidate_id": r.get("candidate_id")}
        for k in sorted(r.keys()):
            if "desc" in k and not k.endswith("base64_jpg"):
                entry[k] = r.get(k, "")
        desc_data.append(entry)
    with open(desc_path, "w", encoding="utf-8") as f:
        json.dump(desc_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"  Done! {saved}/{NUM_CANDIDATES} candidates saved to paper/figures/")
    print(f"  Descriptions saved to {desc_path.name}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(main())
