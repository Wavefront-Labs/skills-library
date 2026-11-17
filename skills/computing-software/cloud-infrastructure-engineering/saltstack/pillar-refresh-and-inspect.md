---
id: computing-software.cloud-infrastructure-engineering.saltstack.pillar-refresh-and-inspect
name: pillar-refresh-and-inspect
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, pillar, refresh-pillar, pillar-items, pillar-get, pillar-cache]
level: practitioner
status: docs-checked
description: "Refresh and inspect Salt pillar: saltutil.refresh_pillar, pillar.items vs pillar.item vs pillar.raw, pillar.get, and clearing the pillar cache."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/pillar/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh and inspect pillar

Minions keep pillar in memory, loaded at startup.

Refresh:

```
salt '*' saltutil.refresh_pillar
```

It runs asynchronously and returns `None`. Running states or `pillar.items` compiles fresh data but does not refresh the in-memory copy.

If `pillar_cache: True`, clear a minion's cache on the master:

```
salt-run pillar.clear_pillar_cache 'minion'
```

View:
- `pillar.item`: keys from in-memory data.
- `pillar.items`: compiles fresh data; with keys passed it behaves like `pillar.item`.
- `pillar.raw`: the full in-memory dictionary.
- `pillar.get`: `:` separates nested keys, with an optional default.

```
salt '*' pillar.get foo:bar:baz
```

## Checked

2026-11-04: read the Salt pillar reference page in full. Confirmed in-memory pillar, refresh_pillar (asynchronous, returns None), what does and does not refresh it, clear_pillar_cache with pillar_cache, and the item, items, raw and get descriptions. Nothing removed.

Method: documentation only; no commands were run.

