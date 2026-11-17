---
id: computing-software.systems-network-administration.incus.cluster-remove-upgrade-certificate
name: cluster-remove-upgrade-certificate
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, cluster, remove, force, upgrade, blocked, cluster-certificate, update-certificate]
level: advanced
status: docs-checked
description: "Remove Incus cluster members (cleanly or --force), upgrade members without blocking the cluster, and replace the cluster certificate."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/cluster_manage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Remove, upgrade, certificate

Removal:
- `incus cluster remove <member>`: member must be online and hold no instances.
- `incus cluster remove --force <member>` from an online member for a permanently offline one. Do it promptly; offline members hurt upgrades. The member's database is left inconsistent, so reinstall that server fully.

Upgrade:
- Bring every member to the same version; never upgrade while a member is offline.
- Upgrade the package and restart the daemon. Members may go "blocked" after schema or API changes: they stop serving API requests but instances keep running. See them with `incus cluster list` on an unblocked member. They recover after the last member upgrades.

Certificate: all members share `/var/lib/incus/cluster.crt` (self-signed, ten-year expiry). Replace it, for example with an ACME certificate, using `incus cluster update-certificate`, which applies to all members.

## Checked

2026-11-09. Confirmed against the Incus doc howto/cluster_manage.md (Delete cluster members, Upgrade cluster members, Update the cluster certificate): removal rules, force-remove consequences, blocked state, certificate path and ten-year expiry, update-certificate. Removed: nothing needed removing.

Method: documentation only; no commands were run.
