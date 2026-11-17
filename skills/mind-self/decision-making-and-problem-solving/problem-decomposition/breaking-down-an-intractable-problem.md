---
id: mind-self.decision-making-and-problem-solving.problem-decomposition.breaking-down-an-intractable-problem
name: breaking-down-an-intractable-problem
category: mind-self
field: decision-making-and-problem-solving
product: problem-decomposition
tags: [decision-making-and-problem-solving, problem-decomposition, problem-solving, polya, how-to-solve-it, problem-restatement, reframing, working-backwards, simpler-case, special-cases, mece, issue-tree, logic-tree, hypothesis-driven, divide-and-conquer, fermi-estimation, first-principles, stuck, heuristics]
level: practitioner
status: draft
description: "Break a stuck problem into solvable parts: restate it, define done, build a MECE issue tree, work backwards, solve a simpler or special case first, and know when to change approach."
sources: ["Polya, How to Solve It (1945)", "Minto, The Pyramid Principle (1987)", "Rasiel, The McKinsey Way (1999)", "Schoenfeld, Mathematical Problem Solving (1985)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Breaking down an intractable problem

**Goal:** get unstuck on a problem too big or vague to attack directly — a puzzle, a
project, a business question, a maths or coding problem — by turning it into pieces you
can actually solve.

## 1. Understand and restate (Polya's first step)
- Write the problem in **one sentence, in your own words**.
- What's the **unknown**? What's **given**? What are the **constraints**?
- Define **done**: what would a satisfactory answer look like? ("A plan that cuts monthly
  costs by £200 without moving house" is solvable; "sort out money" isn't.)
- Restate it in at least two other ways: as a question, from another person's view, in
  the opposite direction ("how could we make costs go *up*?"). Reframing often reveals
  the real problem is different from the stated one.

## 2. Build an issue tree
Split the problem into sub-questions, then split those. Aim for **MECE** branches —
**mutually exclusive** (no overlap) and **collectively exhaustive** (nothing missing).
Example — "Why is profit down?":
- Revenue down? → fewer customers? / lower spend per customer?
- Costs up? → variable costs? / fixed costs?
Arithmetic and process splits (revenue − costs; stage 1 → 2 → 3) are easier to keep
MECE than lists of themes. Stop splitting when a branch can be answered or acted on.

## 3. Prioritise branches
Mark each leaf by **likely impact** and **ease of answering**. Do high-impact, easy ones
first. A hypothesis ("I think it's mostly fewer customers") can direct where you dig, as
long as you're willing to be wrong.

## 4. Tactics when a piece won't crack
- **Work backwards:** start from the goal and ask what the step just before it must be.
  Good for planning, proofs and puzzles with a clear end state.
- **Solve a simpler version:** fewer variables, smaller numbers, one case instead of all.
  Then generalise.
- **Try special cases and examples:** n = 1, 2, 3; the extreme values; a concrete
  instance. Patterns emerge.
- **Find a related problem you've solved:** "Have I seen something with the same unknown?"
- **Draw it:** diagrams, tables, timelines.
- **Drop a constraint temporarily:** solve without it, then add it back.
- **Estimate (Fermi):** a rough order-of-magnitude answer can tell you whether the
  problem matters or which branch dominates.

## 5. Monitor and switch
Set a checkpoint (e.g. every 20–30 minutes): am I making progress? If not, switch tactic
rather than grinding. Schoenfeld found novices often pursue one unproductive approach
for the whole session — the meta-skill is noticing and changing course. Taking a break
can help ("incubation" has modest evidence).

## 6. Recombine and check
Assemble the sub-answers. Does the combined answer actually solve the original
restatement and meet the "done" definition? Look back (Polya's last step): could it be
done more simply? What did you learn for next time?

## Gotchas
- **Solving the wrong problem** — skipping step 1 — wastes the most time.
- **Non-MECE trees** double-count or leave gaps; check each level adds up to its parent.
- **Analysis paralysis:** trees can grow forever. Stop at actionable leaves.
- **First-principles** thinking is useful but slow; you don't need to rederive what you
  can look up.

## Verify
- [ ] You have a one-sentence restatement and a written definition of done.
- [ ] Your top-level split is MECE (check for overlaps and gaps).
- [ ] Each leaf is answerable or actionable.
- [ ] You used at least one tactic from step 4 on the hardest piece.
- [ ] The recombined answer meets the definition of done.
