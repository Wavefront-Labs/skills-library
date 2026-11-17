---
id: computing-software.software-engineering.refactoring.breaking-up-monster-methods
name: breaking-up-monster-methods
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, legacy-code, monster-method, extract-function, sprout-method, sensing-variables]
level: advanced
status: draft
description: "Break up monster methods hundreds of lines long: map them, extract small pieces with automated refactoring, use sensing variables and skeletonize or find-sequences strategies."
sources: ["https://www.oreilly.com/library/view/working-effectively-with/0131177052/", "https://refactoring.com/catalog/extractFunction.html", "https://refactoring.com/catalog/replaceFunctionWithCommand.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Breaking up monster methods

Feathers (WELC ch. 22): **bulleted** methods (long sequence of chunks) and **snarled** methods
(deep nesting, one big chunk). Both are hard to test and fear-inducing.

## Map before cutting
- Print it or use folding: mark sections, nesting depth, which variables are read/written where
  (effect sketch). Some IDEs highlight variable usages; complexity tools (lizard, Sonar) give
  cyclomatic complexity per method.
- Identify responsibilities and the variables that flow between them.

## Strategies
1. **Automated refactoring first.** With few or no tests, use only IDE Extract Method (behaviour-
   preserving by construction). Extract small chunks: conditions into predicates, loop bodies,
   blocks between comments. Rename later.
2. **Sensing variables**: add a temporary field/variable recording what a branch did, assert it in a
   characterisation test, refactor, then remove it.
3. **Extract what you know**: start with pieces with few inputs/outputs (low coupling count).
4. **Gather dependencies**: when part of the method is critical logic and part is side-effect noise,
   extract the noise to leave the logic visible.
5. **Break out a method object** (Replace Function with Command): when locals tangle everything,
   turn the method into a class whose locals become fields, then extract methods freely inside it.
6. **Skeletonize** (snarled methods): extract the condition and body of each block so the original
   becomes a skeleton of calls. **Find sequences** (bulleted): extract each step so the method
   reads as a sequence.

## Tips
- Extract to methods with many parameters at first if needed; consolidate later (Introduce
  Parameter Object).
- Don't fix bugs while extracting; note them, add tests, fix separately.
- Commit after each extraction; small steps you can revert.
- Sprout Method/Class to add new behaviour beside the monster instead of inside it.

## Done when
Each extracted piece has a name that explains it, the top-level method reads as a summary, and
the riskiest pieces have unit tests.
