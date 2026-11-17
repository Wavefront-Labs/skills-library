---
id: computing-software.systems-network-administration.incus.cluster-evacuate-healing
name: cluster-evacuate-healing
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, cluster, evacuate, restore, healing, rebalance, maintenance]
level: advanced
status: docs-checked
description: "Evacuate and restore Incus cluster members, enable automatic healing (cluster.healing_threshold) and its risks, and tune re-balancing."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/cluster_manage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evacuation, healing and re-balancing

```
incus cluster evacuate <member>
incus cluster restore <member>
```

- Evacuation moves all instances off a member (maintenance, reboots). The member cannot create new instances meanwhile. `cluster.evacuate` on an instance sets how it moves; shutdown respects `boot.host_shutdown_timeout`.

Healing: a non-zero `cluster.healing_threshold` auto-evacuates after the leader marks a member offline. Offline means failing both heartbeat and ICMP checks. Recovered members must be restored manually. It applies only to instances on shared storage with no local devices.
- Risk: partial connectivity can corrupt data if a live server is marked offline. Mitigate by watching the `cluster-member-offline` event, cutting power via BMC or PDU, and setting `cluster.healing_delay` long enough.

Re-balancing uses `cluster.rebalance.batch`, `.cooldown`, `.interval` and `.threshold`. Past the threshold, Incus live-migrates suitable VMs to the least-loaded server.

## Checked

2026-11-09. Confirmed against the Incus doc howto/cluster_manage.md (Evacuate and restore, Cluster healing, Cluster re-balancing): evacuate and restore behaviour, healing threshold, offline definition, shared-storage limit, data-corruption warning and mitigations, rebalance option names. Removed: nothing needed removing.

Method: documentation only; no commands were run.
