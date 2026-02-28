"""
Central configuration for the agentic analysis pipeline.
Models, paths, token budgets.
"""

import os

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR     = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIT_DIR      = os.path.join(BASE_DIR, "literature")
ATLAS_DIR    = os.path.join(BASE_DIR, "data", "raw", "atlas")
ATLAS_DIST   = os.path.join(ATLAS_DIR, "dist", "ATLAS.yaml")
SCRIPTS_DIR  = os.path.join(BASE_DIR, "scripts")
OUT_DIR      = os.path.join(BASE_DIR, "data", "processed")
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
MAX_RETRIES  = 6
RETRY_DELAY  = 15  # seconds

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

# Source type classification for triangulation checks
# Each source is classified as academic, standard, or practitioner
SOURCE_TYPES = {
    "#01": "academic",    # Springer - CIO Role in DT
    "#02": "academic",    # MISQ - AI Orientation
    "#03": "academic",    # SAGE - Dynamic Managerial Capability
    "#04": "academic",    # ScienceDirect - Responsible AI Governance
    "#05": "academic",    # ScienceDirect - IS Article on AI Governance
    "#06": "academic",    # Springer Book Chapter
    "#07": "practitioner",  # Gartner CIO Agenda
    "#08": "practitioner",  # HBR Gen AI Playbook
    "#09": "practitioner",  # Deloitte Tech Trends
    "#10": "practitioner",  # Bizzdesign EA & AI
    "#11": "practitioner",  # Microsoft Learn LLMOps
    "#12": "practitioner",  # IBM Data Governance
    "#13": "practitioner",  # AWS Data Governance
    "#14": "practitioner",  # MIT CISR Data as Product
    "#15": "practitioner",  # McKinsey Agentic AI Safety
    "#16": "practitioner",  # McKinsey Change Management
    "#17": "practitioner",  # McKinsey Superagency
    "#18": "practitioner",  # Bain Talent Gap
    "#19": "practitioner",  # WEF Future of Jobs
    "#20": "practitioner",  # BCG CIOs Role
    "#21": "standard",     # NIST AI RMF 1.0
    "#22": "standard",     # NIST GenAI Profile
    "#23": "standard",     # ISO/IEC 42001
    "#24": "standard",     # ISO/IEC 23894
    "#25": "standard",     # ISACA COBIT for AI
    "#26": "standard",     # EU AI Act
    "#27": "standard",     # EU Parliament AI Briefing
    "#28": "standard",     # EDPS GenAI Data Protection
    "#29": "standard",     # OWASP Top 10 LLM
    "#31": "practitioner",  # Callahan Chief AI Officer
    "#32": "practitioner",  # McKinsey New CIO Mandate
    "#33": "academic",     # MIT Sloan/WEF AI Ethicist
    "#34": "academic",     # Pinski & Benlian AI Literacy
}

# Sources grouped by construct relevance (for targeted extraction)
# Updated to include PDFs now that PyMuPDF extraction is available
TRUST_SOURCES = [
    "#22",  # NIST GenAI Profile
    "#26",  # EU AI Act
    "#29",  # OWASP Top 10 LLM
    "#25",  # ISACA COBIT for AI
    "#28",  # EDPS GenAI Data Protection
    "#23",  # ISO/IEC 42001
    "#24",  # ISO/IEC 23894
    "#04",  # ScienceDirect Responsible AI Governance
    "#05",  # ScienceDirect IS Article on AI Governance
    "#21",  # NIST AI RMF 1.0 Full Document (PDF)
    "#15",  # McKinsey Agentic AI Safety & Security (PDF)
    "#27",  # EU Parliament AI Implementation Briefing (PDF)
    "#33",  # MIT Sloan/WEF AI Ethicist (PDF)
]
INTEGRATION_SOURCES = [
    "#09",  # Deloitte Tech Trends 2026 Agentic AI
    "#10",  # Bizzdesign Enterprise Architecture & AI
    "#11",  # Microsoft Learn LLMOps/GenAIOps
    "#12",  # IBM Data Governance for AI
    "#13",  # AWS Data Governance Age of GenAI
    "#20",  # BCG CIOs Role in AI Transformation
    "#15",  # McKinsey Agentic AI Safety & Security (PDF)
    "#16",  # McKinsey Reconfiguring Work for GenAI (PDF)
    "#34",  # Pinski & Benlian AI Literacy (PDF)
]
ORIENTATION_SOURCES = [
    "#01",  # Springer CIO Role in Digital Transformation
    "#02",  # MISQ Strategic Directions AI Role CIOs
    "#06",  # Springer Book Chapter AI & Digital Transformation
    "#08",  # HBR Gen AI Playbook
    "#18",  # Bain Widening Talent Gap AI
    "#20",  # BCG CIOs Role in AI Transformation
    "#03",  # SAGE/Hossain Digital Leadership (PDF)
    "#07",  # Gartner CIO Agenda 2026 (PDF)
    "#17",  # McKinsey Superagency Workplace (PDF)
    "#19",  # WEF Future of Jobs Report 2025 (PDF)
    "#31",  # Callahan Rise of Chief AI Officer (PDF)
    "#32",  # McKinsey New CIO Mandate (PDF)
]
REGULATORY_SOURCES = [
    "#26",  # EU AI Act
    "#28",  # EDPS GenAI Data Protection
    "#22",  # NIST GenAI Profile
    "#25",  # ISACA COBIT for AI
    "#23",  # ISO/IEC 42001
    "#24",  # ISO/IEC 23894
    "#21",  # NIST AI RMF 1.0 Full Document (PDF)
    "#27",  # EU Parliament AI Implementation Briefing (PDF)
]
