---
id: computing-software.software-engineering.prolog.plunit-basics
name: plunit-basics
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, prolog-testing, plunit-basics, run-tests]
level: practitioner
status: docs-checked
description: "Write and run plunit tests in SWI-Prolog: test blocks, options, running tests and reading results."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=section(%27packages/plunit.html%27)
  - https://raw.githubusercontent.com/SWI-Prolog/packages-plunit/master/plunit.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# plunit basics
```prolog
:- use_module(library(plunit)).
:- begin_tests(arith).
test(add) :- 2 =:= 1 + 1.
test(sum, X == 7) :- X is 3 + 4.
test(div0, error(evaluation_error(zero_divisor))) :- _ is 1/0.
test(no, fail) :- 1 =:= 2.
test(all, all(X == [1,2,3])) :- member(X, [1,2,3]).
test(pick, [nondet, true(X == a)]) :- member(X, [a,b]).
:- end_tests(arith).
```
Run: `?- run_tests.` or `?- run_tests(arith).` (a unit name, or `Unit:Test`), or `swipl -g run_tests -t halt file.pl`, which exits with status 0 or 1 depending on whether the suite succeeds.
Test options: `true(AnswerTerm Cmp Value)` (Cmp is typically `=`, `==`, `=:=` or `=@=`), `fail`, `throws(Error)` (matched with `subsumes_term/2`), `error(Formal)`, `all(Var == List)` (order matters), `set(Var == List)` (both sorted with `sort/2` first), `nondet`, `blocked(Reason)`, `condition(Goal)`, `setup(Goal)`, `cleanup(Goal)`, `forall(Generator)`, `occurs_check(Mode)`.
## Gotchas
- A body that leaves a choice point prints a warning to stderr unless the test has `nondet` (or the body ends in `!`).
- Without options the body must succeed deterministically; failing is a test failure.
- Tests can live in the source file or in a separate `foo.plt` file; load the code, then run `run_tests`.
- `assertion/1` in a test body reports failures without trapping the debugger.
## Self-check
Write a failing test and confirm the failure report names the file and line.

## Checked

2026-11-03. SWI-Prolog manual "Prolog Unit Tests" (packages/plunit): test box and option list (true, fail, throws, error, all, set, nondet, blocked, condition, setup, cleanup, forall, occurs_check), the `=@=` footnote, `.plt` files, run_tests/0,1 with `Unit:Test`, command line `swipl -g run_tests -t halt` and its 0/1 exit status, the choice-point warning and the assertion/1 section. Removed: nothing factual; the source list now names the plunit manual.

Method: documentation only; no commands were run.
