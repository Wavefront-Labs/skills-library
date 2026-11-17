---
id: computing-software.software-engineering.nim.doctests-and-runnable-examples
name: doctests-and-runnable-examples
category: computing-software
field: software-engineering
product: nim
tags: [doctests-and-runnable-examples, unit-testing, runnableexamples, doctest, testament, test-spec, nim-doc, golden-output, nim]
level: advanced
status: docs-checked
description: "Embed tested examples in docs with runnableExamples, and run larger test suites with testament specs."
sources:
  - https://github.com/nim-lang/Nim/blob/devel/doc/testament.md
  - https://github.com/nim-lang/Nim/blob/devel/doc/advopt.txt
  - https://github.com/nim-lang/Nim/blob/devel/lib/core/macros.nim
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Doctests: runnableExamples and testament

Goal: keep documentation honest and test compiler-level behaviour.

- In a proc or type: put `runnableExamples:` (an indented block of code with asserts) right after the doc comment, as the stdlib does in `macros.nim`.
- `nim doc` runs those examples. The `--docCmd:cmd` switch controls it: `--docCmd:skip` skips runnableExamples, any other value runs them with those options, e.g. `--docCmd:"-d:foo --threads:on"`.
- `testament` is the test runner used for Nim itself: process isolation, several targets (C, C++, ObjectiveC, JavaScript), statistics, HTML reports.
- By default it looks for `./tests/category/*.nim`. Commands: `testament all` (every test in category folders), `testament pattern "tests/*.nim"`, `testament category <category>`, `testament run <test>`, `testament html` (writes `testresults.html`; run at least one test first).
- A test's spec is a leading `discard """ ... """` block. Fields include `action` (`"compile"`, `"run"`, `"reject"`), `exitcode`, `output`, `outputsub`, `nimout`, `errormsg`, `input`, `cmd`, `timeout`, `targets` (default c), `matrix` (flags delimited by `;`) and `disabled`.
- Use testament for expected compile errors (`errormsg`, `action: "reject"`), several backends (`targets: "c js"`) and flag matrices (`matrix: "; -d:release"`).
- `--targets:"js"` needs a working NodeJS on `PATH`.

Gotchas:
- A test with no spec works too: a plain `assert` is enough (the spec has defaults).
- Any `$` in `errormsg`, `nimout` or `cmd` that is not an interpolation variable must be written `$$`.

Verify: a deliberately wrong assert in a test file makes `testament run <test>` report a failure.

## Checked

2026-11-08. Read in full: doc/testament.md (default location, commands, options, spec fields, `$$` escaping, no-spec tests) and doc/advopt.txt (`--docCmd` text) from nim-lang/Nim. For runnableExamples placement, searched lib/core/macros.nim for the usage after a doc comment (partial read; the stdlib convention only). Removed: "ships with Nim", the claim that a failing example breaks the docs build, import-in-example advice, the "needs Nim sources layout" gotcha and the fuzz/property-test package suggestions (none confirmed). manual.md, tut1.md and lib.html dropped from sources.
Method: documentation only; no commands were run.
