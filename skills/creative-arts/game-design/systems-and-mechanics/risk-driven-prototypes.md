---
id: creative-arts.game-design.systems-and-mechanics.risk-driven-prototypes
name: risk-driven-prototypes
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, prototype-question, risk-prototype, game-prototyping, prototype-iteration, schell, rule-of-the-loop, risk-assessment, preproduction]
level: practitioner
status: draft
description: "Plan prototypes from the project's risk list: each prototype answers one question, is as cheap as possible, and ends with a written yes/no that changes the plan."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Risk-driven prototypes

**Goal:** spend prototype effort where the project is most likely to fail, and stop each
prototype as soon as it has answered its question.

Schell (2nd ed.) ch8 gives the "Rule of the Loop" (the more times you test and improve, the better
the game) and prototyping tips including: answer a question; forget quality; do not get
attached; prioritise prototypes; parallelise; it need not be digital; pick a fast
iteration engine; build the toy first.

## Procedure
1. **List risks** in four buckets: design (is it fun?), technical (can we build it?),
   art/content (can we make enough at quality?), market (will people want it?).
2. **Rank by likelihood x impact.** The top 3 get prototypes.
3. **Write each as a closed question with a pass criterion:**
   ```
   Q: Can 4 players coordinate with only pings, no voice?
   Pass: 3 of 4 test groups finish the heist without verbal callouts being necessary.
   Prototype: grey-box level, ping wheel, no art, no audio. Budget: 3 days.
   ```
4. **Choose the cheapest medium** that can answer it: paper, a spreadsheet, an existing
   game modded, a grey-box build, a video mock-up for market tests.
5. **Run, record the answer, decide:** proceed, pivot, or cut. Write it down; prototypes
   whose results nobody acts on were wasted.
6. **Throw the prototype code away** unless deliberately written to keep; prototype code
   carries shortcuts.

## Gotchas
- **"Prototype the whole game"** is not a question; it becomes early production.
- Prototypes answering low risks (the fun part you already know works) feel productive
  and teach nothing.
- Running prototypes in parallel (Schell) is cheaper than sequentially when the team can
  split; questions must be independent.
- A "no" is a successful prototype. Cutting early is the point.

## Verify
- [ ] Risk list with top 3 ranked.
- [ ] Each prototype has a closed question, pass criterion and time budget.
- [ ] Each ended with a written decision that changed or confirmed the plan.
