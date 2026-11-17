---
id: computing-software.cloud-infrastructure-engineering.saltstack.grains-custom-modules
name: grains-custom-modules
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, grains, custom-grains, sync-grains, grains-dir, python]
level: practitioner
status: docs-checked
description: "Write custom Salt grain modules in _grains: return dictionaries, underscore helpers, syncing to minions, and the top-file availability limit."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/grains/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom grain modules

Put Python files in `_grains` under the master's `file_roots` (default `/srv/salt/_grains`).

- Each public function must return a dictionary; its keys become grain names. The function name does not matter.
- Prefix helpers with an underscore so their return values do not become grains.
- A function that accepts a `grains` argument receives earlier-rendered grains, but only core grains are guaranteed present (2019.2.0).

Distribute to minions with any of:

```
salt '*' state.highstate
salt '*' saltutil.sync_grains
salt '*' saltutil.sync_all
```

Limit: custom grains are not available in the top file until after the first highstate. To have them ready at minion startup, the page points to a minion-start reactor example.

Caching: with `grains_cache` False, grains are built and kept in memory, rebuilt on every minion restart or `saltutil.refresh_grains`.

## Checked

2026-11-09. Read against the grains source (doc/topics/grains/index.rst); the _grains path, return rules, underscore helpers, sync functions, top-file limit and grains_cache note were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
