---
id: creative-arts.game-design.systems-and-mechanics.constitutive-operational-implicit-rules
name: constitutive-operational-implicit-rules
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-and-mechanics, constitutive-rules, operational-rules, implicit-rules, rules-analysis, game-rules]
level: practitioner
status: draft
description: "Analyse and write game rules at three levels (constitutive, operational, implicit) per Salen and Zimmerman, to find gaps and ambiguities before players do."
sources:
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
  - https://mitpress.mit.edu/9780262195362/the-game-design-reader/
  - https://www.routledge.com/Game-Design-Workshop-A-Playcentric-Approach-to-Creating-Innovative-Games/Fullerton/p/book/9781032611631
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Constitutive, operational and implicit rules

**Goal:** a rule set with no hidden gaps, by separating its three levels (Salen and
Zimmerman, *Rules of Play*, chapter 12).

| Level | What it is | Tic-tac-toe example |
|---|---|---|
| Constitutive | the abstract formal logic | players alternately claim cells of a 3x3 grid; first to own a line wins |
| Operational | the rules players read and follow | draw X or O in a square; take turns; three in a row wins |
| Implicit | unwritten etiquette and assumptions | do not take forever; do not erase marks; be a good sport |

## Procedure
1. **Write the constitutive core** as math-like statements: state, legal moves, end condition.
   Check completeness: every state has defined legal moves; every end has an outcome.
2. **Derive the operational rules** for the medium (cards, board, software). Different
   media can share one constitutive core.
3. **List the implicit rules** you rely on (time limits, no peeking, tie-breaks at the
   table). Decide which should become operational.
4. **Test for ambiguity** with "rules lawyer" playtests; each dispute is a missing or
   unclear operational rule.
5. **For digital games,** constitutive rules are code; operational rules are what the
   tutorial and UI communicate; implicit rules become community norms and terms of service.

## Gotchas
- Fixing implicit-rule problems (stalling, kingmaking) by adding operational rules costs
  learning load each time. Prefer constitutive fixes.
- Porting a board game to digital exposes implicit rules (who shuffles, take-backs).
- House rules are operational variants; a robust constitutive core tolerates them.

## Verify
- [ ] Constitutive state, moves and end conditions written.
- [ ] Operational rules cover every constitutive branch.
- [ ] Implicit-rule list reviewed; each kept implicit on purpose.
