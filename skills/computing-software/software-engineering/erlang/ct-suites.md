---
id: computing-software.software-engineering.erlang.ct-suites
name: ct-suites
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-common-test, ct-suites]
level: practitioner
status: draft
description: "Common Test suite layout: all/0, init_per_suite, init_per_testcase, ct:pal, ?config and rebar3 ct options."
sources:
  - https://www.erlang.org/doc/apps/common_test/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Suites, test cases and run options
**Goal:** write and run an integration suite.

```erlang
-module(api_SUITE).
-include_lib("common_test/include/ct.hrl").
-export([all/0, init_per_suite/1, end_per_suite/1, hello/1]).
all() -> [hello].
init_per_suite(Config) -> {ok, _} = application:ensure_all_started(myapp), Config.
end_per_suite(_Config) -> application:stop(myapp), ok.
hello(Config) ->
    ct:pal("priv_dir ~p", [?config(priv_dir, Config)]),
    {ok, _} = httpc:request("http://localhost:8080/").
```
```
rebar3 ct
rebar3 ct --suite=test/api_SUITE --case=hello
```
- Suites are modules named `*_SUITE` in `test/`; a case is a function of arity 1 taking `Config`.
- A case passes if it returns normally; failures are exceptions or `ct:fail/1`.
- `suite() -> [{timetrap, {seconds, 30}}]` sets the default time limit.
- Logs: `_build/test/logs/`, open `index.html`.

## Gotchas
- Config values from `init_per_suite` are shared by all cases; return the modified Config.
- Default timetrap is 30 minutes; set a shorter one.

## Self-check
Run a suite with a failing case and open the HTML log.
