---
id: computing-software.software-engineering.erlang.eunit-basics
name: eunit-basics
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-eunit, eunit-basics]
level: intro
status: docs-checked
description: "EUnit basics: _test and _test_ functions, assert macros, assertMatch, assertException, TEST/NOTEST macros and m_tests modules."
sources:
  - https://www.erlang.org/doc/apps/eunit/chapter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EUnit assertions and test discovery
**Goal:** write and run unit tests quickly.

```erlang
-include_lib("eunit/include/eunit.hrl").
add_test() -> ?assertEqual(3, lists:sum([1,2])).
match_test() -> ?assertMatch({ok, _}, parse(<<"1">>)).
raises_test() -> ?assertError(badarith, 1/0).
exc_test() -> ?assertException(throw, oops, throw(oops)).
list_test_() -> [?_assertEqual(N*2, N+N) || N <- lists:seq(1, 5)].   % generator
```
- Including `eunit.hrl` automatically exports functions named `..._test()` and `..._test_()` (unless testing is turned off or `EUNIT_NOAUTO` is defined). `_test_` functions are generators returning test sets; the `?_assert...` forms wrap an assertion in a fun for that purpose.
- After compiling, call `m:test()` (generated) or `eunit:test(m)` to run a module's tests; `eunit:test({inparallel, m})` runs them in parallel.
- Tests for module `m` can live in a module named `m_tests` (not `m_test`); EUnit runs it too when you test `m`.
- `?assertEqual/2`, `?assertNotEqual/2`, `?assertMatch/2` (a guarded pattern), `?assertNotMatch/2`, `?assertException(Class, Term, Expr)`, `?assertError/2`, `?assertExit/2`, `?assertThrow/2`.
- The `TEST` macro is defined whenever EUnit is enabled; wrap test code in `-ifdef(TEST).` Define `NOTEST` (for example `erlc -DNOTEST`) to disable testing.

## Gotchas
- You do not need to write `-export` declarations for the test functions; do not export them by hand.

## Self-check
Run `eunit:test(Module)` for a module of your own and check the pass count.

## Checked

2026-11-03. Confirmed in the EUnit chapter: auto-export of `_test`/`_test_`, `m:test()`, `eunit:test/1`, `m_tests`, assertion macros, `TEST`/`NOTEST`, `EUNIT_NOAUTO`. Removed: the `rebar3 eunit` commands and flags (not covered by the Erlang docs) and the side-effect gotcha.
Method: documentation only; no commands were run.
