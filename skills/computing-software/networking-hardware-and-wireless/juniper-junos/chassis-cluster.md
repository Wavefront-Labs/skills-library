---
id: computing-software.networking-hardware-and-wireless.juniper-junos.chassis-cluster
name: chassis-cluster
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, chassis-cluster, srx-ha, reth, redundancy-group]
level: practitioner
status: draft
description: "Form an SRX chassis cluster with control/fabric links, redundancy groups, reth interfaces and monitoring."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SRX chassis cluster
Goal: run two SRX as one HA pair.

```
user@node0> set chassis cluster cluster-id 1 node 0 reboot
user@node1> set chassis cluster cluster-id 1 node 1 reboot
```

```
set groups node0 system host-name srx-a
set groups node1 system host-name srx-b
set apply-groups "${node}"
set chassis cluster reth-count 2
set chassis cluster redundancy-group 0 node 0 priority 200
set chassis cluster redundancy-group 0 node 1 priority 100
set chassis cluster redundancy-group 1 node 0 priority 200
set chassis cluster redundancy-group 1 node 1 priority 100
set interfaces ge-0/0/5 gigether-options redundant-parent reth0
set interfaces reth0 redundant-ether-options redundancy-group 1
set interfaces fab0 fabric-options member-interfaces ge-0/0/2
```

- RG0 is the control plane; RG1+ carry data plane reth interfaces.
- Control link ports are fixed per model; fabric link carries session sync.

Gotcha: node-specific config belongs in groups; plain config is shared. Do not `commit` while a node is secondary-hold.

## Verify
- `show chassis cluster status` shows primary/secondary for each RG and `show chassis cluster interfaces` is up.
