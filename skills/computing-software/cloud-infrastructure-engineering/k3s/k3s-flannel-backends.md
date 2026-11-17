---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-flannel-backends
name: k3s-flannel-backends
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, flannel-backend, wireguard-native, vxlan]
level: practitioner
status: docs-checked
description: "Select the Flannel backend (vxlan, host-gw, wireguard-native, none) and Flannel options in K3s."
sources:
  - https://docs.k3s.io/networking/basic-network-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Flannel is the default CNI. Its options are set only on server nodes and must be identical on all servers. Default backend: vxlan. For encryption use wireguard-native.

--flannel-backend values:

- vxlan: encapsulate packets in VXLAN; may need extra kernel modules on Raspberry Pi (Ubuntu on a Pi needs preparation).
- host-gw: IP routes to pod subnets via node IPs; needs direct layer 2 connectivity between all nodes.
- wireguard-native: WireGuard encapsulation and encryption. WireGuard kernel modules must be present on every node, servers and agents, before use (follow the WireGuard install guide).
- ipsec: strongSwan via swanctl; deprecated and removed in v1.27.0.
- none: disable Flannel entirely.

Other server flags: `--flannel-ipv6-masq` (masquerade IPv6 traffic; dual-stack or IPv6-only clusters; works with any backend except none) and `--flannel-external-ip` (use node external IPs for Flannel traffic; only applies when --node-external-ip is set).

Per-agent flags for that node's Flannel: `--flannel-iface`, `--flannel-conf`, `--flannel-cni-conf`.

Deprecated form: `--no-flannel` (use --flannel-backend=none).

Config file form:

```
flannel-backend: wireguard-native
```

Ports: UDP 8472 for VXLAN, UDP 51820 (and 51821 for IPv6) for WireGuard.

## Checked

2026-11-03: read docs.k3s.io networking/basic-network-options (ports from installation/requirements, per-agent flags from cli/agent). Confirmed: backend values and descriptions, the wireguard-native module requirement, ipsec deprecation (removal in v1.27.0), --flannel-ipv6-masq, --flannel-external-ip, per-agent flannel flags, --no-flannel, and ports 8472, 51820 and 51821. Removed: the claim that `--flannel-backend wireguard` is a deprecated form, which no fetched page states.

Method: documentation only; no commands were run.
