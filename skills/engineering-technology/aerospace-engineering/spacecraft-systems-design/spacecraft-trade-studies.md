---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.spacecraft-trade-studies
name: spacecraft-trade-studies
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [trade-studies, trade-study, decision-analysis, pugh-matrix, weighted-criteria, mission-systems-engineering]
level: practitioner
status: docs-checked
description: "Run a spacecraft trade study with explicit criteria, weights, scoring, sensitivity analysis and a recorded decision rationale."
sources:
  - https://www.nasa.gov/reference/6-8-decision-analysis/
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Trade studies

**Goal:** a defensible choice among alternatives, with the reasoning kept for review.

## Procedure
1. State the decision need, the constraints and objectives from the programme or project, and the stakeholders.
2. Generate alternatives broadly; they can come from design, operational, cost or schedule options.
3. Choose criteria linked to requirements and mission value. NASA lists customer expectations and requirements, technology limitations, environmental impact, safety, risks, total ownership and life-cycle cost, and schedule impact as types to consider. Define the acceptable range and scale of each so two people would score it alike.
4. Weight the criteria if the method uses weights, and record who set them and why.
5. Evaluate each alternative against each criterion with data (analysis, quotes, test); account for uncertainty in all but the simplest cases.
6. Compute the weighted total, or a comparison against a baseline, as the chosen method requires. Fit the method's complexity to the decision; a simple stakeholder discussion can be enough.
7. Run sensitivity: check whether uncertainty in the inputs or the assumptions behind the criteria could change the ranking; if it could, consider the value of reducing that uncertainty.
8. Decide and document the criteria, methods, assumptions, uncertainties, sensitivities, the final decision with its rationale, and the risks of the choice.

## Practice
- Use a few criteria that really discriminate; many criteria dilute the signal.
- Keep cost and risk visible as separate columns.

## Gotchas
- False precision (decimal scores from guesses).
- Weights tuned after the fact to reach a preferred answer.
- Omitting integration costs such as interfaces and verification.

## Verify
- [ ] Varying each weight either leaves the choice unchanged or the report says which weights flip it.

## Checked
2026-11-01. Confirmed against NASA Systems Engineering Handbook section 6.8 Decision Analysis: criteria types, alternatives sources, method fitted to the decision, uncertainty and sensitivity handling, and the documented work products. Removed: named weighting methods (pairwise, swing), the heritage criterion, the 20 percent weight test, the close-result rule, and the Wertz-Larson book source.
Method: documentation only; no commands were run.
