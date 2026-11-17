---
id: computing-software.software-engineering.refactoring.extract-and-decompose-large-classes
name: extract-and-decompose-large-classes
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, extract-method, extract-class, god-class, decomposition, seams, single-responsibility, strangler-fig, incremental-refactoring, code-smell]
level: advanced
status: draft
description: "Break up a god class/function safely: find seams, extract method before extract class, and the ordering that keeps tests green and the diff reviewable."
sources: ["Refactoring (Martin Fowler, 2nd ed.) - Extract Function, Extract Class", "Working Effectively with Legacy Code (Michael Feathers) - seams"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extracting and decomposing large classes — without a week-long unreviewable diff

**Goal:** turn a 2000-line god class or a function with 15 responsibilities into
focused, independently testable units, one small reviewable step at a time, never
breaking behavior along the way.

## 1. Characterize before you cut
If the class/function lacks tests, write characterization tests first (see
computing-software.software-engineering.refactoring.characterisation-tests-and-safe-refactoring)
that pin down its *current* behavior, bugs and all — decomposition is not the place
to also fix a bug; separate those into two distinct changes so a review can tell
"did this change behavior" from the diff alone.

## 2. Find the seams before deciding the shape
A seam (Feathers' term) is a place you can change behavior without editing the code
at that point — an injected dependency, a virtual method, a function boundary. Before
extracting, read the god class for **natural clusters**: which fields are read/written
together, which methods never touch certain fields, which block of code has its own
local variable cluster that doesn't leak elsewhere. These clusters are your future
classes — not an abstract "what should the architecture be" guess, but "what
already behaves like a separate thing in this specific code."

## 3. Extract Method before Extract Class
Always shrink the long function into smaller, named private methods *within the same
class* first:
```
// before: one 200-line method
// after: one 20-line method calling 8 well-named private methods
```
This is lower-risk (no new public surface, no new file, purely internal) and makes
the next step — grouping related extracted methods into a new class — almost
mechanical, because the clusters from step 2 are now visibly separate methods
instead of buried inline code. Skipping straight to Extract Class on a still-tangled
200-line method usually produces a wrong split that gets re-split again later.

## 4. Extract Class: move a cluster, keep the facade
```
// Before: OrderProcessor has 40 methods, including 8 shipping-label methods
// After: OrderProcessor delegates to a new ShippingLabelGenerator
class OrderProcessor {
    private ShippingLabelGenerator labelGen;
    void printLabel(Order o) { labelGen.generate(o); }   // old call sites unchanged
}
```
Move the cluster's methods and the fields they use into the new class; leave a
forwarding method on the original for every existing external caller so the extract
is invisible to the rest of the codebase in that commit — update call sites to use
the new class directly as a **separate, later** commit. This keeps each diff small
and each commit independently safe to revert.

## 5. Order of operations that keeps the diff reviewable
1. Add characterization tests (if missing).
2. Extract Method repeatedly until the long function/class is a sequence of
   well-named calls — commit after each extraction or small batch; run tests after
   every single one.
3. Identify the cluster(s) that deserve to be a new class.
4. Extract Class with a forwarding facade on the original — commit.
5. Update external callers to use the new class directly, deleting the facade once
   nothing references it — a final, separate commit.
6. Only now, if still needed, address any actual design issue (circular dependency,
   wrong abstraction) that was easier to see once the mechanical extraction was done.

## 6. Signals a class/function needs this
- A class whose name has grown vague ("Manager," "Helper," "Processor," "Utils")
  while its responsibilities multiplied — the name stopped being descriptive because
  the class stopped doing one thing.
- A method with more than ~4 levels of indentation, or where you need to scroll to
  see the whole thing to reason about any one part.
- The same group of 3+ fields keeps appearing together in method signatures/usage
  across a subset of the class's methods, while other methods never touch them —
  that's a class hiding inside this one.

## Gotchas
- Extracting while simultaneously renaming or "cleaning up" the extracted code mixes
  two changes in one diff — do the extraction verbatim first (even if the resulting
  names/structure aren't ideal yet), then rename in a follow-up commit; a reviewer
  can verify "pure move, no behavior change" far faster than a move-plus-rewrite.
- A forwarding facade left in place for "just in case" after all callers were
  updated accumulates as dead code — delete it in the same change that updates the
  last caller, not an indefinite later.
- Extract Class purely to reduce line count (an arbitrary split with no behavioral
  cohesion) produces two classes that must always change together — worse than the
  original single class, since now two files need updating for one change. Split
  along the seams from step 2, not by line count.

## Verify
- [ ] Characterization tests exist and pass before the first extraction, and after
      every single extraction step (not just at the end).
- [ ] Each commit is independently revertable: a pure Extract Method or Extract Class
      step, not mixed with a rename or logic change.
- [ ] The new class's name describes what it does in one sentence without "and."
- [ ] No forwarding facade remains after the commit that updates its last caller.

Related: computing-software.software-engineering.refactoring.characterisation-tests-and-safe-refactoring,
computing-software.software-engineering.software-architecture.module-boundaries-and-decomposition
