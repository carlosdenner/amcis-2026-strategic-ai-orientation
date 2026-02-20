"""
Central configuration for the agentic analysis pipeline.
Models, paths, token budgets.
"""

import os

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIT_DIR      = os.path.join(BASE_DIR, "Literature")
ATLAS_DIR    = os.path.join(LIT_DIR, "atlas-data")
ATLAS_DIST   = os.path.join(ATLAS_DIR, "dist", "ATLAS.yaml")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")
OUT_DIR      = os.path.join(ANALYSIS_DIR, "output")
ENRICHED_DIR = os.path.join(OUT_DIR, "enriched")

os.makedirs(ENRICHED_DIR, exist_ok=True)

# ── Models ───────────────────────────────────────────────────────────────────
# Use gpt-4.1-mini for bulk extraction (fast, cheap, 1M context)
# Use gpt-4.1 for synthesis/reasoning (higher quality)
EXTRACTION_MODEL = os.environ.get("AMCIS_EXTRACTION_MODEL", "gpt-4.1-mini")
SYNTHESIS_MODEL  = os.environ.get("AMCIS_SYNTHESIS_MODEL",  "gpt-4.1")
TEMPERATURE      = 0.2   # Low temperature for analytical consistency

# ── Token budgets ────────────────────────────────────────────────────────────
# gpt-4.1 has 1M context; we'll chunk literature to stay well within limits
MAX_CHUNK_CHARS   = 60_000   # ~15k tokens per chunk
MAX_OUTPUT_TOKENS = 16_000   # Reasonably long structured outputs

# ── Retry / rate-limit ───────────────────────────────────────────────────────
MAX_RETRIES  = 3
RETRY_DELAY  = 5  # seconds

# ── Literature file mapping ─────────────────────────────────────────────────
# Maps source IDs used in the framework to actual filenames.
# Only files that are machine-readable (HTML, MD) are included.
# PDF files are noted but skipped for automated extraction.
LITERATURE_FILES = {
    "#01": {"file": "01_Springer_CIO-Role-Digital-Transformation_Exploratory-Study.html",
            "label": "Springer (2023) — CIO Role in Digital Transformation", "type": "html"},
    "#02": {"file": "02_MISQ_Strategic-Directions-AI-Role-CIOs-Boards_MANUAL-DOWNLOAD.md",
            "label": "MISQ — Strategic Directions for AI: Role of CIOs and Boards", "type": "md"},
    "#04": {"file": "04_ScienceDirect_Responsible-AI-Governance-Review_MANUAL-DOWNLOAD.md",
            "label": "ScienceDirect — Responsible AI Governance Review", "type": "md"},
    "#05": {"file": "05_ScienceDirect_IS-Article-S0378720622000027_MANUAL-DOWNLOAD.md",
            "label": "ScienceDirect — IS Article on AI Governance", "type": "md"},
    "#06": {"file": "06_Springer_Book-Chapter-978-3-031-75266-7_9.html",
            "label": "Springer Book Chapter — AI & Digital Transformation", "type": "html"},
    "#08": {"file": "08_HBR_Gen-AI-Playbook-Organizations-2025.html",
            "label": "HBR — Gen AI Playbook for Organizations 2025", "type": "html"},
    "#09": {"file": "09_Deloitte_Tech-Trends-2026-Agentic-AI-Strategy.html",
            "label": "Deloitte — Tech Trends 2026: Agentic AI Strategy", "type": "html"},
    "#10": {"file": "10_Bizzdesign_Future-Enterprise-Architecture-AI-Integration.html",
            "label": "Bizzdesign — Future Enterprise Architecture & AI Integration", "type": "html"},
    "#11": {"file": "11_Microsoft-Learn_LLMOps-GenAIOps-Guidance.html",
            "label": "Microsoft Learn — LLMOps/GenAIOps Guidance", "type": "html"},
    "#12": {"file": "12_IBM_Data-Governance-for-AI.html",
            "label": "IBM — Data Governance for AI", "type": "html"},
    "#13": {"file": "13_AWS_Data-Governance-Age-of-GenAI.html",
            "label": "AWS — Data Governance in the Age of GenAI", "type": "html"},
    "#14": {"file": "14_CIO-MIT-CISR_Managing-Data-Like-Product.html",
            "label": "MIT CISR — Managing Data Like a Product", "type": "html"},
    "#18": {"file": "18_Bain_Widening-Talent-Gap-AI-Ambitions.html",
            "label": "Bain — Widening Talent Gap and AI Ambitions", "type": "html"},
    "#20": {"file": "20_BCG_CIOs-Role-AI-Transformation-Productivity.md",
            "label": "BCG — CIOs Role in AI Transformation and Productivity", "type": "md"},
    "#22": {"file": "22_NIST_GenAI-Profile-Risk-Management-Framework.html",
            "label": "NIST — GenAI Profile for Risk Management Framework", "type": "html"},
    "#23": {"file": "23_ISO-IEC-42001_AI-Management-System-Requirements_MANUAL-DOWNLOAD.md",
            "label": "ISO/IEC 42001 — AI Management System Requirements", "type": "md"},
    "#24": {"file": "24_ISO-IEC-23894_AI-Risk-Management-Guidance_MANUAL-DOWNLOAD.md",
            "label": "ISO/IEC 23894 — AI Risk Management Guidance", "type": "md"},
    "#25": {"file": "25_ISACA_COBIT-AI-System-Governance.html",
            "label": "ISACA — COBIT for AI System Governance", "type": "html"},
    "#26": {"file": "26_EU-AI-Act_Regulation-2024-1689.html",
            "label": "EU AI Act — Regulation 2024/1689", "type": "html"},
    "#28": {"file": "28_EDPS_GenAI-Data-Protection-Guidance.html",
            "label": "EDPS — GenAI Data Protection Guidance", "type": "html"},
    "#29": {"file": "29_OWASP_Top-10-LLM-Applications.html",
            "label": "OWASP — Top 10 for LLM Applications", "type": "html"},
    # PDF-only sources — noted for manual review, not auto-extracted
    "#03": {"file": "03_SAGE_Digital-Leadership-Dynamic-Managerial-Capability_Hossain-et-al-2025.pdf",
            "label": "SAGE/Hossain et al. (2025) — Digital Leadership", "type": "pdf"},
    "#07": {"file": "07_Gartner_CIO-Agenda-2026-Master-Agility-Risk-Tenacity.pdf",
            "label": "Gartner — CIO Agenda 2026", "type": "pdf"},
    "#15": {"file": "15_McKinsey_Deploying-Agentic-AI-Safety-Security-Playbook.pdf",
            "label": "McKinsey — Deploying Agentic AI with Safety & Security", "type": "pdf"},
    "#16": {"file": "16_McKinsey_Reconfiguring-Work-Change-Management-GenAI.pdf",
            "label": "McKinsey — Reconfiguring Work for GenAI", "type": "pdf"},
    "#17": {"file": "17_McKinsey_Superagency-Workplace-Unlock-AI-Potential.pdf",
            "label": "McKinsey — Superagency in the Workplace", "type": "pdf"},
    "#19": {"file": "19_WEF_Future-of-Jobs-Report-2025.pdf",
            "label": "WEF — Future of Jobs Report 2025", "type": "pdf"},
    "#21": {"file": "21_NIST_AI-RMF-1.0-Full-Document.pdf",
            "label": "NIST AI RMF 1.0 Full Document", "type": "pdf"},
    "#27": {"file": "27_EU-Parliament_AI-Implementation-Briefing.pdf",
            "label": "EU Parliament — AI Implementation Briefing", "type": "pdf"},
    "#31": {"file": "31_Callahan_2023_Rise-of-Chief-AI-Officer_WorkLife.pdf",
            "label": "Callahan (2023) — Rise of the Chief AI Officer", "type": "pdf"},
    "#32": {"file": "32_McKinsey_2026_New-CIO-Mandate-Strategy-Speed-Scaled-Intelligence.pdf",
            "label": "McKinsey (2026) — New CIO Mandate", "type": "pdf"},
    "#33": {"file": "33_MIT-Sloan-WEF_2019_What-Is-AI-Ethicist_WEF.pdf",
            "label": "MIT Sloan/WEF (2019) — What Is an AI Ethicist?", "type": "pdf"},
    "#34": {"file": "34_Pinski-Benlian_AI-Literacy-Measuring-Human-Competency_IS-Research.pdf",
            "label": "Pinski & Benlian — AI Literacy and Human Competency", "type": "pdf"},
}

# Sources grouped by construct relevance (for targeted extraction)
TRUST_SOURCES     = ["#22", "#26", "#29", "#25", "#28", "#23", "#24", "#04", "#05"]
INTEGRATION_SOURCES = ["#09", "#10", "#11", "#12", "#13", "#20"]
ORIENTATION_SOURCES = ["#01", "#02", "#06", "#08", "#18", "#20"]
REGULATORY_SOURCES  = ["#26", "#28", "#22", "#25", "#23", "#24"]
