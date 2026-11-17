---
id: computing-software.it-governance-risk-compliance.enterprise-architecture.gap-analysis-matrix
name: gap-analysis-matrix
category: computing-software
field: it-governance-risk-compliance
product: enterprise-architecture
tags: [gap-analysis-matrix, gap-analysis-technique, gap analysis, gap matrix, baseline target, eliminated, new, carried over, gap analysis technique, enterprise-architecture]
level: practitioner
status: draft
description: "Build the TOGAF gap analysis matrix with baseline on one axis and target on the other to find eliminated and new elements."
sources:
  - https://pubs.opengroup.org/togaf-standard/
  - https://pubs.opengroup.org/architecture/archimate32-doc/
  - https://www.zachman.com/about-the-zachman-framework
  - https://www.businessarchitectureguild.org/
  - https://www.dodcio.defense.gov/Library/DoD-Architecture-Framework/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gap analysis matrix: baseline versus target

Goal: show what is kept, removed and added.

1. List baseline architecture elements down the rows.
2. List target elements across the columns, with a final column for new elements and a row for eliminated.
3. Mark where a baseline element is carried over to a target element.
4. Unmatched baseline rows are eliminated (intentionally or accidentally); unmatched target columns are new and need development or procurement.
5. Convert each gap to a candidate work package.

Gotchas:
- Intentional versus accidental elimination: confirm with the owner that nothing needed is lost.
- Match at consistent granularity.

Verify: every unmatched cell has a decision.
