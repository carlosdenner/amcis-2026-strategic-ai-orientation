"""
Step 2 -- Crosswalk Coding
Rows:    Governance requirements (NIST AI RMF + GenAI Profile + EU AI Act + OWASP LLM)
Columns: Architecture/integration controls (agentic patterns, GenAIOps, integration boundaries)
Output:  crosswalk matrix CSV + competency statement list
"""

import csv, os
from collections import Counter

BASE    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "analysis", "output")
os.makedirs(OUT_DIR, exist_ok=True)

GOVERNANCE_REQUIREMENTS = [
    # NIST AI RMF 1.0 -- GOVERN
    {"id":"NIST-GV-1","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Policies, processes, procedures and practices for mapping, measuring, and managing AI risks are in place, transparent, and implemented effectively.","trust_sub":"AI Risk Policy & Accountability","integration_sub":"Governance-as-Code / Policy Enforcement"},
    {"id":"NIST-GV-2","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Accountability structures empower appropriate teams and individuals for AI risk management.","trust_sub":"AI Governance Accountability Structures","integration_sub":"Role-Based Access & Identity Controls"},
    {"id":"NIST-GV-3","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Organizational culture considers and communicates AI risk.","trust_sub":"AI Risk Culture & Communication","integration_sub":"Human-in-the-Loop Design"},
    {"id":"NIST-GV-4","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Organizational teams are committed to a culture that considers AI risk.","trust_sub":"Organizational AI Risk Culture","integration_sub":"Change Management & GenAIOps"},
    {"id":"NIST-GV-5","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Senior leadership and board members understand and contribute to AI risk management.","trust_sub":"Board & CIO AI Risk Oversight","integration_sub":"AI Orientation Strategic Alignment"},
    {"id":"NIST-GV-6","source":"NIST AI RMF 1.0","function":"GOVERN","requirement":"Policies address AI risks from third-party software, data, and supply chain.","trust_sub":"AI Supply Chain Risk Management","integration_sub":"Resource & Supply Chain Controls"},
    # NIST AI RMF 1.0 -- MAP
    {"id":"NIST-MP-1","source":"NIST AI RMF 1.0","function":"MAP","requirement":"Context established for AI system risks through understanding of intended purpose, impacts, and deployment context.","trust_sub":"AI System Risk Contextualization","integration_sub":"Requirements-Driven Agent Pattern Selection"},
    {"id":"NIST-MP-2","source":"NIST AI RMF 1.0","function":"MAP","requirement":"Scientific findings and organizational practices integrated to characterize AI risks.","trust_sub":"Threat Intelligence Integration","integration_sub":"Adversarial Threat Modeling for Agentic Systems"},
    {"id":"NIST-MP-3","source":"NIST AI RMF 1.0","function":"MAP","requirement":"AI risks and benefits mapped and prioritized by likelihood and magnitude of impact.","trust_sub":"AI Risk Prioritization","integration_sub":"Risk-Based Architecture Decisions"},
    {"id":"NIST-MP-4","source":"NIST AI RMF 1.0","function":"MAP","requirement":"Risks and benefits understood by the organization and relevant AI actors.","trust_sub":"Stakeholder Risk Communication","integration_sub":"Transparency & Explainability Controls"},
    {"id":"NIST-MP-5","source":"NIST AI RMF 1.0","function":"MAP","requirement":"Practices and personnel for supporting AI risk identification are in place.","trust_sub":"AI Risk Identification Capability","integration_sub":"Eval & Red-Teaming Pipelines"},
    # NIST AI RMF 1.0 -- MEASURE
    {"id":"NIST-MS-1","source":"NIST AI RMF 1.0","function":"MEASURE","requirement":"AI risk measurement approaches are identified and applied.","trust_sub":"AI Risk Metrics & KPIs","integration_sub":"Evaluation & Monitoring Architecture"},
    {"id":"NIST-MS-2","source":"NIST AI RMF 1.0","function":"MEASURE","requirement":"AI system evaluated for trustworthy characteristics.","trust_sub":"Trustworthiness Evaluation","integration_sub":"LLM Evaluation Gates & Benchmarks"},
    {"id":"NIST-MS-3","source":"NIST AI RMF 1.0","function":"MEASURE","requirement":"AI system performance or assurance criteria are measured.","trust_sub":"Performance Assurance Measurement","integration_sub":"GenAIOps Monitoring & Observability"},
    {"id":"NIST-MS-4","source":"NIST AI RMF 1.0","function":"MEASURE","requirement":"Feedback about efficacy of measurement incorporated into organizational processes.","trust_sub":"Measurement Feedback Loops","integration_sub":"Continuous Improvement & MLOps Cycles"},
    # NIST AI RMF 1.0 -- MANAGE
    {"id":"NIST-MG-1","source":"NIST AI RMF 1.0","function":"MANAGE","requirement":"A plan for managing AI risks is developed, monitored, and in place.","trust_sub":"AI Risk Management Planning","integration_sub":"Incident Response & Recovery Architecture"},
    {"id":"NIST-MG-2","source":"NIST AI RMF 1.0","function":"MANAGE","requirement":"Strategies to maximize AI benefits and minimize negative impacts are planned, implemented, and documented.","trust_sub":"Risk-Benefit Optimization Governance","integration_sub":"Agentic Workflow Orchestration Controls"},
    {"id":"NIST-MG-3","source":"NIST AI RMF 1.0","function":"MANAGE","requirement":"AI risks and benefits from third-party entities are managed.","trust_sub":"Third-Party AI Risk Management","integration_sub":"Tool-Use Boundaries & API Access Controls"},
    {"id":"NIST-MG-4","source":"NIST AI RMF 1.0","function":"MANAGE","requirement":"Risk treatments including response, recovery, and communication plans are put in place.","trust_sub":"AI Incident Response & Recovery","integration_sub":"Fallback & Graceful Degradation Patterns"},
    # NIST GenAI Profile
    {"id":"NIST-GEN-1","source":"NIST GenAI Profile","function":"GOVERN","requirement":"Policies address GenAI-specific risks: hallucination, data provenance, and synthetic content.","trust_sub":"GenAI-Specific Risk Policy","integration_sub":"RAG Architecture & Data Provenance Controls"},
    {"id":"NIST-GEN-2","source":"NIST GenAI Profile","function":"MAP","requirement":"Agentic AI risks including prompt injection, tool misuse, and autonomous action boundaries are identified.","trust_sub":"Agentic Threat Surface Mapping","integration_sub":"Prompt Injection Defense & Tool-Call Validation"},
    {"id":"NIST-GEN-3","source":"NIST GenAI Profile","function":"MEASURE","requirement":"GenAI outputs evaluated for accuracy, bias, toxicity, and alignment with intended use.","trust_sub":"GenAI Output Quality Assurance","integration_sub":"Output Filtering & Content Safety Gates"},
    {"id":"NIST-GEN-4","source":"NIST GenAI Profile","function":"MANAGE","requirement":"Human oversight mechanisms in place for high-stakes agentic decisions.","trust_sub":"Human-in-the-Loop Governance","integration_sub":"Human Approval Gates in Agentic Workflows"},
    # EU AI Act
    {"id":"EU-1","source":"EU AI Act (2024/1689)","function":"GOVERNANCE","requirement":"High-risk AI systems must implement a risk management system throughout the lifecycle (Art. 9).","trust_sub":"Lifecycle Risk Management Compliance","integration_sub":"MLOps Lifecycle Governance Gates"},
    {"id":"EU-2","source":"EU AI Act (2024/1689)","function":"GOVERNANCE","requirement":"High-risk AI systems must use high-quality data with appropriate data governance (Art. 10).","trust_sub":"Data Governance & Quality Assurance","integration_sub":"Data Layer Architecture & Access Controls"},
    {"id":"EU-3","source":"EU AI Act (2024/1689)","function":"TRANSPARENCY","requirement":"High-risk AI systems must maintain technical documentation sufficient to assess compliance (Art. 11).","trust_sub":"AI System Documentation & Auditability","integration_sub":"Model Cards & System Documentation Pipelines"},
    {"id":"EU-4","source":"EU AI Act (2024/1689)","function":"TRANSPARENCY","requirement":"High-risk AI systems must enable logging of events throughout operation (Art. 12).","trust_sub":"Operational Logging & Audit Trails","integration_sub":"AI Telemetry & Observability Infrastructure"},
    {"id":"EU-5","source":"EU AI Act (2024/1689)","function":"TRANSPARENCY","requirement":"High-risk AI systems must be transparent and provide information to deployers (Art. 13).","trust_sub":"Transparency & Explainability Obligations","integration_sub":"Explainability & Interpretability Modules"},
    {"id":"EU-6","source":"EU AI Act (2024/1689)","function":"HUMAN OVERSIGHT","requirement":"High-risk AI systems must allow effective human oversight including ability to intervene and override (Art. 14).","trust_sub":"Human Override & Control Mechanisms","integration_sub":"Human-in-the-Loop Architecture Patterns"},
    {"id":"EU-7","source":"EU AI Act (2024/1689)","function":"ACCURACY & ROBUSTNESS","requirement":"High-risk AI systems must achieve appropriate accuracy, robustness, and cybersecurity (Art. 15).","trust_sub":"AI Robustness & Cybersecurity Standards","integration_sub":"Adversarial Robustness & Security Testing"},
    {"id":"EU-8","source":"EU AI Act (2024/1689)","function":"GOVERNANCE","requirement":"GPAI model providers must maintain technical documentation and comply with copyright law (Art. 53).","trust_sub":"GPAI Model Compliance & Documentation","integration_sub":"Foundation Model Governance & Vendor Management"},
    {"id":"EU-9","source":"EU AI Act (2024/1689)","function":"GOVERNANCE","requirement":"GPAI models with systemic risk must perform adversarial testing and incident reporting (Art. 55).","trust_sub":"Systemic Risk Assessment & Reporting","integration_sub":"Red-Teaming & Incident Reporting Pipelines"},
    # OWASP Top 10 LLM
    {"id":"OWASP-1","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM01 Prompt Injection: Attackers manipulate LLMs via crafted inputs to cause unintended actions.","trust_sub":"Prompt Injection Defense Capability","integration_sub":"Input Validation & Prompt Sanitization Architecture"},
    {"id":"OWASP-2","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM02 Sensitive Information Disclosure: LLMs may reveal confidential data in responses.","trust_sub":"Data Confidentiality Controls","integration_sub":"Output Filtering & PII Redaction Pipelines"},
    {"id":"OWASP-3","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM03 Supply Chain Vulnerabilities: LLM pipelines depend on third-party components with potential vulnerabilities.","trust_sub":"AI Supply Chain Security","integration_sub":"Dependency Management & Model Provenance Controls"},
    {"id":"OWASP-4","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM04 Data and Model Poisoning: Training data or model weights manipulated to introduce vulnerabilities.","trust_sub":"Training Data Integrity Assurance","integration_sub":"Data Governance & Model Integrity Verification"},
    {"id":"OWASP-5","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM05 Improper Output Handling: Insufficient validation of LLM outputs before passing to downstream systems.","trust_sub":"Output Validation Governance","integration_sub":"Output Schema Validation & Downstream Integration Guards"},
    {"id":"OWASP-6","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM06 Excessive Agency: LLM agents granted excessive permissions or autonomy beyond what is needed.","trust_sub":"Agentic Permission Governance","integration_sub":"Least-Privilege Tool-Access Architecture & Scope Boundaries"},
    {"id":"OWASP-7","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM07 System Prompt Leakage: System prompts containing sensitive instructions are exposed.","trust_sub":"System Prompt Confidentiality Controls","integration_sub":"Prompt Management & Secret Handling Architecture"},
    {"id":"OWASP-8","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM08 Vector and Embedding Weaknesses: Vulnerabilities in vector stores and embedding pipelines.","trust_sub":"RAG Security & Embedding Integrity","integration_sub":"Vector Store Access Controls & Embedding Validation"},
    {"id":"OWASP-9","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM09 Misinformation: LLMs produce factually incorrect content presented as authoritative.","trust_sub":"Hallucination & Misinformation Controls","integration_sub":"Grounding Architecture (RAG) & Fact-Checking Gates"},
    {"id":"OWASP-10","source":"OWASP Top 10 LLM","function":"SECURITY","requirement":"LLM10 Unbounded Consumption: LLM applications vulnerable to resource exhaustion and denial-of-service.","trust_sub":"Resource Consumption Governance","integration_sub":"Rate Limiting, Quotas & Cost Controls Architecture"},
]

ARCH_CONTROLS = [
    "Single-Agent Orchestration Pattern",
    "Multi-Agent Orchestration Pattern",
    "Tool-Use Boundaries & Least-Privilege Access",
    "Human-in-the-Loop Approval Gates",
    "Nondeterminism Controls & Output Validation",
    "RAG Architecture & Data Grounding",
    "GenAIOps / MLOps Lifecycle Governance",
    "Evaluation & Monitoring Infrastructure",
    "Prompt Management & Secret Handling",
    "Scalable Modular Architecture (Archetypes)",
    "AI Risk Policy & Accountability Structures",
    "Threat Modeling & Red-Teaming",
    "Incident Response & Recovery Playbooks",
    "Audit Logging & Telemetry",
    "Regulatory Compliance Documentation",
    "Supply Chain & Vendor Risk Controls",
    "Data Governance & Access Controls",
    "Human Override & Control Mechanisms",
]

CROSSWALK = {
    "NIST-GV-1": ["AI Risk Policy & Accountability Structures","Regulatory Compliance Documentation","GenAIOps / MLOps Lifecycle Governance"],
    "NIST-GV-2": ["AI Risk Policy & Accountability Structures","Tool-Use Boundaries & Least-Privilege Access","Human-in-the-Loop Approval Gates"],
    "NIST-GV-3": ["Human-in-the-Loop Approval Gates","Human Override & Control Mechanisms","Incident Response & Recovery Playbooks"],
    "NIST-GV-4": ["GenAIOps / MLOps Lifecycle Governance","AI Risk Policy & Accountability Structures"],
    "NIST-GV-5": ["AI Risk Policy & Accountability Structures","Regulatory Compliance Documentation"],
    "NIST-GV-6": ["Supply Chain & Vendor Risk Controls","Tool-Use Boundaries & Least-Privilege Access","Data Governance & Access Controls"],
    "NIST-MP-1": ["Single-Agent Orchestration Pattern","Multi-Agent Orchestration Pattern","Threat Modeling & Red-Teaming"],
    "NIST-MP-2": ["Threat Modeling & Red-Teaming","Evaluation & Monitoring Infrastructure"],
    "NIST-MP-3": ["Threat Modeling & Red-Teaming","AI Risk Policy & Accountability Structures","Evaluation & Monitoring Infrastructure"],
    "NIST-MP-4": ["Regulatory Compliance Documentation","Audit Logging & Telemetry","Human-in-the-Loop Approval Gates"],
    "NIST-MP-5": ["Threat Modeling & Red-Teaming","Evaluation & Monitoring Infrastructure","GenAIOps / MLOps Lifecycle Governance"],
    "NIST-MS-1": ["Evaluation & Monitoring Infrastructure","Audit Logging & Telemetry"],
    "NIST-MS-2": ["Evaluation & Monitoring Infrastructure","Nondeterminism Controls & Output Validation","Threat Modeling & Red-Teaming"],
    "NIST-MS-3": ["Evaluation & Monitoring Infrastructure","GenAIOps / MLOps Lifecycle Governance","Audit Logging & Telemetry"],
    "NIST-MS-4": ["GenAIOps / MLOps Lifecycle Governance","Evaluation & Monitoring Infrastructure"],
    "NIST-MG-1": ["Incident Response & Recovery Playbooks","AI Risk Policy & Accountability Structures","GenAIOps / MLOps Lifecycle Governance"],
    "NIST-MG-2": ["Single-Agent Orchestration Pattern","Multi-Agent Orchestration Pattern","Human-in-the-Loop Approval Gates","Nondeterminism Controls & Output Validation"],
    "NIST-MG-3": ["Supply Chain & Vendor Risk Controls","Tool-Use Boundaries & Least-Privilege Access"],
    "NIST-MG-4": ["Incident Response & Recovery Playbooks","Human Override & Control Mechanisms","Audit Logging & Telemetry"],
    "NIST-GEN-1": ["RAG Architecture & Data Grounding","Data Governance & Access Controls","AI Risk Policy & Accountability Structures"],
    "NIST-GEN-2": ["Prompt Management & Secret Handling","Tool-Use Boundaries & Least-Privilege Access","Threat Modeling & Red-Teaming","Single-Agent Orchestration Pattern"],
    "NIST-GEN-3": ["Nondeterminism Controls & Output Validation","Evaluation & Monitoring Infrastructure","RAG Architecture & Data Grounding"],
    "NIST-GEN-4": ["Human-in-the-Loop Approval Gates","Human Override & Control Mechanisms","Multi-Agent Orchestration Pattern"],
    "EU-1":  ["GenAIOps / MLOps Lifecycle Governance","AI Risk Policy & Accountability Structures","Regulatory Compliance Documentation"],
    "EU-2":  ["Data Governance & Access Controls","RAG Architecture & Data Grounding","Supply Chain & Vendor Risk Controls"],
    "EU-3":  ["Regulatory Compliance Documentation","Audit Logging & Telemetry","GenAIOps / MLOps Lifecycle Governance"],
    "EU-4":  ["Audit Logging & Telemetry","Evaluation & Monitoring Infrastructure"],
    "EU-5":  ["Regulatory Compliance Documentation","Nondeterminism Controls & Output Validation","Human-in-the-Loop Approval Gates"],
    "EU-6":  ["Human Override & Control Mechanisms","Human-in-the-Loop Approval Gates","Single-Agent Orchestration Pattern"],
    "EU-7":  ["Threat Modeling & Red-Teaming","Nondeterminism Controls & Output Validation","Evaluation & Monitoring Infrastructure"],
    "EU-8":  ["Supply Chain & Vendor Risk Controls","Regulatory Compliance Documentation","Data Governance & Access Controls"],
    "EU-9":  ["Threat Modeling & Red-Teaming","Incident Response & Recovery Playbooks","Audit Logging & Telemetry"],
    "OWASP-1":  ["Prompt Management & Secret Handling","Nondeterminism Controls & Output Validation","Tool-Use Boundaries & Least-Privilege Access"],
    "OWASP-2":  ["Data Governance & Access Controls","Nondeterminism Controls & Output Validation","Audit Logging & Telemetry"],
    "OWASP-3":  ["Supply Chain & Vendor Risk Controls","Data Governance & Access Controls"],
    "OWASP-4":  ["Data Governance & Access Controls","GenAIOps / MLOps Lifecycle Governance","Threat Modeling & Red-Teaming"],
    "OWASP-5":  ["Nondeterminism Controls & Output Validation","Single-Agent Orchestration Pattern","Multi-Agent Orchestration Pattern"],
    "OWASP-6":  ["Tool-Use Boundaries & Least-Privilege Access","Human-in-the-Loop Approval Gates","Single-Agent Orchestration Pattern","Multi-Agent Orchestration Pattern"],
    "OWASP-7":  ["Prompt Management & Secret Handling","Data Governance & Access Controls"],
    "OWASP-8":  ["RAG Architecture & Data Grounding","Data Governance & Access Controls","Tool-Use Boundaries & Least-Privilege Access"],
    "OWASP-9":  ["RAG Architecture & Data Grounding","Nondeterminism Controls & Output Validation","Evaluation & Monitoring Infrastructure"],
    "OWASP-10": ["Tool-Use Boundaries & Least-Privilege Access","GenAIOps / MLOps Lifecycle Governance","Evaluation & Monitoring Infrastructure"],
}

# Build crosswalk matrix
matrix_rows = []
for req in GOVERNANCE_REQUIREMENTS:
    rid = req["id"]
    applicable = set(CROSSWALK.get(rid, []))
    row = {"req_id": rid, "source": req["source"], "function": req["function"],
           "requirement": req["requirement"], "trust_sub": req["trust_sub"],
           "integration_sub": req["integration_sub"]}
    for ctrl in ARCH_CONTROLS:
        row[ctrl] = "X" if ctrl in applicable else ""
    matrix_rows.append(row)

fieldnames = ["req_id","source","function","requirement","trust_sub","integration_sub"] + ARCH_CONTROLS
out_matrix = os.path.join(OUT_DIR, "step2_crosswalk_matrix.csv")
with open(out_matrix, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(matrix_rows)
print(f"Wrote: {out_matrix} ({len(matrix_rows)} rows x {len(ARCH_CONTROLS)} control columns)")

# Derive competency statements
competencies = []
seen = set()
for req in GOVERNANCE_REQUIREMENTS:
    key = (req["trust_sub"], req["integration_sub"])
    if key not in seen:
        seen.add(key)
        trust_keywords = {"Trust","Governance","Policy","Compliance","Audit","Risk","Security","Data","Human","Logging"}
        is_trust = any(kw in req["trust_sub"] for kw in trust_keywords)
        competencies.append({
            "competency_id": f"COMP-{len(competencies)+1:02d}",
            "bundle": "Trust Readiness" if is_trust else "Integration Readiness",
            "trust_sub": req["trust_sub"],
            "integration_sub": req["integration_sub"],
            "source": req["source"],
            "source_req_id": req["id"],
            "competency_statement": (
                f"Ability to {req['trust_sub'].lower()} by designing and operating "
                f"{req['integration_sub'].lower()} to satisfy {req['source']} "
                f"{req['function']} requirements."
            ),
            "arch_controls": "; ".join(CROSSWALK.get(req["id"], [])),
        })

out_comp = os.path.join(OUT_DIR, "step2_competency_statements.csv")
with open(out_comp, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=competencies[0].keys())
    writer.writeheader()
    writer.writerows(competencies)
print(f"Wrote: {out_comp} ({len(competencies)} competency statements)")

# Control coverage analysis
ctrl_demand = Counter()
for rid, controls in CROSSWALK.items():
    for c in controls:
        ctrl_demand[c] += 1

print("\n" + "="*60)
print("STEP 2 SUMMARY -- CROSSWALK ANALYSIS")
print("="*60)
print(f"Governance requirements: {len(GOVERNANCE_REQUIREMENTS)}")
for src_label, src_key in [("NIST AI RMF 1.0","NIST AI RMF"),("NIST GenAI Profile","GenAI"),("EU AI Act","EU AI"),("OWASP Top 10 LLM","OWASP")]:
    n = sum(1 for r in GOVERNANCE_REQUIREMENTS if src_key in r["source"])
    print(f"  {src_label}: {n}")
print(f"Architecture controls: {len(ARCH_CONTROLS)}")
print(f"Competency statements: {len(competencies)}")
trust_n = sum(1 for c in competencies if c["bundle"] == "Trust Readiness")
integ_n = sum(1 for c in competencies if c["bundle"] == "Integration Readiness")
print(f"  Trust Readiness bundle:       {trust_n}")
print(f"  Integration Readiness bundle: {integ_n}")

print("\nArchitecture controls by governance demand (most required):")
for ctrl, cnt in ctrl_demand.most_common():
    print(f"  [{cnt:2d} reqs] {ctrl}")
