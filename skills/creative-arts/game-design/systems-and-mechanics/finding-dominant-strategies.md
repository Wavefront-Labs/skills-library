---
id: creative-arts.game-design.systems-and-mechanics.finding-dominant-strategies
name: finding-dominant-strategies
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, dominant-strategy, meaningful-choice, interesting-decisions, degenerate-strategy, balance, exploits, game-theory, playtesting]
level: practitioner
status: draft
description: "Find and remove dominant strategies (options best in every situation) using option-vs-option tables, min-maxer playtests and simulation, then fix with costs, counters or context."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
  - https://gamebalanceconcepts.wordpress.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Finding dominant strategies

**Goal:** no option (unit, card, build, tactic) is the best choice in every situation,
because a dominant option turns a decision into a formality.

Schell (2nd ed.) ch13 names dominant strategies as the classic balance failure: once players find
one, the game reduces to executing it. Game theory term: a strategy is *strictly
dominant* if it is better than every alternative regardless of what opponents do.

## Detection methods
1. **Option-vs-situation table:** rows = options, columns = situations (enemy types,
   game phases, map types). Mark the best option per column. If one row wins every
   column, it is dominant.
2. **Option-vs-option matchup matrix** for competitive pieces: if a row beats or ties
   every other row, it is dominant.
3. **Min-maxer playtests:** brief testers explicitly: "find the strongest way to win,
   exploits encouraged". Normal testers do not hunt; optimisers do.
4. **Usage and win-rate telemetry:** a pick rate far above peers plus an above-average
   win rate is the classic signal. High pick but average win rate may simply be
   popularity.
5. **Simulation/bots:** run greedy or search-based bots; dominant lines surface fast in
   simple systems.

## Fixes (prefer the top of the list)
| Fix | Example |
|---|---|
| Add a situational weakness / counter | spearmen beat cavalry |
| Raise its cost or opportunity cost | longer cooldown, consumes a scarce resource |
| Diminishing returns | stacking the same buff gives less each time |
| Context change | maps or events where it is weak |
| Nerf numbers | last resort; can make it irrelevant instead |
Aim for options that are best *somewhere*, not equal everywhere.

## Gotchas
- **Dominated** options (never best) are the mirror problem: they are dead content.
  Fix them too.
- A strategy can be dominant only at certain skill levels (strong for novices, weak for
  experts or vice versa). Segment data by skill.
- Fixing one dominant option often reveals the next; re-test after each change.
- Some games accept a "solved" opening or optimal line if the rest is rich; decide if
  the dominance actually removes a decision players care about.

## Verify
- [ ] Option-vs-situation table shows a different best option in different columns.
- [ ] Min-maxer playtest run and findings logged.
- [ ] No option exceeds the agreed pick-rate/win-rate thresholds in telemetry.
