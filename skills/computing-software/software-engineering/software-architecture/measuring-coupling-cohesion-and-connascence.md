---
id: computing-software.software-engineering.software-architecture.measuring-coupling-cohesion-and-connascence
name: measuring-coupling-cohesion-and-connascence
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-evaluation, coupling-metrics, connascence, cohesion, afferent-coupling, instability]
level: advanced
status: draft
description: "Measure modularity with afferent/efferent coupling, instability and abstractness, LCOM cohesion and connascence, using tools, and act on what the numbers show."
sources: ["https://connascence.io/", "https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/", "https://github.com/sverweij/dependency-cruiser", "https://jdepend.github.io/jdepend/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Measuring modularity: coupling, cohesion, connascence

## Coupling metrics (Robert Martin, package/module level)
- **Ca** afferent: modules that depend on this one (responsibility).
- **Ce** efferent: modules this one depends on.
- **Instability** I = Ce / (Ca + Ce): 0 stable (hard to change, many dependents), 1 unstable.
- **Abstractness** A = abstract types / total types.
- **Distance from main sequence** D = |A + I - 1|: near 0 good. High D near (0,0) = "zone of pain"
  (concrete and depended upon, e.g. a utils module everyone imports); near (1,1) = "zone of
  uselessness" (abstractions nobody uses).
- Stable dependencies principle: depend in the direction of stability.

Tools: JDepend / ArchUnit (Java), NDepend (.NET), dependency-cruiser and madge (JS/TS), pydeps +
import-linter (Python), Structure101, SonarQube. Track trends per release, not absolute values.

## Cohesion
LCOM (lack of cohesion of methods): classes whose methods use disjoint field sets are really
several classes. Use as a pointer for review, not a target.

## Connascence (Page-Jones; connascence.io)
Two components are connascent if changing one requires changing the other.
- Static, weakest to strongest: **name**, **type**, **meaning** (magic values), **position**
  (argument order), **algorithm** (both sides must hash the same way).
- Dynamic: **execution** order, **timing**, **values** (must change together), **identity**
  (same instance).
Rules: refactor towards weaker forms (position -> name via keyword args/parameter objects; meaning
-> named constants/enums), keep strong connascence local (same function/class), and degree (how many
places) matters as much as type.

## Acting on it
Hot spots = high coupling x high change frequency (from git log: `code-maat`, CodeScene). Fix
those first; a highly coupled module nobody changes is cheap.
