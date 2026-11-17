---
id: computing-software.software-engineering.erlang.eunit-fixtures
name: eunit-fixtures
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-eunit, eunit-fixtures]
level: practitioner
status: docs-checked
description: "EUnit fixtures: setup, foreach, Where (spawn/local), timeout, inorder, inparallel and setup/cleanup semantics."
sources:
  - https://www.erlang.org/doc/apps/eunit/chapter.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fixtures, setup and test control
**Goal:** run tests with shared resources.

```erlang
db_test_() ->
    {setup,
     fun() -> {ok, P} = db:start(), P end,        % setup
     fun(P) -> db:stop(P) end,                    % cleanup
     fun(P) -> [?_assertEqual(ok, db:put(P, a, 1)),
                ?_assertEqual({ok, 1}, db:get(P, a))] end}.
```
- `{setup, Setup, Cleanup, Instantiator}` runs `Setup` once before the tests, passes its return value to `Cleanup` and to the instantiator, and runs `Cleanup` when no more of the tests will run, regardless of the reason. `{foreach, Setup, Cleanup, [Tests | Instantiator]}` repeats the fixture for each test set. When no `Cleanup` is given a dummy function is used.
- `{timeout, Seconds, Tests}` sets a timeout in seconds (the default for an individual test is 5 seconds). A timeout around a fixture includes setup and cleanup; if it triggers, the whole fixture is terminated without running cleanup.
- `{inorder, Tests}` runs tests in strict order; `{inparallel, Tests}` (or `{inparallel, N, Tests}`) runs them in parallel; `{spawn, Tests}` runs them in a separate subprocess.
- The optional `Where` argument of `setup`/`foreach` is `spawn` (the default: the current process does setup and teardown while the tests run in a subprocess), `{spawn, Node}`, or `local` (one process does both).

## Gotchas
- With `local`, if a test times out and the process is killed, cleanup is not performed; avoid it for persistent fixtures such as file operations.

## Self-check
Make a failing test inside a fixture and confirm cleanup still runs.

## Checked

2026-11-03. Confirmed in the EUnit chapter ("Fixtures", "Control" primitives, setup/cleanup semantics, `Where`, default 5-second timeout). Removed: the ETS and socket ownership advice, the `erlang:processes()` leak check, and the claim that all fixtures run in different processes.
Method: documentation only; no commands were run.
