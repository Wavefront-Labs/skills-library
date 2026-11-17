---
id: computing-software.systems-network-administration.ceph.mon-election-strategy
name: mon-election-strategy
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, monitor, election, connectivity, disallowed-leader]
level: advanced
status: docs-checked
description: "Choose the monitor election strategy (classic, disallow, connectivity) and keep chosen monitors from becoming leader."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/change-mon-elections/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set the strategy:

```
ceph mon set election_strategy {classic|disallow|connectivity}
```

- `classic`: the default and the simplest mode; the page recommends staying in it unless you need the features of the others.
- `disallow`: you can mark monitors as disallowed; they join the quorum and serve clients but cannot be elected leader.
- `connectivity`: monitors score each other's connectivity and elect the best connected, which suits stretch or network-split risk.

Disallow mode:

```
ceph mon add disallowed_leader {name}
ceph mon rm disallowed_leader {name}
ceph mon dump
```

`ceph mon dump` lists the disallowed leaders. The page suggests this for monitors far away from clients.

Connectivity scores:

```
ceph daemon mon.{name} connection scores dump
ceph daemon mon.{name} connection scores reset
```

Mode values are `1` for classic, `2` for disallow and `3` for connectivity. For a new cluster, set `mon_election_default_strategy` to one of those integers before the first monitor map is created. The docs recommend staying in `classic` unless you have a very specific reason, and stretch mode requires `connectivity`. Disallowed monitors participate in the quorum and serve clients but are never elected leader, and connectivity mode supports the same `disallowed_leader` commands; `ceph mon dump` lists them. Connection scores range from 0 to 1 and are maintained even outside connectivity mode, so you can inspect them any time. Resetting them is low risk but not recommended unless support or a developer asks.

## Checked

2026-11-03. Confirmed against: the Ceph Configuring Monitor Election Strategies page (docs.ceph.com/en/latest/rados/operations/change-mon-elections/).

Removed: the 'lowest-ranked live monitor wins' description of classic and the tiebreaker use case (not on the page).

Method: documentation only; no commands were run.
