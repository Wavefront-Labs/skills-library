---
id: computing-software.database-administration.dragonfly.memcached-mode
name: memcached-mode
category: computing-software
field: database-administration
product: dragonfly
tags: [memcached, memcached-port, dragonfly]
level: intro
status: docs-checked
description: "Serve Memcached clients from Dragonfly by setting the --memcached_port flag, or memcachedPort in the Kubernetes Operator Dragonfly resource."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/flags.md
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/operator/dragonfly-configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Enable the Memcached protocol on a separate port:

```bash
dragonfly --memcached_port 11211
```

The flag's default is `0`.

Kubernetes Operator: set `memcachedPort` (int, since v1.1.2) in the Dragonfly resource spec; the operator page says to use it instead of the `--memcached_port` arg.

## Checked

2026-11-04. Confirmed against the Dragonfly flags page (`--memcached_port`, default 0) and the operator configuration page (`memcachedPort`, since v1.1.2). Removed the claims that Memcached shares Redis database 0 and supports strings only: neither page states them.

Method: documentation only; no commands were run.
