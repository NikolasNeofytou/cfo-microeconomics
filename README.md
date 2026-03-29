# Principles of Microeconomics — Study Modules

**Textbook**: Case, Fair & Oster — *Principles of Microeconomics*
**Method**: Puzzle → Read → Model → Debate → Data

A structured study system for learning microeconomics the way top universities teach it — through real-world puzzles, interactive models, policy debates, and data analysis.

## Pedagogy

Each chapter produces a 5-phase study module:

| Phase | Name | Format | Purpose |
|-------|------|--------|---------|
| 1 | **The Puzzle** | Python script | A real-world paradox that doesn't make sense yet |
| 2 | **Read** | Markdown guide | Guided reading with MIT, Harvard, and Yale-style questions |
| 3 | **Model** | React interactive | Manipulate the economic model — drag curves, adjust parameters |
| 4 | **Debate** | Structured markdown | Argue both sides of a policy question using the model |
| 5 | **Data Lab** | Python + matplotlib | Test the model against real economic data (OECD, FRED, World Bank) |

This approach is inspired by how economics is taught at MIT 14.01 (Gruber), Harvard Ec 10 (Mankiw/Chetty), and Yale ECON 115. The key insight: models are tools for thinking, not answers. Phase 4 (debate) forces you to use the same model to argue opposite conclusions. Phase 5 (data) shows where the model works and where reality is messier than the textbook.

## Chapters

| Chapter | Module | Core Model | Status |
|---------|--------|-----------|--------|
| 1 | [Thinking Like an Economist](ch1-thinking-like-an-economist/) | Opportunity cost, PPF | ✅ Complete |
| 3 | Supply and Demand | Equilibrium, shifts | 🔜 Next |
| 5 | Elasticity | Price elasticity, revenue | — |
| 6-7 | Consumer Behavior | Utility, budget constraints | — |
| 8-9 | Costs & Competition | Cost curves, profit maximization | — |
| 12 | Monopoly | Market power, deadweight loss | — |
| 14 | Externalities | Market failure, Pigouvian taxes | — |

## Getting Started

### Prerequisites

```bash
pip install pandas matplotlib numpy
```

### Running a Chapter Module

```bash
cd ch1-thinking-like-an-economist

# Phase 1: The Puzzle (before reading)
python puzzle.py

# Phase 2: Read Chapter 1 with reading_guide.md

# Phase 3: Open model.jsx in Claude for interactive PPF explorer

# Phase 4: Complete debate.md — argue both sides

# Phase 5: Data Lab (after reading)
python data_lab.py
```

## The Red Thread

Every module reinforces one principle: **models are tools, not truths.** Phase 1 shows the puzzle. Phase 3 shows the model's power. Phase 4 shows the model's limits. Phase 5 shows reality's messiness. By the end of the textbook, you should reflexively ask three questions about any economic claim: *What model are they using? What assumptions does it make? Does the data support it?*

## Built With

Study modules generated using a custom [textbook-economics](https://github.com/nikiforosGithub/learning-skills) Claude skill that implements the 5-phase pedagogy for any economics textbook.

## License

Educational use. Data sourced from OECD, World Bank, and public datasets.
