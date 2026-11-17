---
id: computing-software.software-engineering.refactoring.getting-a-class-into-a-test-harness
name: getting-a-class-into-a-test-harness
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, legacy-code, test-harness, dependency-breaking, characterization-tests, seams]
level: advanced
status: draft
description: "Get a legacy class instantiated in a test harness: diagnose construction blockers (hidden dependencies, irritating parameters, globals), apply Feathers' dependency-breaking moves."
sources: ["https://www.oreilly.com/library/view/working-effectively-with/0131177052/", "https://martinfowler.com/bliki/LegacySeam.html", "https://michaelfeathers.silvrback.com/characterization-testing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Getting a class into a test harness

Feathers, WELC ch. 9 "I Can't Get This Class into a Test Harness". The first goal is just to
**construct the object in a test**; then you can write characterisation tests and change safely.

## Step 0: try the obvious
Write the test that constructs it and see what fails ("let the compiler tell you"). Often it's
less bad than feared.

## Common blockers and moves
| Blocker | Move |
|---|---|
| **Irritating parameter**: constructor takes a heavy object (DB connection, `HttpServletRequest`) | pass `null` if unused on the tested path (Pass Null); Extract Interface and pass a fake; subclass a fake |
| **Hidden dependency**: constructor news up collaborators (`new MailService()`) | Parameterize Constructor (keep old ctor delegating with the default) |
| **Construction blob**: constructor builds a web of objects | Extract and Override Factory Method; or Supersede Instance Variable (setter used only by tests) |
| **Irritating global/singleton**: constructor calls `Config.getInstance()` | Introduce Static Setter on the singleton for tests, or Encapsulate Global References, then inject |
| **Horrible include dependencies** (C++) | link-time seams: compile with fake implementations of the headers |
| **Onion parameter** (needs object needing object...) | build with test builders, or extract an interface at the outermost layer |
| **Aliased parameter** (final class you can't fake) | Extract Interface on a wrapper; or subclass-and-override where allowed |

## Rules while breaking dependencies without tests
- Minimal, mechanical edits only, preferably IDE refactorings ("Preserve Signatures" when editing
  by hand: copy/paste whole signatures, don't retype).
- Lean on the compiler: change a type and let errors show all usages.
- Each move adds a **seam**: a place where behaviour can change without editing the code there.

## Then
Write characterisation tests: call the code, assert whatever it currently returns (even if it
looks wrong), and grow coverage around the area you'll change. Approval/snapshot testing
(ApprovalTests, Verify, syrupy) speeds this up for large outputs.
