---
id: computing-software.cloud-infrastructure-engineering.saltstack.states-test-mode
name: states-test-mode
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, states, test-mode, dry-run, state-apply]
level: intro
status: docs-checked
description: "Preview Salt state changes without applying them using test=True, read the yellow None results, and default the minion to test mode with test=False override."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/ref/states/testing.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State test mode

Preview what a run would change:

```
salt '*' state.apply test=True
```

`test=True` works on state functions such as `state.apply` and `state.single`.

Reading output: pending changes show in yellow with result `None`.

Default to test mode: set `test: True` in the minion config file. Even then, run for real with:

```
salt '*' state.apply test=False
```

## Checked

2026-11-04: read the Salt state testing page in full. Confirmed test=True on state.apply and state.single, yellow output with result None, the minion test default and the test=False override. Nothing removed.

Method: documentation only; no commands were run.

