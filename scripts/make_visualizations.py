"""
make_visualizations.py

Generates the four core visualizations for the project's "Findings" section.

Charts produced (all saved to outputs/figures/):
    1. salary_vs_pie_scatter.png  - salary vs PIE, colored by archetype
    2. avg_etd_by_archetype.png   - bar chart of mean EtD-PIE per archetype
    3. top_etd_leaderboard.png    - top 20 players by EtD-PIE
    4. salary_by_archetype_box.png - salary distribution per archetype

Inputs:
    data/processed/nba_merged_with_archetypes.csv

Outputs:
    outputs/figures/*.png
"""

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Force UTF-8 output for terminal (handles accented player names)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)

DATA_IN = Path("data/processed/nba_merged_with_archetypes.csv")
FIG_DIR = Path("outputs/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)


# Style
sns.set_theme(style="whitegrid", context="notebook")
plt.rcParams["figure.dpi"] = 100
plt.rcParams["savefig.dpi"] = 200
plt.rcParams["savefig.bbox"] = "tight"

# Consistent archetype color order so all charts use the same palette
ARCHETYPE_ORDER = [
    "Veteran Star",
    "Prime Star",
    "High-Volume Scorer",
    "Sixth Man",
    "3-and-D Wing",
    "Defensive Specialist",
    "Rookie Contributor",
    "Role Player",
]
ARCHETYPE_PALETTE = sns.color_palette("tab10", n_colors=len(ARCHETYPE_ORDER))
ARCHETYPE_COLORS = dict(zip(ARCHETYPE_ORDER, ARCHETYPE_PALETTE))


# Load
print("Loading data...")
df = pd.read_csv(DATA_IN)
print(f"  {len(df)} players")

# Convert salary to millions for nicer axis labels
df["salary_m"] = df["salary"] / 1_000_000


# Chart 1: Salary vs PIE scatter, colored by archetype
print("\n[1/4] Salary vs PIE scatter...")
fig, ax = plt.subplots(figsize=(11, 7))

for archetype in ARCHETYPE_ORDER:
    subset = df[df["archetype"] == archetype]
    if subset.empty:
        continue
    ax.scatter(
        subset["salary_m"],
        subset["pie"],
        label=f"{archetype} (n={len(subset)})",
        color=ARCHETYPE_COLORS[archetype],
        alpha=0.7,
        s=50,
        edgecolor="white",
        linewidth=0.5,
    )

# Notable players
notable = df.nlargest(5, "pie")  # the league's most productive
for _, row in notable.iterrows():
    ax.annotate(
        row["player_name"],
        (row["salary_m"], row["pie"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8,
        alpha=0.8,
    )

ax.set_xlabel("2025-26 Salary (USD, millions)")
ax.set_ylabel("PIE (Player Impact Estimate)")
ax.set_title("Salary vs Production: Where the NBA Spends Its Money", fontsize=13, weight="bold")
ax.legend(loc="upper left", frameon=True, fontsize=8, framealpha=0.95)
plt.tight_layout()
plt.savefig(FIG_DIR / "salary_vs_pie_scatter.png")
plt.close()
print(f"  -> {FIG_DIR / 'salary_vs_pie_scatter.png'}")


# Chart 2: Average EtD by archetype
print("\n[2/4] Average EtD by archetype bar chart...")
avg_etd = (
    df.groupby("archetype")["etd_pie"]
    .mean()
    .reset_index()
    .sort_values("etd_pie", ascending=True)  # ascending so worst is at bottom of horizontal chart
)

fig, ax = plt.subplots(figsize=(10, 6))
colors = [ARCHETYPE_COLORS[a] for a in avg_etd["archetype"]]
ax.barh(avg_etd["archetype"], avg_etd["etd_pie"], color=colors, edgecolor="black", linewidth=0.5)

for i, val in enumerate(avg_etd["etd_pie"]):
    ax.text(val + 0.05, i, f"{val:.2f}", va="center", fontsize=9)

ax.set_xlabel("Average EtD-PIE (PIE × 100 per $M salary)")
ax.set_ylabel("Archetype")
ax.set_title("Best Value by Player Archetype", fontsize=13, weight="bold")
ax.set_xlim(0, avg_etd["etd_pie"].max() * 1.15)
plt.tight_layout()
plt.savefig(FIG_DIR / "avg_etd_by_archetype.png")
plt.close()
print(f"  -> {FIG_DIR / 'avg_etd_by_archetype.png'}")


# Chart 3: Top 20 EtD leaderboard
print("\n[3/4] Top 20 EtD leaderboard...")
top20 = df.nlargest(20, "etd_pie").sort_values("etd_pie", ascending=True)

fig, ax = plt.subplots(figsize=(11, 9))
colors = [ARCHETYPE_COLORS[a] for a in top20["archetype"]]
ax.barh(top20["player_name"], top20["etd_pie"], color=colors, edgecolor="black", linewidth=0.5)

# Add salary and PIE annotations to the right of each bar
for i, (_, row) in enumerate(top20.iterrows()):
    label = f"PIE {row['pie']:.3f}, ${row['salary']/1_000_000:.2f}M, {row['archetype']}"
    ax.text(row["etd_pie"] + 1, i, label, va="center", fontsize=8, color="#333333")

ax.set_xlabel("EtD-PIE (PIE × 100 per $M salary)")
ax.set_ylabel("Player")
ax.set_title("NBA Cap Efficiency Leaderboard: Top 20 Players by EtD-PIE", fontsize=13, weight="bold")
ax.set_xlim(0, top20["etd_pie"].max() * 1.5)
plt.tight_layout()
plt.savefig(FIG_DIR / "top_etd_leaderboard.png")
plt.close()
print(f"  -> {FIG_DIR / 'top_etd_leaderboard.png'}")


# Chart 4: Salary distribution by archetype (boxplot)
print("\n[4/4] Salary distribution by archetype boxplot...")
# Order by median salary so the chart reads naturally
order = df.groupby("archetype")["salary_m"].median().sort_values(ascending=False).index.tolist()

fig, ax = plt.subplots(figsize=(11, 6))
sns.boxplot(
    data=df,
    x="archetype",
    y="salary_m",
    order=order,
    palette=[ARCHETYPE_COLORS[a] for a in order],
    ax=ax,
    showfliers=True,
    linewidth=1.0,
)
ax.set_xlabel("Archetype")
ax.set_ylabel("2025-26 Salary (USD, millions)")
ax.set_title("Salary Distribution by Archetype", fontsize=13, weight="bold")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(FIG_DIR / "salary_by_archetype_box.png")
plt.close()
print(f"  -> {FIG_DIR / 'salary_by_archetype_box.png'}")


print("\nAll visualizations saved to outputs/figures/")
print("Done.")