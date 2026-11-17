---
id: computing-software.systems-network-administration.glusterfs.quota-timeouts-alert
name: quota-timeouts-alert
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, quota, soft-timeout, hard-timeout, alert-time]
level: advanced
status: docs-checked
description: "Tune GlusterFS quota accuracy with features.soft-timeout and hard-timeout, alert-time logging, and quota-deem-statfs so df reflects directory limits."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Directory-Quota.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quota timeouts and alert time

Quota caches directory sizes on clients, so a stale cache can let writes pass the limit until the timeout expires.

```
gluster volume set <VOLNAME> features.soft-timeout <time>
gluster volume set <VOLNAME> features.hard-timeout <time>
```

- Soft timeout applies while usage is below the soft limit.
- Hard timeout applies while usage is between the soft and hard limits.
- A timeout of 0 forces a server fetch on every data-modifying operation and disables client-side caching.
- Example: `gluster volume set test-volume features.hard-timeout 5` prints `Set volume successful`.
- The page does not state default timeouts.

Alert time, how often usage is logged after the soft limit is reached (default one week):

```
gluster volume quota <VOLNAME> alert-time <time>
```

Example: `gluster volume quota test-volume alert-time 1d` prints `volume quota : success`.

`df` behaviour:

```
gluster volume set <VOLNAME> quota-deem-statfs on
```

On (the default once quota is enabled): `df` on a limited directory reports its hard limit as total size. Off: it shows the full volume size.

## Checked

2026-11-04. Confirmed against the glusterdocs Directory Quota page: client-side size caching, soft-timeout and hard-timeout meaning and examples, zero timeout behaviour, alert-time with its one week default and example, and quota-deem-statfs default on with the df behaviour. Nothing removed.

Method: documentation only; no commands were run.
