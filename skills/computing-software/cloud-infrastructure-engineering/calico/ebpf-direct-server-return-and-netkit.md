---
id: computing-software.cloud-infrastructure-engineering.calico.ebpf-direct-server-return-and-netkit
name: ebpf-direct-server-return-and-netkit
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ebpf, dsr, netkit, bpfexternalservicemode, bpfattachtype, tcx, pod-interface, performance]
level: advanced
status: docs-checked
description: "Tune the eBPF data plane: direct server return via bpfExternalServiceMode, cloud source-dest check needs, and tech-preview netkit pod interfaces with bpfAttachType."
sources:
  - https://docs.tigera.io/calico/latest/operations/ebpf/enabling-ebpf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Direct server return.** DSR skips a hop for traffic to services (such as NodePorts) from outside the cluster, lowering latency and CPU. It needs the network to let nodes send traffic with each other's IPs: in AWS all nodes in one subnet with source/dest check disabled; in GCP, source/dest check disabled by enabling IP forwarding. It is off by default.

```
calicoctl patch felixconfiguration default --patch='{"spec": {"bpfExternalServiceMode": "DSR"}}'
```

Set it back to `"Tunnel"` to revert. Switching can disrupt in-progress connections.

**Netkit (tech preview).** The CNI plugin normally creates a veth pair per pod. On Linux 6.7 or later you can ask for netkit L2 pairs, recommended for eBPF (equivalent to veth for iptables and nftables). Older kernels silently fall back to veth, so mixed clusters are safe. Requires `spec.cni.type: Calico`.

```bash
kubectl patch installation.operator.tigera.io default --type merge -p '{"spec":{"calicoNetwork":{"linuxPodInterfaceType":"Netkit"}}}'
```

Existing pods keep veth; new or restarted pods get netkit. Reverting to `Veth` leaves existing netkit pods as they are.

**Attach type** (`bpfAttachType` in FelixConfiguration): `Netkit` (default; netkit on netkit interfaces, TCX elsewhere), `TCX` everywhere, or legacy `TC`, which does not support pod bandwidth QoS annotations. Changing it restarts Felix on every node.

**Before downgrading** to a release without netkit support, move off netkit attachment, because the old release cannot remove the programs:

```bash
kubectl patch felixconfiguration default --type merge -p '{"spec":{"bpfAttachType":"TCX"}}'
```

After upgrading again, remove the field with a JSON patch `remove` on `/spec/bpfAttachType`.

## Checked

2026-11-08. The Enabling the eBPF data plane page was read in full. DSR requirements and commands, netkit prerequisites, attach types and downgrade steps were confirmed on the Enabling the eBPF data plane page.

Method: documentation only; no commands were run.
