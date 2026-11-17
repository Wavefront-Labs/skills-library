---
id: computing-software.qa-testing-engineering.test-case-design.modularity-and-modifiability-assessment
name: modularity-and-modifiability-assessment
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [modularity-assessment, maintainability-testing, modifiability, coupling-metrics, iso-25010, istqb-tta]
level: advanced
status: docs-checked
description: "Assess modularity and modifiability: coupling and cohesion metrics, dependency-cycle checks, change-impact sampling and architecture rules enforced in CI."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta
  - https://www.archunit.org/userguide/html/000_Index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Modularity and modifiability assessment

**Goal:** give evidence, not opinion, on how easy the code is to change (maintainability), and stop it degrading.

## Static measures
- **Dependency cycles** between packages/modules: should be zero. ArchUnit example: `slices().matching("com.myapp.(*)..").should().beFreeOfCycles()`.
- **Coupling:** count incoming and outgoing dependencies per module; stable core modules should be depended on by many, volatile UI modules by few.
- **Size and complexity hotspots:** files over agreed size, cyclomatic complexity per function (from your static-analysis tooling).
- **Code churn x complexity:** files that change most often and are most complex are where modifiability hurts (from version-control history).

## Dynamic / empirical measures
- **Change impact sampling:** take 5-10 recent typical change requests; count files and modules touched per change. Many modules per small feature = poor modularity (shotgun surgery).
- **Lead time per change** and defects introduced per change (from Git + defect tracker).
- **Build/test isolation:** can one module be built and tested alone?

## Enforce
Encode layer rules as tests (for example ArchUnit `layeredArchitecture()`) so violations fail CI.

```java
@ArchTest static final ArchRule layers = layeredArchitecture().consideringAllDependencies()
  .layer("Web").definedBy("..web..").layer("Domain").definedBy("..domain..")
  .whereLayer("Domain").mayOnlyBeAccessedByLayers("Web");
```

## Verify
The assessment report lists cycles (target zero), hotspot files, and average modules touched per sampled change, and architecture rules run in CI.

## Checked

2026-10-28. Confirmed: ArchUnit user guide (cycle check `slices().matching(..).should().beFreeOfCycles()`, `layeredArchitecture()`, `definedBy`, `mayOnlyBeAccessedByLayers`). Removed: ISO 25010 wording (source unreadable), the instability formula, tool names and commands not in the sources (madge, import-linter, JDepend, NDepend, SonarQube, radon, lizard, git log pipeline, dependency-cruiser).

Method: documentation only; no commands were run.
