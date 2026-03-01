"""
Regenerate fig0_framework.png with readable fonts using matplotlib.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis('off')

# ── Colors ─────────────────────────────────────────────────────────────────
C_TR   = '#c8e6c9'   # light green
C_IR   = '#bbdefb'   # light blue
C_PROC = '#ffcdd2'   # light red/pink
C_OD   = '#ffe082'   # light amber
C_PORT = '#e8eaf6'   # light indigo
C_OVAL = '#f5f5dc'   # beige for data sources
BORDER_TR   = '#388e3c'
BORDER_IR   = '#1565c0'
BORDER_PROC = '#c62828'
BORDER_OD   = '#e65100'
BORDER_PORT = '#303f9f'

def box(ax, x, y, w, h, fc, ec, lw=1.5, radius=0.3, alpha=1.0):
    r = FancyBboxPatch((x, y), w, h,
                       boxstyle=f'round,pad=0,rounding_size={radius}',
                       facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha,
                       zorder=2)
    ax.add_patch(r)
    return r

def txt(ax, x, y, s, fs=8, bold=False, color='black', ha='center', va='center', wrap=False):
    weight = 'bold' if bold else 'normal'
    ax.text(x, y, s, fontsize=fs, fontweight=weight, color=color,
            ha=ha, va=va, zorder=3,
            wrap=wrap, multialignment='center')

def oval(ax, cx, cy, w, h, fc, ec):
    e = mpatches.Ellipse((cx, cy), w, h, facecolor=fc, edgecolor=ec, linewidth=1.5, zorder=2)
    ax.add_patch(e)

def arrow(ax, x1, y1, x2, y2, color='#555555', lw=1.5, style='->', dashed=False):
    ls = '--' if dashed else '-'
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw, linestyle=ls),
                zorder=4)

# ── 1. Organizational AI Portfolio Scope (top) ───────────────────────────────
box(ax, 3.5, 7.5, 7.0, 1.1, C_PORT, BORDER_PORT, lw=2)
txt(ax, 7.0, 8.3, 'Organizational AI Portfolio Scope', fs=11, bold=True, color=BORDER_PORT)
txt(ax, 7.0, 7.85, 'Agency-level proxy: z-scored log portfolio size + topic breadth', fs=8, color='#444')

# ── 2. Trust Readiness (TR) — left ───────────────────────────────────────────
box(ax, 0.4, 4.0, 5.2, 3.2, C_TR, BORDER_TR, lw=2)
txt(ax, 3.0, 7.0, 'Trust Readiness (TR)', fs=10, bold=True, color=BORDER_TR)

txt(ax, 0.65, 6.55, 'TR+', fs=8, bold=True, color=BORDER_TR, ha='left')
txt(ax, 1.0, 6.55, 'Surface (0–2):  Internal review · Authorization to Operate (ATO)',
    fs=7.5, ha='left', va='center', color='#333')

txt(ax, 0.65, 5.95, 'TR−', fs=8, bold=True, color=BORDER_TR, ha='left')
txt(ax, 1.0, 5.70, 'Substantive (0–7):  Impact assessment · Independent evaluation\n'
                    'Real-world testing · Bias mitigation · AI notice · Appeal process',
    fs=7.5, ha='left', va='center', color='#333')

# dashed line surface/substantive
ax.plot([0.65, 5.5], [5.25, 5.25], color=BORDER_TR, lw=1, linestyle='--', zorder=3)
txt(ax, 1.5, 4.95, 'Surface compliance ─────── Substantive safeguards', fs=7, color=BORDER_TR, ha='left')

# ── 3. Integration Readiness (IR) — right ────────────────────────────────────
box(ax, 8.4, 4.0, 5.2, 3.2, C_IR, BORDER_IR, lw=2)
txt(ax, 11.0, 7.0, 'Integration Readiness (IR)', fs=10, bold=True, color=BORDER_IR)

lines_ir = [
    'Data pipeline governance · Documentation',
    'Source code & model access · Custom code',
    'Provisioned infrastructure · Component reuse',
    'Evaluation infrastructure · Timely resources',
    '↑ Enforcement hooks for governance implementability',
]
for k, l in enumerate(lines_ir):
    bold = k == 4
    txt(ax, 8.55, 6.55 - k*0.48, l, fs=7.5, ha='left', va='center', color='#333', bold=bold)

txt(ax, 13.4, 6.85, 'IR+', fs=8, bold=True, color=BORDER_IR)

# ── 4. Operational Deployment — far right ─────────────────────────────────────
box(ax, 12.1, 5.1, 1.7, 1.5, C_OD, BORDER_OD, lw=2, radius=0.2)
txt(ax, 12.95, 5.95, 'Operational', fs=8.5, bold=True, color=BORDER_OD)
txt(ax, 12.95, 5.65, 'Deployment', fs=8.5, bold=True, color=BORDER_OD)

# ── 5. Commercial Procurement / Evaluability Constraint (center) ──────────────
box(ax, 2.8, 2.5, 8.4, 1.3, C_PROC, BORDER_PROC, lw=2)
txt(ax, 7.0, 3.55, 'Commercial Procurement  |  Evaluability Constraint', fs=10, bold=True, color=BORDER_PROC)
txt(ax, 7.0, 3.1, 'Restricts control rights · Blocks model/artifact access · Weakens substantive safeguards', fs=8, color='#333')
txt(ax, 7.0, 2.72, '← Governance Theater →', fs=8.5, bold=False, color=BORDER_PROC)
txt(ax, 11.5, 3.1, 'H4', fs=8, bold=True, color=BORDER_PROC)

# ── 6. Empirical Triangulation label ──────────────────────────────────────────
txt(ax, 7.0, 2.1, 'Empirical Triangulation', fs=9, bold=True, color='#555')

# ── 7. Data source ovals ──────────────────────────────────────────────────────
for cx, label1, label2 in [
    (2.5, 'MITRE ATLAS', '52 case studies'),
    (7.0, 'AI Incident Database (AIID)', '1,362 incidents'),
    (11.5, 'EO 13960 Federal AI', '1,757 deployments'),
]:
    oval(ax, cx, 1.1, 3.5, 1.3, C_OVAL, '#999')
    txt(ax, cx, 1.3, label1, fs=8, bold=True, color='#333')
    txt(ax, cx, 0.9, label2, fs=7.5, color='#555')

# ── 8. TR × IR interaction arrow ─────────────────────────────────────────────
ax.annotate('', xy=(8.3, 5.55), xytext=(5.7, 5.55),
            arrowprops=dict(arrowstyle='<->', color='#555', lw=1.8), zorder=4)
txt(ax, 7.0, 5.75, 'TR × IR', fs=8.5, bold=True, color='#555')
txt(ax, 7.0, 5.42, '(conditional on governance maturity)', fs=7.5, color='#555')

# ── 9. Arrows ─────────────────────────────────────────────────────────────────
# Portfolio → TR
arrow(ax, 5.0, 7.5, 3.5, 7.2, color=BORDER_PORT, lw=1.8)
# Portfolio → IR
arrow(ax, 9.0, 7.5, 10.5, 7.2, color=BORDER_PORT, lw=1.8)
# TR → Procurement (down)
arrow(ax, 3.0, 4.0, 4.5, 3.8, color=BORDER_TR, lw=1.5)
# IR → Procurement (down)
arrow(ax, 11.0, 4.0, 9.5, 3.8, color=BORDER_IR, lw=1.5)
# IR → Operational Deployment
arrow(ax, 13.6, 5.55, 13.85, 5.85, color=BORDER_IR, lw=1.8)
ax.annotate('', xy=(12.1, 5.85), xytext=(13.6, 5.55),
            arrowprops=dict(arrowstyle='->', color=BORDER_IR, lw=1.8), zorder=4)
# Procurement → Empirical
arrow(ax, 7.0, 2.5, 7.0, 2.2, color=BORDER_PROC, lw=1.5)
# Empirical ovals arrows
for cx in [2.5, 7.0, 11.5]:
    arrow(ax, 7.0, 2.1, cx, 1.8, color='#888', lw=1.2)

# ── 10. Hypothesis labels ──────────────────────────────────────────────────────
txt(ax, 0.65, 7.55, 'H1+', fs=8, bold=True, color=BORDER_TR, ha='left')
txt(ax, 0.65, 7.25, 'H2−', fs=8, bold=True, color=BORDER_TR, ha='left')
txt(ax, 8.55, 7.55, 'H3+', fs=8, bold=True, color=BORDER_IR, ha='left')

# ── 11. Legend ────────────────────────────────────────────────────────────────
legend_items = [
    (C_TR, BORDER_TR, 'Trust Readiness (TR)'),
    (C_IR, BORDER_IR, 'Integration Readiness (IR)'),
    (C_PROC, BORDER_PROC, 'Evaluability Constraint'),
    (C_OD, BORDER_OD, 'Operational Deployment'),
]
lx = 0.5
for fc, ec, label in legend_items:
    r = FancyBboxPatch((lx, 0.1), 0.35, 0.35, boxstyle='round,pad=0,rounding_size=0.05',
                       facecolor=fc, edgecolor=ec, linewidth=1.2, zorder=3)
    ax.add_patch(r)
    txt(ax, lx + 0.55, 0.27, label, fs=8, ha='left', va='center', color='#333')
    lx += 3.2

plt.tight_layout(pad=0.2)
out = r'C:\Users\carlo\Dropbox\Projeto - Universite de Sherbrooke\AMCIS 2026\paper\figures\fig0_framework.png'
plt.savefig(out, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {out}')

from PIL import Image
img = Image.open(out)
print(f'Output size: {img.size}')
