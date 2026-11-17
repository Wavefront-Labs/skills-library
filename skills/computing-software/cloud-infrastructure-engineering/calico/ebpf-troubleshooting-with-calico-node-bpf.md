---
id: computing-software.cloud-infrastructure-engineering.calico.ebpf-troubleshooting-with-calico-node-bpf
name: ebpf-troubleshooting-with-calico-node-bpf
category: computing-software
field: cloud-infrastructure-engineering
product: calico
tags: [ebpf, troubleshooting, calico-node, bpf-counters, conntrack, nat, policy-dump, bpfloglevel, tracelog]
level: advanced
status: docs-checked
description: "Debug the eBPF data plane with the calico-node -bpf tool: verify BPF is on, dump NAT and conntrack, read drop counters, dump attached policy, and enable filtered BPF debug logs."
sources:
  - https://docs.tigera.io/calico/latest/operations/ebpf/troubleshoot-ebpf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Run the embedded tool inside a calico-node pod (find one with `kubectl get pod -o wide -n calico-system`):

```bash
kubectl exec -n calico-system <calico-node-name> -- calico-node -bpf <args>
```

Use `calico-node -bpf help` (not `--help`) to list commands: `arp`, `cleanup`, `connect-time`, `conntrack`, `counters`, `ifstate`, `ipsets`, `nat`, `policy`, `profiling`, `routes`, `version`.

**Is BPF on?** The calico-node log shows `BPF enabled, starting BPF endpoint manager and map manager.` If unsupported it logs an ERROR `BPF data plane mode enabled but not supported by the kernel. Disabling BPF mode.`

**NodePort timeouts to a pod on another node.** The fabric must allow VXLAN (UDP 4789 by default) between nodes; this is separate from any pod overlay. In DSR mode the fabric must let one node reply for another (AWS source/dest check off, GCP allow forwarding); DSR does not work through a load balancer on the return path.

**Services.** `calico-node -bpf nat dump` shows each service IP, port, protocol and backends. `conntrack dump` shows tracked flows; TCP from inside the cluster uses connect-time load balancing by default, so the NAT is not visible in conntrack.

**Drops.** `calico-node -bpf counters dump --iface=eth0` breaks counts into Accepted, Dropped (by policy, failed decapsulation, unknown route, and more), Redirect and Total. A rising `Dropped by policy` means check your policy.

**Policy.** `calico-node -bpf policy dump <interface> <type> [--asm]`, with type `ingress`, `egress`, `xdp` or `all`. Pod ingress policy sits on the tc or tcx egress hook of the host side of the `caliXXXXXX` veth.

**Debug logs.** Set Felix `bpfLogLevel` to `Debug` (heavy performance cost) and narrow it with `bpfLogFilters` (pcap expressions applied to the original packet, before NAT, so filter service and backend addresses). Read with `bpftool prog tracelog` in the pod. Tags such as `ens192---E` mean interface plus ingress or egress; an `X` suffix is XDP.

## Checked

2026-11-08. The Troubleshoot eBPF mode page was read in full. Commands, log messages, counter categories and filter behaviour were confirmed on the Troubleshoot eBPF mode page.

Method: documentation only; no commands were run.
