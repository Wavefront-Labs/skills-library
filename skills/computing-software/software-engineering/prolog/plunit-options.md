---
id: computing-software.software-engineering.prolog.plunit-options
name: plunit-options
category: computing-software
field: software-engineering
product: prolog
tags: [prolog, plunit-options, plunit-setup-cleanup]
level: advanced
status: docs-checked
description: "Control plunit tests with test and unit options such as true, fail, throws, setup, cleanup, blocked and condition."
sources:
  - https://www.swi-prolog.org/pldoc/doc_for?object=section(%27packages/plunit.html%27)
  - https://raw.githubusercontent.com/SWI-Prolog/packages-plunit/master/plunit.pl
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# plunit options and CI
```prolog
:- begin_tests(db, [setup(assertz(t(1))), cleanup(retractall(t(_)))]).
test(has, [setup(assertz(t(2))), cleanup(retractall(t(2)))]) :- t(2).
test(sq, [forall(member(X, [1,2])), true(Y =:= X*X)]) :- Y is X*X.
:- end_tests(db).
:- set_test_options([format(log), output(on_failure)]).
```
CI command, which exits 0 when the suite succeeds and 1 when it does not:
`swipl -g run_tests -t halt tests.pl`
Check it with `echo $?`.
- Unit options (`begin_tests/2`): `blocked(Reason)`, `condition(Goal)`, `setup(Goal)` (once before the unit's tests), `cleanup(Goal)` (after all tests of the unit), `occurs_check(Mode)`.
- Test options: `setup(Goal)` runs before the test body, `cleanup(Goal)` always runs afterwards; `forall(Generator)` reruns the test (with setup and cleanup) for each solution.
- `set_test_options/1`: `load(never|always|normal)`, `run(manual|make|make(all))`, `format(tty|log)`, `output(always|never|on_failure)`, `show_blocked(Bool)`, `occurs_check(Mode)`, `cleanup(Bool)`, `jobs(Num)`, `timeout(Seconds)`.
## Gotchas
- `format(tty)` (default on a console) overwrites passing tests; use `format(log)` for non-interactive output.
- `set_test_options([load(never)])` before loading the application leaves tests out of a production build.
- `timeout(Seconds)` is a default that unit and test options may override; 0 or negative means infinite.
## Self-check
Make a failing test and verify the shell exit status is 1 with `echo $?`.

## Checked

2026-11-03. SWI-Prolog manual "Prolog Unit Tests": test options (setup, cleanup, forall, true), unit options for begin_tests/2, set_test_options/1 option list and meanings, section 4.2 command line and 0/1 exit status, section 5 `load(never)`. Removed: the `silent(true)` option (not in the documented list), the unconfirmed `-g "run_tests,halt(0)" -t "halt(1)"` command and the "varies by version" remarks.

Method: documentation only; no commands were run.
