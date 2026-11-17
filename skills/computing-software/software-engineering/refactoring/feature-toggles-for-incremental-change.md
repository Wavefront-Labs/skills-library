---
id: computing-software.software-engineering.refactoring.feature-toggles-for-incremental-change
name: feature-toggles-for-incremental-change
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, feature-toggles, feature-flags, trunk-based-development, branch-by-abstraction, large-scale-refactoring]
level: practitioner
status: draft
description: "Use feature toggles to ship large refactors incrementally on trunk: release vs ops toggles, toggle points, testing both paths, and removing toggles promptly."
sources: ["https://martinfowler.com/articles/feature-toggles.html", "https://martinfowler.com/bliki/BranchByAbstraction.html", "https://openfeature.dev/docs/reference/intro"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Feature toggles for incremental change

Large refactorings (new pricing engine, ORM swap, rewritten module) shouldn't live on a months-long
branch. Merge continuously behind a toggle and switch when ready.

## Toggle categories (Hodgson, martinfowler.com)
| Type | Lifetime | Dynamism | Example |
|---|---|---|---|
| **Release** | days-weeks | static/per deploy | new checkout code path hidden until done |
| **Experiment** | weeks | per request/user | A/B test |
| **Ops** (kill switch) | short or permanent | runtime | disable recommendations under load |
| **Permission** | long | per user | premium feature |
Refactoring uses release toggles (and sometimes ops toggles for gradual rollout).

## Implementing for a refactor
1. **Branch by abstraction**: introduce an interface in front of the old implementation; all callers
   use it.
2. Build the new implementation behind the same interface, merged to trunk, inactive.
3. Toggle point at **one place** (the factory/composition root), not `if (flag)` sprinkled in 40 files:
   ```java
   PricingEngine engine = flags.isEnabled("new-pricing", ctx) ? newEngine : legacyEngine;
   ```
4. Roll out: internal users -> 1% -> 10% -> 100%, watching errors and comparisons (dark launch).
5. Remove the old implementation, the toggle and the abstraction if no longer needed.

## Practices
- Toggle config via a flag service or library (OpenFeature SDK with LaunchDarkly, Unleash, Flagsmith,
  ConfigCat, or simple config files for release toggles).
- Test both states in CI for the toggle's lifetime; default in tests = production default.
- **Expiry**: each release toggle has an owner and removal date; track as tech debt (ticket created
  with the toggle). Stale toggles multiply code paths (Knight Capital's 2012 loss involved a
  repurposed old flag).
- Keep toggle evaluation out of hot inner loops; evaluate once per request.
