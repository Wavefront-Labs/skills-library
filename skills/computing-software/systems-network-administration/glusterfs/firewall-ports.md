---
id: computing-software.systems-network-administration.glusterfs.firewall-ports
name: firewall-ports
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, firewall, ports, 49152, iptables]
level: practitioner
status: docs-checked
description: "Which ports a GlusterFS server must open: 24007-24008 TCP/UDP, one port per brick from 49152, the Gluster 10 randomised range, and iptables rule ordering."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Setting-Up-Clients.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Troubleshooting/troubleshooting-gnfs.md
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Storage-Pools.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall ports for servers

For the native client:

- TCP and UDP 24007 and 24008.
- One port per brick starting at 49152. Five bricks need 49152 to 49156.
- From Gluster 10 onward, brick ports are randomised within the `base_port` to `max_port` range in `glusterd.vol`. Lower `max_port` and restart glusterd to reduce the number of open ports.

Example rules:

```
iptables -A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 24007:24008 -j ACCEPT
iptables -A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 49152:49156 -j ACCEPT
```

If chains already exist, the ACCEPT rules must come before any DROP rule (use a lower rule number).

Peer probing also needs port 24007 (see peer-probe-server).

Gluster NFS: open port 111 (portmap) and 38465, 38466 and 38467. A blocked firewall shows up as `showmount` failing with "clnt_create: RPC: Unable to receive".

## Checked

2026-11-04: ports 24007 and 24008, per-brick ports from 49152, the Gluster 10 randomised range, the iptables examples and rule-order note, and the Gluster NFS ports 111, 38465, 38466 and 38467 were read against the glusterdocs pages Setting-Up-Clients and troubleshooting-gnfs; port 24007 for peer probing is on Storage-Pools. Nothing removed.

Method: documentation only; no commands were run.
