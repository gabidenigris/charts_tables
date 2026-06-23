# =====================================================================
# Graficos: evolucao da inadimplencia do MEI (2018-2024)
# Fonte dos dados: Receita Federal, Estatisticas do Simples Nacional
# =====================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import font_manager

# ---------------------------------------------------------------------
# ESTILO ACADEMICO (aparencia Overleaf / pgfplots)
# Serifa estilo Computer Modern, moldura fechada, ticks para dentro.
# Tenta CMU Serif; se nao houver, usa STIX (serifa academica nativa).
# ---------------------------------------------------------------------
serif_stack = ["CMU Serif", "STIXGeneral", "DejaVu Serif"]
try:
    font_manager.findfont("CMU Serif", fallback_to_default=False)
except Exception:
    serif_stack = ["STIXGeneral", "DejaVu Serif"]

plt.rcParams.update({
    "font.family": "serif", "font.serif": serif_stack,
    "mathtext.fontset": "cm", "axes.unicode_minus": True,
    "figure.dpi": 130, "savefig.dpi": 300, "figure.figsize": (7.1, 4.5),
    "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 10.5, "ytick.labelsize": 10.5,
    # moldura fechada + ticks para dentro = cara de figura LaTeX
    "axes.spines.top": True, "axes.spines.right": True,
    "axes.edgecolor": "#222222", "axes.linewidth": 0.9,
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.top": True, "ytick.right": False,
    "xtick.major.size": 4.5, "ytick.major.size": 4.5,
    "xtick.minor.size": 2.5, "ytick.minor.size": 2.5,
    "axes.grid": True, "grid.color": "#CFCFCF",
    "grid.linewidth": 0.55, "grid.linestyle": ":",
    "legend.frameon": False, "legend.fontsize": 10.5,
    "axes.titlepad": 12,
})
# (Opcional) Para usar LaTeX de verdade no Colab, instale texlive e descomente:
# !apt-get -qq install texlive texlive-latex-extra cm-super dvipng
# plt.rcParams["text.usetex"] = True

INK   = "#1A1A1A"   # texto (quase preto, academico)
NAVY  = "#27406A"   # barras (quantidade)
BRICK = "#A23B2E"   # linha (taxa)
SRC   = "Fonte: Receita Federal, Estatisticas do Simples Nacional. Elaboracao propria."

# ---------------------------------------------------------------------
# DADOS
# ---------------------------------------------------------------------
ARQ = "Inadimplencia_MEI_2018_2024.xlsx"
df = pd.read_excel(ARQ, sheet_name="UF_serie_longa")
df["Ano"] = df["Ano"].astype(int)
br = (df.groupby("Ano")
        .agg(optantes=("Optantes MEI", "sum"),
             inadimplentes=("MEIs inadimplentes", "sum"))
        .reset_index())
br["taxa"] = br["inadimplentes"] / br["optantes"] * 100
x = br["Ano"].astype(str)

# =====================================================================
# FIGURA 1: dois paineis empilhados (eixo x compartilhado)
#   painel superior -> taxa de inadimplencia (linha)
#   painel inferior -> quantidade de inadimplentes (barras)
#   Layout que evita qualquer sobreposicao de rotulos.
# =====================================================================
fig, (axT, axB) = plt.subplots(
    2, 1, sharex=True, figsize=(7.1, 5.7),
    gridspec_kw={"height_ratios": [1.0, 1.15], "hspace": 0.10})

# --- painel superior: taxa (%) ---
axT.plot(x, br["taxa"], color=BRICK, marker="o", markersize=6,
         markerfacecolor="white", markeredgecolor=BRICK, markeredgewidth=1.6,
         linewidth=2.0, zorder=5)
axT.set_ylim(35, 49)
axT.yaxis.set_major_locator(mticker.MultipleLocator(3))
axT.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
axT.set_ylabel("Taxa de inadimplência (%)", color=INK)
axT.tick_params(colors=INK, right=True)
axT.grid(axis="y"); axT.set_axisbelow(True)
for xi, ti in zip(x, br["taxa"]):
    dy = 10 if ti >= 41 else -16
    axT.annotate(f"{ti:.1f}%", (xi, ti), textcoords="offset points",
                 xytext=(0, dy), ha="center", fontsize=9.5, color=BRICK, zorder=6)
axT.set_title("Figura 1 — Inadimplência do MEI no Brasil, 2018-2024", color=INK)

# --- painel inferior: quantidade (milhoes) ---
bars = axB.bar(x, br["inadimplentes"] / 1e6, width=0.60,
               color=NAVY, edgecolor="white", linewidth=0.6, zorder=3)
axB.set_ylim(0, 8.2)
axB.yaxis.set_major_locator(mticker.MultipleLocator(2))
axB.set_ylabel("MEIs inadimplentes (milhões)", color=INK)
axB.set_xlabel("Ano (referência: dezembro; 2024 = setembro)", color=INK)
axB.tick_params(colors=INK, right=True)
axB.grid(axis="y"); axB.set_axisbelow(True)
for b, v in zip(bars, br["inadimplentes"] / 1e6):
    axB.text(b.get_x() + b.get_width()/2, b.get_height() + 0.12, f"{v:.1f}",
             ha="center", va="bottom", fontsize=9.5, color=INK, zorder=4)

fig.text(0.012, 0.005, SRC, fontsize=8.2, color="#666666")
plt.savefig("fig1_inadimplencia_mei_brasil.png", bbox_inches="tight")
plt.show()

# =====================================================================
# FIGURA 1 (versao sobreposta): barras (quantidade) + linha (taxa)
# em eixo duplo, estilo Overleaf/LaTeX minimalista. Script autossuficiente.
#   Uso no Colab: upload de "Inadimplencia_MEI_2018_2024.xlsx" e rodar.
# =====================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

ARQ = "Inadimplencia_MEI_2018_2024.xlsx"

# ---------- estilo academico (mesmo das outras figuras) ----------
serif_stack = ["CMU Serif", "STIXGeneral", "DejaVu Serif"]
try:
    font_manager.findfont("CMU Serif", fallback_to_default=False)
except Exception:
    serif_stack = ["STIXGeneral", "DejaVu Serif"]

plt.rcParams.update({
    "font.family": "serif", "font.serif": serif_stack,
    "mathtext.fontset": "cm", "axes.unicode_minus": True,
    "figure.dpi": 130, "savefig.dpi": 300, "figure.figsize": (7.1, 4.6),
    "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 10.5, "ytick.labelsize": 10.5,
    "axes.spines.top": True, "axes.spines.right": True,
    "axes.edgecolor": "#222222", "axes.linewidth": 0.9,
    "xtick.direction": "in", "ytick.direction": "in",
    "xtick.top": True, "xtick.major.size": 4.5, "ytick.major.size": 4.5,
    "axes.grid": True, "grid.color": "#CFCFCF",
    "grid.linewidth": 0.55, "grid.linestyle": ":",
    "legend.frameon": False, "legend.fontsize": 10.5, "axes.titlepad": 12,
    "text.color": "#1A1A1A", "axes.labelcolor": "#1A1A1A",
})
INK   = "#1A1A1A"   # todo o texto (rotulos, numeros, legenda, titulo)
NAVY  = "#27406A"   # barras (quantidade) - cor so dentro do grafico
BRICK = "#A23B2E"   # linha (taxa) - cor so dentro do grafico
SRC   = "Fonte: Receita Federal, Estatísticas do Simples Nacional. Elaboração própria."

# ---------- dados ----------
df = pd.read_excel(ARQ, sheet_name="UF_serie_longa")
df["Ano"] = df["Ano"].astype(int)
br = (df.groupby("Ano")
        .agg(optantes=("Optantes MEI", "sum"),
             inadimplentes=("MEIs inadimplentes", "sum")).reset_index())
br["taxa"] = br["inadimplentes"] / br["optantes"] * 100
x = br["Ano"].astype(str)

# ---------- figura sobreposta ----------
fig, ax1 = plt.subplots()

# barras = quantidade (eixo esquerdo)
bars = ax1.bar(x, br["inadimplentes"] / 1e6, width=0.62,
               color=NAVY, edgecolor="white", linewidth=0.6, alpha=0.92, zorder=2)
ax1.set_ylim(0, 8.5)
ax1.yaxis.set_major_locator(mticker.MultipleLocator(2))
ax1.set_ylabel("MEIs inadimplentes (milhões)", color=INK)
ax1.set_xlabel("Ano (referência: dezembro; 2024 = setembro)", color=INK)
ax1.tick_params(axis="y", colors=INK)
ax1.tick_params(axis="x", colors=INK)
ax1.grid(axis="y"); ax1.set_axisbelow(True)
# rotulos de quantidade ACIMA das barras (preto)
for b, v in zip(bars, br["inadimplentes"] / 1e6):
    ax1.text(b.get_x() + b.get_width()/2, b.get_height() + 0.14, f"{v:.1f}",
             ha="center", va="bottom", fontsize=9.5, color=INK, zorder=3)

# linha = taxa (eixo direito), escala apertada para dar amplitude
ax2 = ax1.twinx()
ax2.set_ylim(36, 48)
ax2.yaxis.set_major_locator(mticker.MultipleLocator(2))
ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
ax2.set_ylabel("Taxa de inadimplência (%)", color=INK)
ax2.tick_params(axis="y", direction="in", colors=INK)
ax2.spines["right"].set_color("#222222")
ax2.plot(x, br["taxa"], color=BRICK, marker="o", markersize=6.5,
         markerfacecolor="white", markeredgecolor=BRICK, markeredgewidth=1.7,
         linewidth=2.2, zorder=6)
# rotulos da taxa em caixinha branca (texto preto); acima nos vales, abaixo nos picos
for xi, ti in zip(x, br["taxa"]):
    dy = -16 if ti >= 43 else 11
    ax2.annotate(f"{ti:.1f}%", (xi, ti), textcoords="offset points",
                 xytext=(0, dy), ha="center", fontsize=9.3, color=INK, zorder=7,
                 bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="#BBBBBB", lw=0.6))

ax1.set_title("Figura 1 — Inadimplência do MEI no Brasil, 2018-2024", color=INK)

# legenda manual (texto preto; so o simbolo carrega a cor)
leg_items = [Patch(facecolor=NAVY, edgecolor="white", label="MEIs inadimplentes (milhões)"),
             Line2D([0], [0], color=BRICK, marker="o", markerfacecolor="white",
                    markeredgecolor=BRICK, markeredgewidth=1.7, markersize=6.5,
                    linewidth=2.2, label="Taxa de inadimplência (%)")]
leg = ax1.legend(handles=leg_items, loc="upper center", bbox_to_anchor=(0.5, -0.17),
                 ncol=2, handlelength=1.8)
for txt in leg.get_texts():
    txt.set_color(INK)
fig.text(0.012, -0.04, SRC, fontsize=8.2, color="#666666")
plt.tight_layout()
plt.savefig("fig1_overlay.png", bbox_inches="tight")
plt.show()
print("ok")

# =====================================================================
# FIGURA 2: taxa de inadimplencia por regiao (mesmo estilo da Figura 1)
# =====================================================================
reg = (df.groupby(["Ano", "Região"])
         .agg(opt=("Optantes MEI", "sum"), inad=("MEIs inadimplentes", "sum"))
         .reset_index())
reg["taxa"] = reg["inad"] / reg["opt"] * 100
ordem = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
cores = {"Norte": "#22425F", "Nordeste": "#3F7CAC", "Centro-Oeste": "#88B0D3",
         "Sudeste": "#A23B2E", "Sul": "#5B8A4E"}
marc  = {"Norte": "o", "Nordeste": "s", "Centro-Oeste": "^", "Sudeste": "D", "Sul": "v"}

fig, ax = plt.subplots()
for r in ordem:
    s = reg[reg["Região"] == r].sort_values("Ano")
    ax.plot(s["Ano"].astype(str), s["taxa"], marker=marc[r], markersize=5.5,
            markerfacecolor="white", markeredgecolor=cores[r], markeredgewidth=1.4,
            linewidth=1.9, color=cores[r], label=r, zorder=4)
ax.set_ylim(25, 65)
ax.yaxis.set_major_locator(mticker.MultipleLocator(5))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%d%%"))
ax.set_title("Figura 2 — Taxa de inadimplência do MEI por região, 2018-2024", color=INK)
ax.set_xlabel("Ano (referência: dezembro; 2024 = setembro)", color=INK)
ax.set_ylabel("Taxa de inadimplência (%)", color=INK)
ax.tick_params(colors=INK, right=True)
ax.grid(axis="y")
ax.set_axisbelow(True)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=5,
          handlelength=1.8, columnspacing=1.4)
fig.text(0.012, -0.045, SRC, fontsize=8.2, color="#666666")
plt.tight_layout()
plt.savefig("fig2_inadimplencia_mei_regiao.png", bbox_inches="tight")
plt.show()

print("OK: fig1_inadimplencia_mei_brasil.png e fig2_inadimplencia_mei_regiao.png")

# =====================================================================
# TABELA 1 (estilo Overleaf/booktabs renderizado em matplotlib)
# MEIs inadimplentes por estado em 2024 (referencia: setembro/2024)
# Uso no Colab: upload de "Inadimplencia_MEI_2018_2024.xlsx" e rodar.
# =====================================================================

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager

ARQ = "Inadimplencia_MEI_2018_2024.xlsx"
DPI = 300

# ---------- fonte serifada estilo Computer Modern (mesma das figuras) ----------
serif_stack = ["CMU Serif", "STIXGeneral", "DejaVu Serif"]
try:
    font_manager.findfont("CMU Serif", fallback_to_default=False)
except Exception:
    serif_stack = ["STIXGeneral", "DejaVu Serif"]
plt.rcParams.update({"font.family": "serif", "font.serif": serif_stack,
                     "mathtext.fontset": "cm", "axes.unicode_minus": True})

# ---------- formatadores (padrao brasileiro) ----------
fmt_int = lambda v: f"{v:,.0f}".replace(",", ".")
fmt_pct = lambda v: f"{v:.1f}%".replace(".", ",")

# ---------- dados: 2024 por UF ----------
df = pd.read_excel(ARQ, sheet_name="UF_serie_longa")
d = df[df["Ano"].astype(int) == 2024].copy()
d["taxa"] = d["MEIs inadimplentes"] / d["Optantes MEI"] * 100
d = d.sort_values("MEIs inadimplentes", ascending=False)
rows = list(zip(d["UF"], d["Estado"], d["Região"],
                d["MEIs inadimplentes"], d["taxa"]))
tot_inad = d["MEIs inadimplentes"].sum()
tot_opt  = d["Optantes MEI"].sum()
tot_taxa = tot_inad / tot_opt * 100

# ---------- render booktabs ----------
def tabela(rows, titulo, subtitulo, notas, saida, dpi=300):
    n = len(rows) + 1  # +1 da linha Brasil
    fig, ax = plt.subplots(figsize=(7.4, 1.9 + 0.30 * n)); ax.axis("off")
    lh = 0.90 / (n + 6); y = 0.99
    # posicoes das colunas
    xuf, xest, xreg, xinad, xtx = 0.02, 0.09, 0.50, 0.86, 0.995

    ax.text(.5, y, titulo, ha="center", va="top", fontsize=12, fontweight="bold"); y -= lh * 1.15
    ax.text(.5, y, subtitulo, ha="center", va="top", fontsize=10.5); y -= lh * 1.45
    ax.plot([0, 1], [y, y], color="k", lw=1.6, transform=ax.transAxes); y -= lh * 0.45

    cab = [(xuf, "UF", "left"), (xest, "Estado", "left"), (xreg, "Região", "left"),
           (xinad, "MEIs inadimplentes", "right"), (xtx, "Taxa", "right")]
    for x, t, a in cab:
        ax.text(x, y, t, ha=a, va="top", fontsize=9.5, fontweight="bold")
    y -= lh
    ax.plot([0, 1], [y + lh * 0.35] * 2, color="k", lw=0.8, transform=ax.transAxes)

    for uf, est, reg, inad, tx in rows:
        ax.text(xuf,  y, uf,            ha="left",  va="top", fontsize=10)
        ax.text(xest, y, est,           ha="left",  va="top", fontsize=10)
        ax.text(xreg, y, reg,           ha="left",  va="top", fontsize=10)
        ax.text(xinad,y, fmt_int(inad), ha="right", va="top", fontsize=10)
        ax.text(xtx,  y, fmt_pct(tx),   ha="right", va="top", fontsize=10)
        y -= lh

    # linha leve separando o total
    ax.plot([0, 1], [y + lh * 0.30] * 2, color="0.75", lw=0.4, transform=ax.transAxes)
    ax.text(xest,  y, "Brasil",          ha="left",  va="top", fontsize=10, fontweight="bold")
    ax.text(xinad, y, fmt_int(tot_inad), ha="right", va="top", fontsize=10, fontweight="bold")
    ax.text(xtx,   y, fmt_pct(tot_taxa), ha="right", va="top", fontsize=10, fontweight="bold")
    y -= lh

    ax.plot([0, 1], [y + lh * 0.10] * 2, color="k", lw=1.6, transform=ax.transAxes); y -= lh * 0.9
    for nt in notas:
        ax.text(0, y, nt, ha="left", va="top", fontsize=8, style="italic"); y -= lh * 0.95

    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    plt.savefig(saida, dpi=dpi, bbox_inches="tight", facecolor="white"); plt.close()

saida = "Tabela1_inadimplencia_mei_uf_2024.png"
tabela(rows,
       "Tabela 1 — MEIs inadimplentes por unidade da federação",
       "Brasil, 2024",
       ["Fonte: elaboração própria a partir das Estatísticas do Simples Nacional (Receita Federal).",
        "Nota: inadimplente é o MEI optante sem pagamento do DAS no mês de referência;",
        "taxa = inadimplentes / optantes. Unidades ordenadas pelo número de inadimplentes."],
       saida, dpi=DPI)
print("gerado:", saida)

from IPython.display import Image
Image(filename=saida)
