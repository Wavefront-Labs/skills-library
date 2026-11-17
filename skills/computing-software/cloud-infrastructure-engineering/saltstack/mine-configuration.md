---
id: computing-software.cloud-infrastructure-engineering.saltstack.mine-configuration
name: mine-configuration
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, mine, mine-functions, mine-interval, allow-tgt, pillar]
level: practitioner
status: docs-checked
description: "Configure the Salt Mine: mine_functions in minion config or pillar, empty-argument syntax, aliases with mine_function, allow_tgt ACL and the 60 minute interval."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/mine/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Salt Mine configuration

The Mine stores the latest values of chosen functions from each minion on the master, where any minion can read them via `mine.get`. It is far fresher than grains. Long-term history needs returners or the external job cache.

- Define `mine_functions` in the minion config or pillar.
- Functions with no arguments still need an empty list: `test.ping: []`.
- Version 3000+ accepts syntax matching `module.run` arguments; the older format still works.
- Alias or reuse a function with different arguments using the `mine_function` keyword.
- `allow_tgt` and `allow_tgt_type` restrict who may request a function's data; unauthorized callers get nothing.
- Functions run at minion start, then every `mine_interval` (default 60 minutes).

```yaml
mine_functions:
  test.ping: []
  network.ip_addrs:
    - eth0
```

Force an update now with `mine.update`; after changing pillar run `saltutil.refresh_pillar` first.

## Checked

2026-11-04: read the Salt Mine page in full. Confirmed mine_functions in minion config or pillar, the empty-list rule, the 3000 format change, mine_function aliases, allow_tgt and allow_tgt_type (3000), the start-up plus mine_interval schedule with its 60 minute default and mine.update. Nothing removed.

Method: documentation only; no commands were run.

