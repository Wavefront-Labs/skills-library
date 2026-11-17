---
id: computing-software.systems-network-administration.incus.incus-admin-group-and-subuid
name: incus-admin-group-and-subuid
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, incus-admin, group, subuid, subgid, access, unprivileged-containers]
level: intro
status: docs-checked
description: "Give a user daemon access through the incus-admin group and set root subuid/subgid ranges so unprivileged containers can start."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/installing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Admin group and subuid/subgid

Access control:
- Root and members of the `incus-admin` group can control the daemon.
- If the group does not exist, create it and restart the daemon.
- Group membership normally applies at next login. Re-open the session or run `newgrp incus-admin`.
- Gentoo also creates an `incus` group that grants basic (non-admin) user access.

Unprivileged containers need ID ranges for root:

```
echo "root:1000000:1000000000" | sudo tee -a /etc/subuid /etc/subgid
```

- If `newuidmap` and `newgidmap` are installed, root needs a contiguous range of at least 10 million UIDs and GIDs.
- On Gentoo, set `/etc/subuid` and `/etc/subgid` before starting the daemon.

## Checked

2026-11-09. Confirmed against the Incus doc installing.md (Gentoo tab, Machine setup, Manage access to Incus): the incus-admin group, newgrp, the subuid/subgid line and the 10M range note. Removed: the closing line about running incus admin init, which this page does not state at that point.

Method: documentation only; no commands were run.
