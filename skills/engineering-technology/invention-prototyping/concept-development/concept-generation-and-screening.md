---
id: engineering-technology.invention-prototyping.concept-development.concept-generation-and-screening
name: concept-generation-and-screening
category: engineering-technology
field: invention-prototyping
product: concept-development
tags: [invention-prototyping, concept-development, ideation, brainstorming, brainwriting, 6-3-5, scamper, morphological-chart, morphological-analysis, triz, contradiction-matrix, inventive-principles, function-decomposition, problem-framing, problem-statement, how-might-we, pugh-matrix, pugh-concept-selection, weighted-decision-matrix, concept-screening, concept-scoring, design-thinking, product-design-specification, requirements, functional-analysis]
level: practitioner
status: draft
description: "Frame the problem, generate concepts with brainstorming, morphological charts and TRIZ principles, then screen with Pugh and weighted matrices before design."
sources: ["Ulrich & Eppinger, Product Design and Development", "Pahl, Beitz, Feldhusen & Grote, Engineering Design: A Systematic Approach", "Pugh, Total Design", "Altshuller, And Suddenly the Inventor Appeared (TRIZ)", "Cross, Engineering Design Methods"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Concept generation and screening — many ideas, then the right one

**Goal:** before any detailed design, frame the real problem, produce a wide set of
genuinely different concepts, and pick one or two with reasons you can defend.

## 1. Frame the problem (most bad concepts start here)
- Write the need **solution-free**: "hold a phone at eye level while cycling", not
  "design a handlebar clamp".
- Ask "why?" two or three times to find the real goal, and "what stops us?" to find
  the actual obstacle.
- List requirements with numbers where you can: target cost, mass, size envelope,
  load, run time, environment. Split **musts** (pass/fail) from **wants** (scored).
- Turn it into one or more "How might we …?" questions at a useful altitude — not so
  broad it is vague, not so narrow it implies the answer.

## 2. Decompose into functions
Draw the overall function (inputs of energy, material, signal → outputs), then break it
into sub-functions: e.g. *attach to bar*, *grip phone*, *adjust angle*, *damp vibration*.
Concepts are built by solving sub-functions, which stops the team fixating on one
whole-product idea.

## 3. Generate widely
Aim for quantity first; judge later.
- **Brainwriting 6-3-5:** six people, three ideas each, five minutes, pass the sheet on —
  up to 108 ideas in 30 minutes, without the loudest voice dominating.
- **SCAMPER** on existing solutions: Substitute, Combine, Adapt, Modify, Put to other use,
  Eliminate, Reverse.
- **External search:** patents, other industries, nature ("who else has to grip a
  moving object?").
- **Morphological chart:** sub-functions as rows, 3–6 alternative means per row. Pick one
  per row to build a whole concept. Five rows × four options gives 1024 combinations, so
  choose combinations deliberately (best-guess, cheapest, most radical) and drop
  incompatible pairs.

| Sub-function | Option A | Option B | Option C | Option D |
|---|---|---|---|---|
| Attach to bar | Strap | Screw clamp | Quarter-turn mount | Magnet |
| Grip phone | Spring jaws | Case adapter | Elastic cross | Suction |
| Damp vibration | Elastomer bush | None | Spring | Gel pad |

## 4. Break contradictions with TRIZ
When improving one parameter worsens another (stronger but heavier, faster but less
accurate), state the **technical contradiction** and look for principles that resolve
it rather than trading off. The 40 inventive principles are a good prompt list; most used
in practice include segmentation, taking out, local quality, asymmetry, nesting,
prior action, dynamics, and changing the physical state/parameters. Altshuller's
contradiction matrix maps pairs of parameters to suggested principles; treat its
output as prompts, not answers.
Also ask for the **ideal final result**: the function delivered with no added cost or
mechanism — what would have to be true for the part to disappear?

## 5. Screen, then score
1. **Must filter:** drop any concept that fails a must-requirement.
2. **Pugh screening:** pick a reference (often the current solution). For each criterion
   mark each concept + / 0 / − against it. Sum. Combine strengths of strong concepts and
   rerun; Pugh is iterative, not a single vote.
3. **Weighted scoring** for the last 3–5: weights summing to 100%, scores 1–5 with
   anchored descriptions, total = Σ(weight × score).
4. **Sensitivity check:** shift the top two weights ±10 points. If the winner changes,
   the decision rests on the weights — discuss those, not the totals.

## Gotchas
- Fixation: the first idea anchors everyone. Generate before anyone sketches "the" answer.
- Matrices give false precision; a 3.62 vs 3.55 total is a tie.
- Criteria that overlap (cost and part count) double-count the same thing.
- Screening only on paper hides the biggest unknown — carry it into a proof-of-concept
  test (see engineering-technology.invention-prototyping.proof-of-concept-builds.critical-assumption-testing).
- Keep rejected concepts with the reason; they are prior art for your own disclosure and
  fallbacks if the winner fails.

## Verify
- [ ] The problem statement contains no solution and has numbered, measurable musts.
- [ ] At least 15–20 distinct concepts were generated from a function breakdown.
- [ ] Every surviving concept passes all musts.
- [ ] The selected concept still wins after a ±10-point weight sensitivity check.
- [ ] The top concept's biggest unknown is named and scheduled for a test.
