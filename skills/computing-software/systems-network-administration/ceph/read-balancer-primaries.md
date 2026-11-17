---
id: computing-software.systems-network-administration.ceph.read-balancer-primaries
name: read-balancer-primaries
category: computing-software
field: systems-network-administration
product: ceph
tags: [ceph, read-balancer, pg-upmap-primary, primary, osdmaptool]
level: sme
status: docs-checked
description: "Even out primary OSD assignments with the Ceph read balancer, online via the balancer module or offline with osdmaptool --read."
sources:
  - https://docs.ceph.com/en/latest/rados/operations/read-balancer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The read (primary) balancer spreads primary roles across OSDs so read load is even. It uses `pg-upmap-primary` entries.

Online:

```
ceph balancer on
ceph balancer mode <read|upmap-read>
ceph osd set-require-min-compat-client reef
ceph features
```

`read` optimises primaries only; `upmap-read` combines it with the upmap balancer. Before the minimum client is raised, `ceph features` must show that no older clients are connected. Never lower an already-higher value. If you prefer another balancer, run `ceph balancer off`.

Offline:

```
ceph osd getmap -o om
osdmaptool om --read out.txt --read-pool <pool name> [--vstart]
```

The output file lists the commands to run against the cluster.

Troubleshooting: a specific `pg-upmap-primary` mapping can be removed with the `ceph osd rm-pg-upmap-primary` command documented on the page. The `read_balance_score` shown by `ceph osd pool ls detail` helps judge a pool before and after.

Decide whether you need it first: `ceph osd pool ls detail` shows `read_balance_score` for each replicated pool, and a score above 1 (for example 1.5) means primaries are unbalanced. Online, run `ceph balancer on` then `ceph balancer mode <read|upmap-read>`; both modes use `pg-upmap-primary`, so the cluster must not have pre-Reef clients. On an existing cluster run `ceph osd set-require-min-compat-client reef`, which fails if older clients or daemons are connected; `ceph features` shows which versions are in use. To clean up, `ceph osd rm-pg-upmap-primary <pgid>` removes one mapping and `ceph osd rm-pg-upmap-primary-all {pool name}` removes all. The kernel client does not support `pg-upmap-primary`, so kernel RBD maps and CephFS mounts fail while such mappings exist.

## Checked

2026-11-03. Confirmed against: the Ceph Read (Primary) Balancer page (docs.ceph.com/en/latest/rados/operations/read-balancer/): read_balance_score, Online and Offline Optimization, Troubleshooting.

Removed: nothing.

Method: documentation only; no commands were run.
