---
id: computing-software.cloud-infrastructure-engineering.saltstack.orchestrate-salt-state-options
name: orchestrate-salt-state-options
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, orchestrate, salt-state, allow-fail, fail-minions, batch, subset, concurrent]
level: advanced
status: docs-checked
description: "Tune salt.state steps in Salt orchestration: tgt, tgt_type, sls/top/highstate, allow_fail, fail_minions, expect_minions, batch, subset, concurrent."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/orchestrate/orchestrate_runner.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# salt.state options in orchestration

Targeting: `tgt` and `tgt_type`.

Exactly one of `sls`, `top` or `highstate` selects what to apply.

Failure handling:
- `allow_fail`: tolerated number of failing minions.
- `fail_minions`: minions whose failure is acceptable.
- `expect_minions` (default `True`): the step fails if a targeted minion does not respond.
- `failhard`: propagate Salt's global `failhard` setting to the child run.

Threshold pattern: to require at least N successes, set `allow_fail` to the matched minion count minus N.

Concurrency: `batch`, `subset`, `concurrent`, `queue`. Returners and SSH dispatch are also supported.

## Checked

2026-11-09. Read against the orchestrate runner source (doc/topics/orchestrate/orchestrate_runner.rst); the option list, defaults and the allow_fail threshold pattern were confirmed there. Corrected the failhard and expect_minions descriptions.
Method: documentation only; no commands were run.
