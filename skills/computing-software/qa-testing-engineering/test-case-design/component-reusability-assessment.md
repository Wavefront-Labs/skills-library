---
id: computing-software.qa-testing-engineering.test-case-design.component-reusability-assessment
name: component-reusability-assessment
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [reusability-assessment, maintainability-testing, reusability, iso-25010, istqb-tta]
level: advanced
status: draft
description: "Assess reusability of components and libraries: API clarity, dependencies, configuration, documentation, test kits, and trial reuse in a second context."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta
  - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reusability assessment of components and libraries

**Goal:** judge whether a component can be used in another system or context without modification (ISO 25010 maintainability / reusability), before teams commit to sharing it.

## Criteria and how to test each
- **Clear public API:** a documented, minimal interface; internals not exported. Check with an API report (`api-extractor` for TS, `japicmp`/`revapi` for Java) and look for leaked implementation types.
- **Low dependency weight:** list transitive dependencies (`npm ls --all`, `mvn dependency:tree`, `pipdeptree`). Heavy frameworks or pinned versions force them on every consumer.
- **No hidden environment assumptions:** global state, singletons, fixed file paths, specific DB vendor, hard-coded tenant/region.
- **Configurable via parameters**, not edits; sensible defaults.
- **Semantic versioning and changelog;** breaking changes detected automatically in CI.
- **Documentation and examples** that compile; a quick-start a new developer can follow in under an hour.
- **Test kit:** the component's own tests pass standalone, plus fakes or contract tests consumers can use.
- **Licensing** allows the intended reuse.

## Trial reuse
The strongest evidence: integrate the component into a small second consumer (spike app or another service). Record each modification needed; every modification is a reusability defect.

## Score
Rate each criterion 0-2 with evidence links; summarise blockers vs improvements.

## Verify
The assessment lists the criteria scores with evidence, and the trial reuse was completed with zero or explicitly accepted modifications.
