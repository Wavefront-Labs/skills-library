---
id: computing-software.systems-network-administration.ceph.balancer-supervised-plans
name: balancer-supervised-plans
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, balancer, plan, eval, optimize, execute]
level: advanced
status: docs-checked
description: "Run the Ceph balancer by hand: score the distribution, build a named plan, review it and execute it."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/balancer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Supervised mode lets you see what the balancer will do before it moves data. Score the present distribution, lower is better:

```
ceph balancer eval
ceph balancer eval <pool-name>
ceph balancer eval-verbose
```

Build, inspect and apply a plan:

```
ceph balancer optimize <plan-name>
ceph balancer show <plan-name>
ceph balancer eval <plan-name>
ceph balancer execute <plan-name>
```

Housekeeping:

```
ceph balancer ls
ceph balancer rm <plan-name>
```

`ceph balancer eval <plan-name>` scores the distribution as it would be after the plan, so you can compare it with the current score before you run `execute`. Discard a plan you do not like with `ceph balancer rm`.

Typical flow: turn the automatic balancer off with `ceph balancer off`, choose a mode with `ceph balancer mode upmap`, create the plan, compare scores, then execute and watch `ceph -s` while data moves.

For more detail on what the automatic balancer has been doing, turn on activity logging and read the detailed status:

```
ceph config set mgr mgr/balancer/update_pg_upmap_activity True
ceph balancer status detail
```

## Checked

2026-11-03. Confirmed against: the Ceph Balancer Module page (docs.ceph.com/en/latest/rados/operations/balancer/): Supervised optimization (eval, optimize, show, ls, rm, execute, status detail, update_pg_upmap_activity).

Removed: nothing.

Method: documentation only; no commands were run.
