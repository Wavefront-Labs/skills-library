---
id: computing-software.cloud-infrastructure-engineering.saltstack.states-failhard
name: states-failhard
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, states, failhard, error-handling, master-config]
level: practitioner
status: docs-checked
description: "Halt a Salt state run on first failure with failhard at state level or globally in the master config, and why global failhard is discouraged."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/failhard.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# failhard

Default: Salt keeps running the remaining states after a failure and skips only states that depend on the failed one. `failhard` halts everything instead.

State level, for critical early steps such as a package repository config:

Set `failhard: True` on the state itself.

Global level: set `failhard: True` in the master config; any failure on a minion then stops execution. Not the default, and the docs advise against it because it can leave states unexecuted and surprise admins who do not know it is on. A state can opt out of a global setting with `failhard: False`.

## Checked

2026-11-04: read the Salt failhard page in full. Confirmed default behaviour, state-level and global failhard, the False override and the advice against global use. Removed the claim that failhard disables onfail requisites, which the page does not state.

Method: documentation only; no commands were run.

