---
id: computing-software.software-engineering.refactoring.scratch-refactoring-and-effect-sketches
name: scratch-refactoring-and-effect-sketches
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, legacy-code, scratch-refactoring, effect-sketch, feature-sketch, code-comprehension, working-effectively-with-legacy-code]
level: practitioner
status: draft
description: "Understand tangled legacy code fast with scratch refactoring (refactor freely, then throw it away) and effect/feature sketches that map what a change can affect."
sources:
  - https://www.oreilly.com/library/view/working-effectively-with/0131177052/
  - https://martinfowler.com/bliki/ScratchRefactoring.html
  - https://understandlegacycode.com/blog/3-ways-to-understand-legacy-code/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Scratch refactoring and effect sketches

From Michael Feathers, *Working Effectively with Legacy Code* (ch. 11 "I need to make a change. What methods should I test?" and ch. 16 "I don't understand the code well enough to change it").

## Scratch refactoring
Purpose: learning, not shipping. Refactor without tests to see the structure, then discard.
1. Create a throwaway branch: `git switch -c scratch/understand-billing`.
2. Refactor aggressively: extract methods, rename variables to what you think they mean, delete code you believe is dead, inline indirection. No tests needed; commit often so you can review the trail.
3. Write down what you learned (the real responsibilities, hidden dependencies, the seams you would use).
4. Throw it away: `git switch main && git branch -D scratch/understand-billing`. Then do the real change test-first using what you learned.
Discipline: never merge scratch work. The danger is that it "looks done"; without tests you may have changed behaviour.

## Effect sketch
A small hand-drawn graph answering "if I change X, what else can change?"
- Bubble per variable/field and method; arrow from a thing to what its value affects (a field to the methods that read it, a method to its callers' return values).
- Follow arrows outward from the change point; each terminal bubble that is externally observable (public method return, DB write, output) is a place to write a characterisation test.
- **Pinch point:** a narrow place in the sketch where many effects converge (a single method through which most behaviour flows). Testing there covers a lot with few tests.

## Feature sketch
For a big class: bubble per method and field, lines for "uses". Clusters of methods sharing fields reveal hidden classes you can extract (responsibility discovery).

## Other comprehension tactics
- Listing markup: print the method and annotate responsibilities with coloured pens / comments, mark blocks to extract.
- Telling the story of the system in a few sentences; naked CRC cards.
- Tools: IDE call hierarchy (IntelliJ Ctrl+Alt+H), "Find usages", code maps (NDepend dependency graph, Sourcetrail-style navigation), git blame/log for why lines exist (`git log -L :function:file`).

## Verify
- [ ] Scratch branch deleted; learning captured in notes or a test plan.
- [ ] Characterisation tests sit at the pinch points identified in the sketch before the real change.
