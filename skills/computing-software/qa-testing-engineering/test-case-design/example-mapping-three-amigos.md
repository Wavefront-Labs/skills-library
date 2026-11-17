---
id: computing-software.qa-testing-engineering.test-case-design.example-mapping-three-amigos
name: example-mapping-three-amigos
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [example-mapping, three-amigos, bdd, test-first, refinement, rules-and-examples, story-readiness]
level: practitioner
status: docs-checked
description: "Run a 25-minute example-mapping session: story, rules, examples and questions on coloured cards, to find gaps and decide whether a story is ready."
sources:
  - https://cucumber.io/blog/bdd/example-mapping-introduction/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Example mapping and three amigos

**Goal:** a fast, visual conversation that turns a story into rules, examples and questions before work starts. Cucumber blog, example mapping introduction.

## Setup
- People: product owner/business, developer, tester (the three amigos). Timebox 25 minutes per story.
- Cards (or a Miro board): **yellow** story, **blue** rules (acceptance criteria), **green** examples under each rule, **red** questions.

## Flow
1. Put the story card at the top.
2. Write each known rule as a blue card.
3. Under each rule, add green examples ("Gina, gold, 100.00 -> 10%"). Use concrete numbers.
4. Anything nobody can answer goes on a red card with an owner.
5. At the end, vote thumbs up/down: is it ready?

## Reading the map
- Many red cards: not ready, take questions away.
- Many blue cards: story is too big, split by rule.
- A rule with no examples: not understood yet.
- Lots of examples under one rule: it is complex, consider decision-table testing.

## Output
Rules become acceptance criteria; examples become scenarios/tests (`atdd-acceptance-test-workshops`); red cards become tasks.

## Gotchas
- Writing Gherkin during the session slows it down. Capture examples tersely; formalise later.
- Over the timebox usually means the story is too big.

## Verify
Stories that went through example mapping produce fewer "clarification" defects; track for a few sprints.

## Checked

2026-10-28 Confirmed against: Cucumber blog (yellow story card, blue rules, green examples, red questions, about 25 minutes, thumb-vote for readiness, story too big or too uncertain signals). Removed or generalised: the attribution to a named author and the advice on friendly names (not stated on the page).

Method: documentation only; no commands were run.
