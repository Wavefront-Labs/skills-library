---
id: creative-arts.design-for-form-and-experience.ux-design.heuristic-evaluation-with-nielsens-ten
name: heuristic-evaluation-with-nielsens-ten
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [heuristic-evaluation, expert-review, ten-usability-heuristics, nielsen-heuristics, usability-inspection, ux-research]
level: practitioner
status: docs-checked
description: "Run a heuristic evaluation: 3-5 evaluators inspect independently against Nielsen's 10 heuristics, log violations, then consolidate and prioritise as a team."
sources:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.nngroup.com/articles/how-to-conduct-a-heuristic-evaluation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heuristic evaluation with Nielsen's ten

**Goal:** find usability problems cheaply, without users, by having several evaluators judge an interface against a fixed list of principles.

## The ten heuristics (use the exact names in reports)
1. Visibility of system status  2. Match between system and the real world  3. User control and freedom  4. Consistency and standards  5. Error prevention  6. Recognition rather than recall  7. Flexibility and efficiency of use  8. Aesthetic and minimalist design  9. Help users recognize, diagnose and recover from errors  10. Help and documentation.

## Procedure
1. **Scope** the evaluation to a representative task or flow (checkout, sign-up) rather than the whole product.
2. **Recruit 3-5 evaluators** who each evaluate the same interface independently; any single evaluator, however expert, is likely to miss issues. New teams read the heuristics and do a group practice round on a simple design first.
3. **Evaluate independently,** timeboxed to about 1-2 hours each, in two passes: first go through the task once just to learn the system without evaluating, then go through it again looking for heuristic violations. Evaluators do not see each other's evaluations until their own is complete.
4. **Log each problem** as one row: location (screen/URL), what is wrong, heuristic violated, evidence (screenshot).
5. **Debrief and consolidate:** cluster similar issues (affinity diagramming), discuss agreements and disagreements, which issues are most detrimental, which need more data, and next steps. Produce a ranked list with a recommended fix per item.

## Gotchas
- The heuristics are broad rules of thumb, not specific usability guidelines or pass/fail rules.
- A violation does not always mean a real problem; mark doubtful ones in the debrief or validate them with users.
- Heuristic evaluation does not replace user research; follow with a usability test (see `creative-arts.design-for-form-and-experience.prototyping.running-a-prototype-walkthrough-test`).

## Verify
- [ ] At least 3 independent evaluators, notes not shared before consolidation.
- [ ] Every finding has location, heuristic and evidence.
- [ ] Output is a ranked, de-duplicated list, not a pile of raw notes.

## Checked
2026-11-01. Confirmed on NN/g Ten Usability Heuristics (names, rules of thumb) and How to Conduct a Heuristic Evaluation (3-5 independent evaluators, 1-2 hour timebox, learning pass then evaluation pass, no sharing until done, affinity diagramming in debrief, not a replacement for user research). Removed (not stated there): 0-4 severity scale, one-third and five-evaluator coverage figures, UX-training advice, 2-4 task scope, positives advice.
Method: documentation only; no commands were run.
