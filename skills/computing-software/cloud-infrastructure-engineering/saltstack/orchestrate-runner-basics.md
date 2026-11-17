---
id: computing-software.cloud-infrastructure-engineering.saltstack.orchestrate-runner-basics
name: orchestrate-runner-basics
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, orchestrate, state-orchestrate, runner, salt-run, masterless]
level: practitioner
status: docs-checked
description: "Coordinate multi-minion Salt runs with salt-run state.orchestrate: where orch SLS files live, step types, ordering, masterless use and output."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/orchestrate/orchestrate_runner.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Orchestrate runner

The orchestrate runner executes on the master, so requisites can span minions and a run can stop on failure. It replaced OverState in 2015.8.0.

```
salt-run state.orchestrate <sls>
```

`state.orch` is a synonym. Masterless: `salt-call --local state.orchestrate` with `file_mode: local`; only `salt.state` is supported there.

Layout: orchestration SLS files sit beside state files; the docs suggest a dedicated directory such as `_orch/`.

Step types:
- `salt.function`: run an execution module function (custom fail function allowed).
- `salt.state`: apply SLS files or a highstate to matched minions.
- `salt.runner`: call another runner.
- `salt.wheel`: call a wheel function.

Steps run in definition order unless requisites such as `require` change it. Since 2018.3.0 custom runner or wheel functions can report failure via `__context__["retcode"]`.

Output: human-readable by default; the `json` outputter is machine-parsable and, since 2018.3.0, lists failed minions in `changes`.

Inline pillar can be passed on the command line with `pillar=`. States can also run on the master itself, one SLS target at a time.

## Checked

2026-11-09. Read against the orchestrate runner source (doc/topics/orchestrate/orchestrate_runner.rst); commands, versions, step types, masterless limits and output notes were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
