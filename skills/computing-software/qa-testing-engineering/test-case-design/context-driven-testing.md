---
id: computing-software.qa-testing-engineering.test-case-design.context-driven-testing
name: context-driven-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [context-driven-testing, testing-principles, testing-schools, test-approach, heuristics]
level: practitioner
status: docs-checked
description: "Apply the context-driven testing principles to choose practices by project context instead of best practices, and justify the chosen approach."
sources:
  - https://context-driven-testing.com/
  - https://www.satisfice.com/download/heuristic-test-strategy-model
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Context-driven testing

**Goal:** pick testing practices that fit this project's risks, people and constraints. The seven principles at context-driven-testing.com (Kaner, Bach, Pettichord).

## The principles (summary)
1. The value of any practice depends on its context.
2. There are good practices in context, but no best practices.
3. People, working together, are the most important part of any project's context.
4. Projects unfold over time in ways that are often not predictable.
5. The product is a solution. If the problem isn't solved, the product doesn't work.
6. Good software testing is a challenging intellectual process.
7. Only through judgment and skill, exercised cooperatively throughout the entire project, are we able to do the right things at the right times to effectively test our products.

## Analysing context (Heuristic Test Strategy Model)
James Bach's HTSM (v6.3 on satisfice.com) is a set of guideword heuristics with four focus areas: test techniques, project elements, product factors and quality criteria categories. Use the guidewords as prompts and answer: what matters most, what can we observe, what are we allowed to spend.

## Examples
| Context | Fitting approach |
|---|---|
| Medical device, regulator audit | scripted, traced, formally reviewed, documented |
| Startup MVP, weekly releases | exploratory sessions + thin automated smoke + monitoring |
| Legacy batch rewrite | golden-master comparison against old system |

## Gotchas
- Context-driven is not "no process": in a regulated context the heavy process *is* the right practice.
- Write down the reasoning; "context" must be explainable to stakeholders.
- Revisit the approach when context changes (team, deadline, risk).

## Verify
The test strategy states the context factors and links each major practice choice to one of them.

## Checked

2026-10-28. Confirmed: context-driven-testing.com: the seven principles (wording corrected to the page); authors Kaner, Bach and Pettichord (Lessons Learned in Software Testing); satisfice.com: HTSM v6.3 has four focus areas (test techniques, project elements, product factors, quality criteria categories). Removed: The detailed guideword lists (page too short to confirm) and loosely paraphrased principle wording.

Method: documentation only; no commands were run.
