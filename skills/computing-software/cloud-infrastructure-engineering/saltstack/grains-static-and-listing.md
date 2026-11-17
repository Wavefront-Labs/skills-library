---
id: computing-software.cloud-infrastructure-engineering.saltstack.grains-static-and-listing
name: grains-static-and-listing
category: computing-software
field: cloud-infrastructure-engineering
product: saltstack
tags: [saltstack, grains, static-grains, grains-items, grains-ls, minion-config]
level: intro
status: docs-checked
description: "List Salt grains and define static ones in the minion config or /etc/salt/grains, including proxy minion location and refreshing after changes."
sources:
  - https://raw.githubusercontent.com/saltstack/salt/master/doc/topics/grains/index.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static grains and listing

List:

```
salt '*' grains.ls
salt '*' grains.items
salt-call --local grains.items
```

The last form checks a masterless minion. Grain names are case-insensitive and resolve to lowercase.

Static grains:
- In `/etc/salt/minion`, under a top-level `grains:` key.
- In `/etc/salt/grains`, the same pairs without the `grains:` key.
- If defined in both, the minion config wins.
- Proxy minions: `/etc/salt/proxy.d/<minion ID>/grains`.

Static grains are not reloaded automatically. After editing, refresh with `saltutil.refresh_modules` as the page states it (for example `salt 'minion' saltutil.refresh_modules`).

## Checked

2026-11-09. Read against the grains source (doc/topics/grains/index.rst); listing commands, static grain locations, precedence between them, the proxy path and the refresh note were confirmed there. Nothing removed.
Method: documentation only; no commands were run.
