---
id: computing-software.software-engineering.refactoring.characterisation-tests-and-safe-refactoring
name: characterisation-tests-and-safe-refactoring
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, legacy-code, characterisation-tests, characterization-tests, approval-tests, golden-master, snapshot-testing, seams, dependency-breaking, sprout-method, wrap-method, strangler-fig, branch-by-abstraction, feature-flags, parallel-change, expand-contract, mutation-testing, pitest, stryker, mutmut, automated-refactoring, small-steps, software-engineering]
level: practitioner
status: draft
description: "Change legacy code without breaking it: pin current behaviour with characterisation/approval tests, cut seams, refactor in tiny green steps, and migrate via strangler fig or branch by abstraction."
sources: ["Feathers, Working Effectively with Legacy Code", "Fowler, Refactoring (2nd ed.)", "Fowler, StranglerFigApplication and BranchByAbstraction articles (martinfowler.com)", "ApprovalTests project documentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Characterisation tests and safe refactoring — change code you don't trust

**Goal:** improve the structure of untested or poorly understood code while proving,
at every step, that its observable behaviour has not changed.

## 1. Pin what the code does today (not what it should do)
A characterisation test records actual behaviour, bugs included.
1. Call the code with a representative input and assert something obviously wrong
   (`assertEquals("x", result)`).
2. Run it; the failure tells you the real output. Paste that in as the expectation.
3. Repeat for edge cases: empty, null, boundaries, error paths, odd locales/timezones.
4. If you find a bug, **keep the test pinned to the buggy output** and file the bug;
   fixing behaviour and refactoring in one step removes your safety net.

For outputs too large to hand-assert (reports, HTML, JSON, rendered invoices) use
**approval / golden-master testing**: serialise the output, store it as an approved
file, diff on every run.
- ApprovalTests (Java, .NET, Python, JS…): `Approvals.verify(output)` writes
  `*.received.*` and compares to `*.approved.*`.
- Snapshot tools: Jest/Vitest `toMatchSnapshot()`, `syrupy` for pytest, `insta` for Rust,
  Verify for .NET.
- **Combination approvals:** feed the cartesian product of input values
  (`verifyAllCombinations`) to cover branches cheaply.
Scrub non-determinism first: fix the clock, seed RNGs, sort unordered collections,
replace generated ids/timestamps with placeholders.

## 2. Check the net actually catches things
Coverage shows lines executed, not behaviour asserted. Before a risky refactor:
- Look at branch coverage of the target (`coverage run --branch`, JaCoCo, `c8`/Istanbul).
- Run **mutation testing** on that area: PIT (`mvn org.pitest:pitest-maven:mutationCoverage`),
  Stryker (`npx stryker run`), `mutmut run`, cargo-mutants. Surviving mutants mark
  behaviour your tests don't pin.

## 3. Create seams to get code under test
A **seam** is a place where you can change behaviour without editing the code there.
- **Object seam:** extract an interface or pass a collaborator via constructor/parameter
  instead of `new`-ing it inside (parameterise constructor; default argument keeps
  callers unchanged).
- **Extract and override:** move the hard call (`DateTime.Now`, HTTP, DB) into a
  protected method; subclass it in the test.
- **Link/module seam:** swap an import or module at test time (`unittest.mock.patch`,
  `jest.mock`) — useful, but couples the test to module layout.
- Adding new behaviour to untestable code: **sprout method/class** (write the new
  logic in a fresh, tested unit and call it from the old code) or **wrap method**
  (rename the old one, create a new one that calls it plus the new step).
Prefer the IDE's automated refactorings over hand edits.

## 4. Refactor in small, always-green steps
- One refactoring at a time from the catalogue: rename, extract function, inline,
  move, introduce parameter object, replace conditional with polymorphism.
- Run the tests after every step (seconds, not minutes — run the focused subset with
  watch mode). Commit on every green; a refactoring session should leave a trail of
  tiny commits you can bisect or revert.
- Never mix refactoring and behaviour change in one commit. Label them
  (`refactor:` vs `feat:`/`fix:`) so reviewers can skim the former.
- Red and unclear why within minutes? `git checkout .` back to green; take a smaller step.

## 5. Large-scale moves without big-bang rewrites
- **Parallel change (expand / migrate / contract):** add the new API alongside the old,
  move callers over one by one, then delete the old. Works for functions, columns,
  endpoints.
- **Branch by abstraction:** introduce an abstraction over the component to replace,
  point all callers at it, build the new implementation behind it, switch with a
  feature flag (optionally per tenant or percentage), then remove the old
  implementation and, if useful, the abstraction. Trunk stays releasable throughout.
- **Strangler fig:** for a whole system, put a routing facade (reverse proxy, API
  gateway, or in-process router) in front; route one capability at a time to the new
  system; retire the legacy piece when it receives zero traffic. Track remaining routes.
- During cut-over, run old and new side by side and compare outputs (Scientist-style
  experiments) before trusting the new path.

## Gotchas
- Snapshot tests approved without reading them pin garbage; review every approved file.
- Over-mocked tests break on every structural change and block the refactor they
  should enable; prefer testing through a stable public boundary.
- Strangler projects stall at 80%; the last routes are the hardest. Budget for them
  and delete legacy code as you go, or you run two systems forever.

## Verify
- [ ] The code being changed has tests that fail when you deliberately break it.
- [ ] Approved/golden files are deterministic and were reviewed by a human.
- [ ] Each commit is either pure refactoring or behaviour change, never both.
- [ ] The test suite was green after every commit in the series.
- [ ] Migrations use parallel change, branch by abstraction or strangler fig with a
      tracked removal step for the old path.

Related: computing-software.software-engineering.debugging.systematic-debugging
