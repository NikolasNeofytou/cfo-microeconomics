"""
Chapter 1 -- The Puzzle: What Does "Free" Actually Cost?
=========================================================
GOAL: Discover that "free" is never free, and that the cost of
      anything is what you give up to get it.

You DON'T need to have read Chapter 1 yet. Just use your intuition.

WHAT TO DO:
  Run this script. It will walk you through a series of real-world
  scenarios where things seem free but aren't. By the end, you'll
  be asking "what's the real cost?" about everything.
"""

import textwrap


def print_header(text):
    print(f"\n{'='*64}")
    print(f"  {text}")
    print(f"{'='*64}\n")


def print_data_table(headers, rows):
    """Print a simple formatted table."""
    col_widths = [max(len(str(row[i])) for row in [headers] + rows) + 2
                  for i in range(len(headers))]
    fmt = "  " + "".join(f"{{:<{w}}}" for w in col_widths)
    print(fmt.format(*headers))
    print("  " + "".join("-" * w for w in col_widths))
    for row in rows:
        print(fmt.format(*row))


def main():
    print_header("THE PUZZLE: What Does 'Free' Actually Cost?")

    # --- Scenario 1: The "free" university ---
    print(textwrap.dedent("""\
    SCENARIO 1: Two University Offers
    ----------------------------------
    You've been accepted to two universities in Cyprus:

      University A: Tuition EUR 6,800/year
      University B: Full scholarship (tuition EUR 0)

    A friend says: "Obviously go to B -- it's free!"
    """))

    answer = input("  Is your friend right? Is University B really free? (yes/no): ").strip().lower()
    print()

    print(textwrap.dedent("""\
    Let's look at the REAL cost of attending university, whether
    tuition is zero or not:
    """))

    print_data_table(
        ["Cost Component", "Univ A (per year)", "Univ B (per year)"],
        [
            ["Tuition", "EUR 6,800", "EUR 0"],
            ["Room & board", "EUR 5,400", "EUR 5,400"],
            ["Books & supplies", "EUR 600", "EUR 600"],
            ["Transport", "EUR 1,200", "EUR 1,200"],
            ["Foregone earnings*", "EUR 14,000", "EUR 14,000"],
            ["", "----------", "----------"],
            ["TOTAL REAL COST", "EUR 28,000", "EUR 21,200"],
        ]
    )
    print()
    print("  * If you didn't attend university, you could work full-time")
    print("    and earn approximately EUR 14,000/year. By attending, you")
    print("    GIVE UP that income. That's a cost -- even if no one sends")
    print("    you a bill for it.\n")
    print('  The "free" university actually costs EUR 21,200 per year.')
    print("  The most expensive line item isn't tuition -- it's the job")
    print("  you're not working.\n")

    input("  Press Enter to continue...\n")

    # --- Scenario 2: The "free" app ---
    print_header("SCENARIO 2: The Free App")
    print(textwrap.dedent("""\
    Instagram is free. You pay EUR 0 to use it.

    But Meta (Instagram's parent) earned $32 billion from Instagram
    in 2023 -- roughly $40 per user per year.

    How does a "free" product generate $40/user/year?
    """))

    print("  What you pay:    EUR 0 (money)")
    print("  What you give up:")
    print("    - ~30 min/day of your time (= 182 hours/year)")
    print("    - Your attention (sold to advertisers)")
    print("    - Your personal data (behavioral profile)")
    print("    - Your focus (opportunity cost of what you could")
    print("      have done with those 182 hours)\n")
    print("  If you value your time at EUR 10/hour, Instagram 'costs'")
    print("  you EUR 1,820/year. The product is free. The cost is not.\n")

    input("  Press Enter to continue...\n")

    # --- Scenario 3: The real puzzle ---
    print_header("SCENARIO 3: The Government's Dilemma")
    print(textwrap.dedent("""\
    Cyprus has a limited budget. It can invest in:
      A) More hospital beds (healthcare)
      B) More teachers (education)
      C) Military equipment (defense)

    In 2023, Cyprus allocated approximately:
      - Healthcare: 7.0% of GDP
      - Education:  5.5% of GDP
      - Defense:    1.8% of GDP

    Every euro spent on hospital beds is a euro NOT spent on teachers.
    Every euro on teachers is a euro NOT spent on defense.

    This is the fundamental economic problem: resources are SCARCE,
    wants are UNLIMITED, and every choice has a cost -- the thing
    you didn't choose.
    """))

    input("  Press Enter to see what this means...\n")

    # --- The framework ---
    print_header("THE FRAMEWORK YOU'RE ABOUT TO LEARN")
    print(textwrap.dedent("""\
    Chapter 1 introduces three ideas that explain ALL of this:

    1. OPPORTUNITY COST
       The cost of anything is what you give up to get it.
       University B's cost isn't EUR 0 -- it's EUR 21,200.
       Instagram's cost isn't EUR 0 -- it's 182 hours of your year.

    2. SCARCITY
       There isn't enough of everything for everyone.
       Cyprus can't fully fund healthcare AND education AND defense.
       You can't attend university AND work full-time.

    3. THE PRODUCTION POSSIBILITIES FRONTIER (PPF)
       A graph that shows every possible combination of two goods
       a society can produce. It makes tradeoffs VISIBLE.
       Moving along it = choosing more of one thing means less of another.
       Being inside it = wasting resources.
       Being outside it = impossible (without growth).

    After reading Chapter 1, you'll build an interactive PPF explorer
    that makes these tradeoffs tangible. You'll drag along the frontier
    and watch opportunity costs change in real time.
    """))

    print("=" * 64)
    print("  Now read Chapter 1. Then come back for the interactive model.")
    print("=" * 64)
    print()


if __name__ == "__main__":
    main()
