---
id: computing-software.software-engineering.erlang.ct-config-hooks
name: ct-config-hooks
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-common-test, ct-config-hooks]
level: advanced
status: draft
description: "Common Test config files, ct_hooks, test specifications, cover analysis and rebar3 ct configuration."
sources:
  - https://www.erlang.org/doc/apps/common_test/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Config files, hooks and cover
**Goal:** pass configuration and plug into the test lifecycle.

- `ct:get_config(key)` reads values from files given via `-config` (`rebar3 ct --config=test/ct.config`); files are Erlang terms.
- `suite() -> [{ct_hooks, [cth_surefire]}]` adds hooks; `cth_surefire` writes JUnit XML for CI.
- `{ct_opts, [{sys_config, ["config/test.config"]}]}.` in `rebar.config` loads app env for tests.
- `rebar3 ct --cover` then `rebar3 cover --verbose` prints coverage.
- Test specs (`.spec` files) list suites and dirs: `{suites, "test", [api_SUITE]}.`
```
rebar3 ct --cover --readable=true --verbose
rebar3 cover
```

## Gotchas
- Hooks run in the CT process tree; a crashing hook fails the whole run.

## Self-check
Produce a surefire XML report and open it in your CI viewer.
