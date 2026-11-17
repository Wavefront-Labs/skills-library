---
id: creative-arts.game-design.systems-and-mechanics.risk-reward-tradeoffs
name: risk-reward-tradeoffs
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, risk-reward, meaningful-choice, interesting-decisions, push-your-luck, gambling-mechanics, tension, expected-value, loss-aversion]
level: practitioner
status: draft
description: "Design risk-reward decisions (push-your-luck, optional challenges, wagering, greed vs safety) where players can read the stakes and both choices are viable."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Risk-reward trade-offs

**Goal:** decisions where the player weighs a bigger payoff against a real chance of
loss, can read the stakes, and could reasonably choose either way.

## Common structures
| Structure | Example | Lever |
|---|---|---|
| Push your luck | keep drawing/rolling until you bank or bust | bust probability per step |
| Optional harder path | side route with better loot and tougher enemies | reward premium vs difficulty |
| Wager / ante | bet resources on an outcome | payout ratio |
| Greed timer | stay longer in the danger zone for more loot | escalating threat |
| Exposure | attack from the open for bonus damage | counter-attack risk |
| Carry-it-home | loot is lost on death until extracted | distance to extraction |

## Design rules
1. **Make the risk legible.** Show odds, threat levels, or at least consistent cues.
   Unreadable risk is just randomness.
2. **Make the reward visible before choosing.**
3. **Keep both choices viable.** If the risky option's EV is always higher, cautious
   play is wrong (dominant greed); if always lower, the risky path is a trap. Tune so
   the choice depends on the situation (current resources, score, position).
4. **Escalate stakes over a sequence.** Push-your-luck works because each additional
   step raises both the pot and the bust chance.
5. **Make losses recoverable** within the session, unless permanent loss is the
   explicit design (hardcore, extraction games).
6. **Account for loss aversion:** players feel losses more than gains, so a
   mathematically neutral bet feels bad. Many designs pay a premium above break-even to
   make risk attractive.

## Tuning procedure
- Compute EV of each choice at several typical states (see
  `creative-arts.game-design.systems-and-mechanics.expected-value-in-game-design`).
- Playtest: record how often players take the risky option. Near 0% or 100% means the
  choice is not a choice.
- Check situational dependence: trailing players should more often prefer risk (a
  natural catch-up tool).

## Gotchas
- Tying risky choices to real-money purchases moves into gambling regulation territory.
- Too many small risk decisions cause fatigue; reserve them for meaningful moments.

## Verify
- [ ] Stakes visible before each risky decision.
- [ ] Risky-option take-rate between roughly 20% and 80% across testers, varying by situation.
- [ ] Neither option dominant in EV across states.
