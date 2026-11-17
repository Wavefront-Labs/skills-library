---
id: computing-software.qa-testing-engineering.test-case-design.defect-prevention-and-rca
name: defect-prevention-and-rca
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [defect-prevention, five-whys, root-cause-analysis, fishbone-diagram, ishikawa, defect-management]
level: practitioner
status: draft
description: "Prevent defect classes with root cause analysis: pick defects worth analysing, run 5 whys and fishbone, find process causes, and track preventive actions to done."
sources:
  - https://www.istqb.org/certifications/test-analyst
  - https://asq.org/quality-resources/fishbone
  - https://www.lean.org/lexicon-terms/5-whys/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Defect prevention and RCA (5 whys, fishbone)

**Goal:** stop whole classes of defects recurring by fixing the process cause, not just the bug (ISTQB CTAL-TA defect prevention; CTFL root cause analysis).

## Choose what to analyse
Escaped defects, severity critical/major, repeated defect types, or a cluster in one component. Not every bug; 2-5 per sprint is sustainable.

## 5 whys (example)
1. Why did customers get double-charged? Retry on payment timeout re-sent the charge.
2. Why did the retry re-send? The payment call is not idempotent.
3. Why not idempotent? No idempotency key passed to the provider.
4. Why was that missed? Provider integration checklist does not mention idempotency; no test for timeout retries.
5. Why no test? Integration tests mock the provider and never simulate timeouts.
Root causes: missing checklist item + missing fault-injection test pattern. Stop when you reach a cause the team can change; there may be several branches.

## Fishbone (Ishikawa)
Categories for software: People, Process, Requirements, Design, Code, Tools, Environment, Test. Brainstorm causes under each, then vote on the most likely and verify with data.

## Preventive actions
- Each action: owner, due date, how we will know it worked.
- Prefer systemic fixes: lint rule, type, template, checklist item, test pattern, review gate.
- Add the missed test at the lowest level that would have caught it.

## Gotchas
- Stopping at "developer made a mistake" (human error is a symptom; ask why the system allowed it).
- Blame kills honesty; run it blameless.
- Actions not tracked = theatre. Review completion monthly.

## Verify
Each analysed defect has a documented causal chain, actions with owners, and a later check that the defect class has not recurred.
