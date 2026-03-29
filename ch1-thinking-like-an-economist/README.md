# Thinking Like an Economist: The Cost of "Free"

**Textbook**: Case, Fair & Oster -- *Principles of Microeconomics*, Chapter 1
**Model**: Opportunity cost, scarcity, production possibilities frontier

## Learning Goals

After completing this module, you should be able to:
1. Explain why "free" is never free -- and calculate the real cost of any choice
2. Draw and interpret a production possibilities frontier
3. Argue both sides of a policy question using economic reasoning
4. Evaluate whether real-world data supports the PPF model's predictions

## Phases

### 1. The Puzzle (20 min)
```bash
python puzzle.py
```
Discover that "free" university costs EUR 21,200/year, and that every choice has a hidden price.

### 2. Read Chapter 1 (1-2 hours)
Follow `reading_guide.md` for section priorities and questions from MIT, Harvard, and Yale-style problem sets.

### 3. Explore the Model (30 min)
Open `model.jsx` in Claude -- an interactive PPF explorer. Drag along the frontier to feel opportunity costs change. Switch between scenarios (COVID shock, tech boom, wartime economy) and watch the frontier shift.

### 4. Policy Debate (30 min)
Complete `debate.md` -- argue both FOR and AGAINST free university education using Chapter 1 concepts. Then write your policy recommendation.

### 5. Data Lab (45 min)
```bash
pip install pandas matplotlib numpy
python data_lab.py
```
Test the PPF model against real OECD data: does education investment actually shift the frontier outward? Spoiler: it's complicated -- and the complications are where the real learning happens.

## Module Map

| File | Phase | What It Does |
|------|-------|-------------|
| `puzzle.py` | 1. Puzzle | Real-world cost paradoxes |
| `reading_guide.md` | 2. Read | Section priorities + MIT/Harvard/Yale questions |
| `model.jsx` | 3. Model | Interactive PPF with scenarios and comparisons |
| `debate.md` | 4. Debate | Policy debate scaffold: should university be free? |
| `data_lab.py` | 5. Data | OECD data analysis with matplotlib visualizations |
| `data/oecd_education_gdp.csv` | 5. Data | 28-country dataset: education, GDP, R&D, employment |
