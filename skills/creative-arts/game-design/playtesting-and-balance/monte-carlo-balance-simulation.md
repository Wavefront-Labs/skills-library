---
id: creative-arts.game-design.playtesting-and-balance.monte-carlo-balance-simulation
name: monte-carlo-balance-simulation
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, monte-carlo-simulation, balance-tuning, simulation, python, bots, win-rate, balance-spreadsheet, automated-playtesting]
level: advanced
status: docs-checked
description: "Simulate a game's rules thousands of times with scripted strategies (Monte Carlo) to estimate win rates, game length and dominant strategies before human playtests."
sources:
  - https://docs.python.org/3/library/random.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monte Carlo balance simulation

**Goal:** use a quick simulation of the rules to answer balance questions (who wins,
how long games last, which strategy dominates) over thousands of games, so playtests
focus on feel rather than arithmetic.

## Procedure
1. **Pick a narrow question:** "Does player 1 win too often?" "Is strategy A better than B?"
   "How many rounds does a game last?"
2. **Model only the rules that matter** to the question; abstract the rest.
3. **Write simple strategies** (greedy, random-legal, scripted heuristics); several per
   question.
4. **Run many games** (thousands) with a fixed random seed per batch for reproducibility.
5. **Report** win rates with confidence intervals, game length distribution, and
   strategy matchups.
6. **Change one parameter at a time** and re-run to see sensitivity.

## Minimal Python skeleton
```python
import random, statistics
def play(rng, p1_strategy, p2_strategy):
    hp = [20, 20]; turn = 0
    while min(hp) > 0:
        strat = p1_strategy if turn % 2 == 0 else p2_strategy
        hp[1 - turn % 2] -= strat(rng)
        turn += 1
    return (0 if hp[1] <= 0 else 1), turn
safe  = lambda rng: 3 if rng.random() < 0.9 else 0     # EV 2.7
risky = lambda rng: 6 if rng.random() < 0.5 else 0     # EV 3.0
rng = random.Random(42)
results = [play(rng, safe, risky) for _ in range(20000)]
p1_win = sum(1 for w, _ in results if w == 0) / len(results)
print(round(p1_win, 3), statistics.median(t for _, t in results))
```
Win-rate standard error ~ sqrt(p(1-p)/n); with n = 20,000 and p ~ 0.5 that is ~0.35
percentage points.

## Gotchas
- Bots play differently from humans; simulation finds arithmetic problems, not fun
  problems.
- Greedy strategies miss deep tactics; a strategy that loses to greedy bots may beat
  humans.
- Model bugs masquerade as balance findings; unit-test rules with known cases.

## Checked

2026-11-09. Confirmed against the Python `random` documentation: `random.Random` instances
are independent generators, `random()` and seeding for reproducible runs. The skeleton's
expected values (2.7 and 3.0) and the standard-error figure (about 0.35 points at n = 20,000,
p = 0.5) were recomputed by hand, not run. Removed the claim about the Game Balance book (its
store page does not mention simulation). Method advice is judgement.
Method: documentation only; no commands were run.

## Verify
- [ ] Question, modelled rules and strategies documented.
- [ ] Fixed seeds; results reproducible.
- [ ] Confidence intervals reported.
- [ ] Findings checked in at least one human playtest.
