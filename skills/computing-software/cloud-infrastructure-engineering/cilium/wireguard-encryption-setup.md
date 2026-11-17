---
id: computing-software.cloud-infrastructure-engineering.cilium.wireguard-encryption-setup
name: wireguard-encryption-setup
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, wireguard, transparent-encryption, cilium-wg0, encryption-type, udp-51871]
level: practitioner
status: docs-checked
description: "Enable Cilium WireGuard transparent encryption with Helm or CLI, open UDP 51871, validate with cilium-dbg status and tcpdump on cilium_wg0."
sources:
  - https://docs.cilium.io/en/stable/security/network/encryption-wireguard/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WireGuard transparent encryption

Each agent creates its own key pair and publishes the public key in the `network.cilium.io/wg-pub-key` annotation of its `CiliumNode`. Agents form tunnels to all other known nodes. Traffic to the same node is not encrypted (intended). In tunnel routing mode, pod traffic is encapsulated twice (VXLAN/Geneve, then WireGuard).

## Enable
Kernel needs WireGuard (`CONFIG_WIREGUARD=m` on Linux 5.6+, or the out-of-tree module). Helm/CLI options:
```
cilium install --version <v> --set encryption.enabled=true --set encryption.type=wireguard
```
Or set `enable-wireguard: true` in the Cilium ConfigMap and restart agents. With CNI chaining (for example AWS CNI) set `cni.enableRouteMTUForCNIChaining=true` or encrypted pod traffic may fragment.

## Ports
The tunnel endpoint is UDP `51871` on each node; nodes must reach each other on it (also across clusters in ClusterMesh).

## Validate
In a Cilium pod (`kubectl -n kube-system exec -ti ds/cilium -- bash`): `cilium-dbg status | grep Encryption` shows `Wireguard [cilium_wg0 (Pubkey: ..., Port: 51871, Peers: N)]` where Peers = nodes minus one. Install tcpdump and run `tcpdump -n -i cilium_wg0` to see pod traffic on the tunnel device.

## Known issue
Packets may be dropped when endpoints are added or removed or nodes update, which can cause failed `sendmsg` and `sendto` calls (GitHub issue 33159).

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the WireGuard encryption page: https://docs.cilium.io/en/stable/security/network/encryption-wireguard/. Confirmed the statements above. Nothing was removed.

Method: documentation only; no commands were run.
