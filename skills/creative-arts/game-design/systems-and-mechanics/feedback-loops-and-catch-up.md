---
id: creative-arts.game-design.systems-and-mechanics.feedback-loops-and-catch-up
name: feedback-loops-and-catch-up
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, positive-feedback, negative-feedback, catch-up-mechanics, rubber-banding, emergence, game-systems-thinking, runaway-leader, cybernetics, rules-of-play]
level: practitioner
status: draft
description: "Identify positive (snowball) and negative (balancing) feedback loops, place them deliberately, and design catch-up mechanics that keep games close without punishing skill."
sources:
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
  - https://users.cs.northwestern.edu/~hunicke/MDA.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feedback loops and catch-up

**Goal:** control how leads grow or shrink over a game, so matches end decisively but
are not decided too early.

Rules of Play (ch18 Games as Cybernetic Systems) describes **positive feedback** (a
change reinforces itself: the leader gets stronger, destabilising the game) and
**negative feedback** (a change triggers a counter-force: the leader is slowed,
stabilising it). The MDA paper's Monopoly example shows a runaway-leader problem from
positive feedback.

## Map the loops
1. List each resource or advantage and ask: does having more of it help you get more?
   (positive) or does it make getting more harder / help opponents? (negative)
2. Draw them as a loop diagram with + / - signs.
3. Decide where each belongs:
   | Phase | Usually want |
   |---|---|
   | early game | mild or no positive feedback (mistakes recoverable) |
   | mid game | balanced |
   | end game | positive feedback to close the game out |

## Catch-up mechanics (negative feedback tools)
| Tool | Example | Visibility |
|---|---|---|
| Turn order by position | last place goes first | visible, accepted |
| Leader tax / upkeep | larger empires pay more | visible |
| Bounty on leader | bonus for attacking first place | visible, creates drama |
| Better random draws for trailing players | item quality by race position | if hidden, "rubber banding" accusations |
| Comeback objectives | big late-game objectives anyone can take | visible |
| Diminishing returns | each extra unit of advantage worth less | subtle |
| Hidden score | players cannot target the leader precisely | changes social dynamics |

## Procedure
1. Measure **lead stability:** in playtests or sims, how often does the leader at the
   midpoint win? Very high (~90%+) suggests too much positive feedback; near random
   suggests skill/lead matters too little.
2. Add the gentlest catch-up that fixes it; visible, rule-based catch-up is better
   accepted than hidden adjustments.
3. Preserve skill: catch-up should narrow gaps, not invert them.

## Gotchas
- Strong catch-up makes early play meaningless ("why bother leading?").
- Visible rubber banding in racing games is a well-known source of player complaints.
- Kingmaking can rise when trailing players can't win but can choose who does.

## Verify
- [ ] Loop diagram with + / - loops per phase.
- [ ] Midpoint-leader win rate measured and within target.
- [ ] Catch-up tools documented; testers do not report the leader being punished unfairly.
