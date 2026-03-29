"""
Chapter 1 -- Data Lab: Does Education Investment Shift the PPF?
================================================================
GOAL: Test the Chapter 1 model against real economic data.

The PPF model predicts that investing in education (human capital)
shifts the production possibilities frontier outward -- meaning
countries that invest more in education should be able to produce
more of everything. Let's see if the data supports this.

WHAT TO DO:
  Run this script. It will load real OECD data, create visualizations,
  and ask you to interpret what you see. You'll need matplotlib and
  pandas installed:

    pip install matplotlib pandas numpy

DATA SOURCE:
  OECD Education at a Glance 2023, World Bank Development Indicators
  Data file: data/oecd_education_gdp.csv
"""

import os
import sys
import textwrap

try:
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("This lab requires: pandas, matplotlib, numpy")
    print("Install with: pip install pandas matplotlib numpy")
    sys.exit(1)


def print_header(text):
    print(f"\n{'='*64}")
    print(f"  {text}")
    print(f"{'='*64}\n")


def load_data():
    """Load the OECD education/GDP dataset."""
    data_path = os.path.join(os.path.dirname(__file__), "data", "oecd_education_gdp.csv")
    df = pd.read_csv(data_path)
    return df


def plot_education_vs_gdp(df):
    """Plot 1: Does education spending correlate with GDP per capita?"""
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(df["edu_spending_pct_gdp"], df["gdp_per_capita_usd"],
               s=80, alpha=0.7, c="#2563eb", edgecolors="white", linewidth=0.5)

    for _, row in df.iterrows():
        ax.annotate(row["country"], (row["edu_spending_pct_gdp"], row["gdp_per_capita_usd"]),
                     fontsize=7, alpha=0.7, ha="left", va="bottom",
                     xytext=(4, 4), textcoords="offset points")

    # Trend line
    z = np.polyfit(df["edu_spending_pct_gdp"], df["gdp_per_capita_usd"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df["edu_spending_pct_gdp"].min(), df["edu_spending_pct_gdp"].max(), 100)
    ax.plot(x_line, p(x_line), "--", color="#f59e0b", alpha=0.6, linewidth=1.5)

    corr = df["edu_spending_pct_gdp"].corr(df["gdp_per_capita_usd"])

    ax.set_xlabel("Education Spending (% of GDP)", fontsize=12)
    ax.set_ylabel("GDP per Capita (USD)", fontsize=12)
    ax.set_title(f"Education Spending vs GDP per Capita (r = {corr:.2f})", fontsize=14, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("plot1_education_vs_gdp.png", dpi=150, bbox_inches="tight")
    plt.show()
    return corr


def plot_tertiary_vs_gdp(df):
    """Plot 2: Does tertiary education attainment correlate with GDP?"""
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.scatter(df["tertiary_attainment_pct"], df["gdp_per_capita_usd"],
               s=80, alpha=0.7, c="#059669", edgecolors="white", linewidth=0.5)

    for _, row in df.iterrows():
        ax.annotate(row["country"], (row["tertiary_attainment_pct"], row["gdp_per_capita_usd"]),
                     fontsize=7, alpha=0.7, ha="left", va="bottom",
                     xytext=(4, 4), textcoords="offset points")

    z = np.polyfit(df["tertiary_attainment_pct"], df["gdp_per_capita_usd"], 1)
    p = np.poly1d(z)
    x_line = np.linspace(df["tertiary_attainment_pct"].min(), df["tertiary_attainment_pct"].max(), 100)
    ax.plot(x_line, p(x_line), "--", color="#f59e0b", alpha=0.6, linewidth=1.5)

    corr = df["tertiary_attainment_pct"].corr(df["gdp_per_capita_usd"])

    ax.set_xlabel("Tertiary Education Attainment (% of 25-64 year olds)", fontsize=12)
    ax.set_ylabel("GDP per Capita (USD)", fontsize=12)
    ax.set_title(f"Education Attainment vs GDP per Capita (r = {corr:.2f})", fontsize=14, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("plot2_tertiary_vs_gdp.png", dpi=150, bbox_inches="tight")
    plt.show()
    return corr


def plot_education_vs_rd(df):
    """Plot 3: Education spending vs R&D spending (PPF expansion proxy)."""
    fig, ax = plt.subplots(figsize=(10, 6))

    scatter = ax.scatter(df["edu_spending_pct_gdp"], df["r_and_d_pct_gdp"],
                         s=df["gdp_per_capita_usd"] / 500, alpha=0.6,
                         c=df["gdp_per_capita_usd"], cmap="YlOrRd",
                         edgecolors="white", linewidth=0.5)

    for _, row in df.iterrows():
        ax.annotate(row["country"], (row["edu_spending_pct_gdp"], row["r_and_d_pct_gdp"]),
                     fontsize=7, alpha=0.7, ha="left", va="bottom",
                     xytext=(4, 4), textcoords="offset points")

    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
    cbar.set_label("GDP per Capita (USD)", fontsize=10)

    ax.set_xlabel("Education Spending (% of GDP)", fontsize=12)
    ax.set_ylabel("R&D Spending (% of GDP)", fontsize=12)
    ax.set_title("Education vs R&D Investment (bubble size = GDP/capita)", fontsize=14, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.tight_layout()
    plt.savefig("plot3_education_vs_rd.png", dpi=150, bbox_inches="tight")
    plt.show()


def highlight_cyprus(df):
    """Show where Cyprus sits relative to peers."""
    cyprus = df[df["country"] == "Cyprus"].iloc[0]
    peers = df[df["country"].isin(["Greece", "Portugal", "Estonia", "Ireland", "Israel"])]

    print_header("CYPRUS IN CONTEXT")

    headers = ["Country", "Edu %GDP", "GDP/cap", "Tertiary%", "Youth Unemp%", "R&D %GDP"]
    print(f"  {headers[0]:<16} {headers[1]:<10} {headers[2]:<10} {headers[3]:<12} {headers[4]:<14} {headers[5]:<10}")
    print(f"  {'-'*16} {'-'*10} {'-'*10} {'-'*12} {'-'*14} {'-'*10}")

    for _, row in pd.concat([df[df["country"] == "Cyprus"], peers]).iterrows():
        marker = " <--" if row["country"] == "Cyprus" else ""
        print(f"  {row['country']:<16} {row['edu_spending_pct_gdp']:<10.1f} "
              f"${row['gdp_per_capita_usd']:>7,.0f}  {row['tertiary_attainment_pct']:<12.0f} "
              f"{row['youth_unemployment_pct']:<14.1f} {row['r_and_d_pct_gdp']:<10.1f}{marker}")

    print(f"\n  Cyprus spends {cyprus['edu_spending_pct_gdp']}% of GDP on education")
    print(f"  but only {cyprus['r_and_d_pct_gdp']}% on R&D (lowest among peers).")
    print(f"  High tertiary attainment ({cyprus['tertiary_attainment_pct']}%) but high")
    print(f"  youth unemployment ({cyprus['youth_unemployment_pct']}%) suggests a possible")
    print("  mismatch between education output and labor market needs.\n")


def main():
    print_header("DATA LAB: Does Education Shift the PPF?")
    print("The PPF model from Chapter 1 predicts that investing in\n"
          "education (human capital) expands the frontier -- countries\n"
          "that invest more should be able to produce more of everything.\n"
          "\nLet's test this prediction against real OECD data.\n")

    df = load_data()
    print(f"Loaded data for {len(df)} countries.\n")

    # --- Plot 1 ---
    print_header("ANALYSIS 1: Education Spending vs GDP per Capita")
    print("If education shifts the PPF outward, countries that spend\n"
          "more on education should have higher GDP per capita.\n")
    input("Press Enter to generate the plot...\n")

    corr1 = plot_education_vs_gdp(df)
    print(f"\n  Correlation: r = {corr1:.2f}")
    if abs(corr1) < 0.3:
        print("  WEAK correlation. Education spending (% of GDP) does NOT")
        print("  strongly predict GDP per capita. Why might this be?")
        print("  Hint: South Africa spends 6.1% but has low GDP. Switzerland")
        print("  spends 5.0% but is the richest. Spending LEVEL may matter")
        print("  less than spending EFFICIENCY and institutional quality.\n")
    else:
        print("  Moderate correlation. The relationship exists but is noisy.\n")

    input("Press Enter to continue...\n")

    # --- Plot 2 ---
    print_header("ANALYSIS 2: Education OUTCOMES vs GDP per Capita")
    print("Maybe spending isn't the right measure. What about results?\n"
          "Countries with more educated populations (higher % with\n"
          "university degrees) should have higher GDP.\n")
    input("Press Enter to generate the plot...\n")

    corr2 = plot_tertiary_vs_gdp(df)
    print(f"\n  Correlation: r = {corr2:.2f}")
    if corr2 > 0.5:
        print("  STRONGER correlation! Education ATTAINMENT predicts GDP")
        print("  better than education SPENDING. This suggests it's not")
        print("  how much you spend, but what you get for it.\n")
    print("  The PPF model is partially validated: more educated")
    print("  populations DO tend to have higher production capacity.\n")

    input("Press Enter to continue...\n")

    # --- Plot 3 ---
    print_header("ANALYSIS 3: Education + R&D = PPF Expansion?")
    print("The PPF shifts outward through investment in human capital\n"
          "(education) AND physical/knowledge capital (R&D). Do countries\n"
          "that invest in both do better?\n")
    input("Press Enter to generate the plot...\n")

    plot_education_vs_rd(df)
    print("\n  Notice: the richest countries (largest bubbles, warmest colors)")
    print("  tend to be in the upper-right quadrant (high edu + high R&D).")
    print("  South Korea and Israel stand out: high R&D + moderate edu")
    print("  spending produces strong outcomes.\n")

    input("Press Enter to continue...\n")

    # --- Cyprus focus ---
    highlight_cyprus(df)

    input("Press Enter for reflection questions...\n")

    # --- Reflection ---
    print_header("REFLECTION QUESTIONS")
    print(textwrap.dedent("""\
    Answer these based on the data you just explored:

    1. THE MODEL'S PREDICTION: The PPF model says education investment
       shifts the frontier outward. Does the data support this?
       [Your answer: partially / yes / no, and why]

    2. WHAT THE MODEL GETS RIGHT: Education attainment (outcomes)
       correlates with GDP better than spending (inputs). What does
       this tell us about how to think about PPF shifts?

    3. WHAT THE MODEL MISSES:
       - South Africa spends 6.1% of GDP on education but has
         low GDP and 63.5% youth unemployment. Why doesn't
         education spending automatically shift the PPF?
       - Ireland spends only 3.3% but has $100K+ GDP per capita.
         What else might be shifting Ireland's PPF outward?

    4. CYPRUS SPECIFICALLY: Cyprus has high education attainment
       (58%) but high youth unemployment (17%) and very low R&D
       (0.9%). Using the PPF framework, what would you recommend
       Cyprus invest in to shift its frontier outward?

    5. CORRELATION vs CAUSATION: We found correlations between
       education and GDP. Does education CAUSE higher GDP, or do
       richer countries simply AFFORD more education? How would
       you design a study to figure this out?

    Save your answers -- they'll be useful when you study
    externalities (Chapter 14) and government policy later.
    """))

    print("=" * 64)
    print("  Plots saved: plot1_education_vs_gdp.png")
    print("               plot2_tertiary_vs_gdp.png")
    print("               plot3_education_vs_rd.png")
    print("=" * 64)


if __name__ == "__main__":
    main()
