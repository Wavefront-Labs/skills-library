---
id: computing-software.qa-testing-engineering.test-case-design.change-impact-analysis
name: change-impact-analysis
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [impact-analysis, change-impact-analysis, maintenance-testing, regression-testing, dependency-analysis, git-diff]
level: practitioner
status: draft
description: "Analyse the impact of a change to decide what to retest: code and config diff, dependency graph, shared data, interfaces and requirement links."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change impact analysis

**Goal:** a reasoned list of areas to retest for a change, instead of "run everything" or "test only the ticket". ISTQB CTFL v4.0 2.3 (maintenance testing).

## Sources of impact
1. **Code diff**: `git diff --stat main...feature` and `git log --name-only` for touched modules.
2. **Callers / dependents**: IDE "find usages", `grep -rn "functionName"`, dependency graphs (`madge` for JS, `pydeps`, `jdeps`, Nx/Bazel affected targets: `nx affected --target=test`).
3. **Shared data**: DB tables, columns, caches, queues, files touched; other services that read them.
4. **Configuration and feature flags** changed.
5. **Interfaces**: API schema diff (`oasdiff breaking old.yaml new.yaml`), message formats.
6. **Requirements** linked to changed code (traceability).
7. **Non-functional**: does the change touch hot paths (performance), auth (security), UI layout (visual, accessibility)?

## Output
A short table: area, why impacted, risk, tests to run (existing ids) and new tests needed.

## Gotchas
- Refactors "with no functional change" still change behaviour at edges; treat as medium risk.
- Library/framework upgrades have wide, hidden impact; run full regression plus exploratory on UI.
- Database migrations impact every reader of the table, including reports and ETL.

## Verify
Post-release, escaped defects related to the change fall within the analysed areas; if not, add the missed dependency type to your checklist.
