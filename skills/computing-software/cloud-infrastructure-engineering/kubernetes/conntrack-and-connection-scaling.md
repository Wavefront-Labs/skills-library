---
id: computing-software.cloud-infrastructure-engineering.kubernetes.conntrack-and-connection-scaling
name: conntrack-and-connection-scaling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, conntrack, nf_conntrack, snat, port-exhaustion, nat, cloud-nat, scaling, sysctl, networking, node-level]
level: advanced
status: docs-checked
description: "Diagnose and size the kernel conntrack table and SNAT port budget that Service/NAT paths in Kubernetes share: the node-level ceiling that outlives any CNI or proxy-mode change."
sources: ["https://docs.kernel.org/networking/nf_conntrack-sysctl.html", "https://docs.kernel.org/networking/ip-sysctl.html", "https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-troubleshooting.html", "https://docs.aws.amazon.com/vpc/latest/userguide/metrics-dimensions-nat-gateway.html", "https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/", "https://docs.cilium.io/en/stable/cmdref/cilium-agent/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conntrack and SNAT port exhaustion: the ceiling under every Service/NAT path

**Goal:** recognize when "random dropped connections under load" is actually a kernel
conntrack table or SNAT port-budget limit, not a proxy-mode, CNI, or app bug. This ceiling
exists regardless of which CNI, kube-proxy mode, or cloud LB is in front of it.

## 1. What conntrack tracks, and why it fills up
- `nf_conntrack` records connection state, including NAT mappings, so return traffic can be
  un-NAT'd correctly. Service ClusterIP/NodePort DNAT, egress SNAT and LoadBalancer paths
  through a node all create entries. Short-lived, high-churn connections (clients that open a
  connection per request, aggressive health-checkers, HTTP/1.1 without keep-alive) fill the
  table far faster than long-lived connections at the same throughput.
- Symptom: the kernel logs `nf_conntrack: table full, dropping packet` (check `dmesg`); new
  connections fail intermittently while existing ones are unaffected. That asymmetry (new
  fails, existing fine) is the tell that separates it from a routing or policy problem,
  which usually affects all traffic to a destination.
- Sizing knobs from the kernel docs: `net.netfilter.nf_conntrack_max` is the maximum number
  of tracked entries and, by default, equals `nf_conntrack_buckets`; the hash table size
  `nf_conntrack_buckets` defaults to total memory divided by 16384, never fewer than
  1024 and never more than 262144. Entries are added twice (original and reply direction),
  so a full default table has an average hash chain length of 2. `nf_conntrack_count`
  (read-only) is the current number of entries.

## 2. SNAT port exhaustion: a related but distinct ceiling
- Any path that SNATs many pods' outbound traffic to one IP (a cloud NAT gateway, a CNI
  egress gateway, `externalTrafficPolicy: Cluster` routing through a node) shares that IP's
  source-port space. On Linux the default ephemeral port range
  (`net.ipv4.ip_local_port_range`) is 32768-60999. High-fanout egress can exhaust the port
  budget **even when the conntrack table is fine**: it is a different resource.
- Cloud NAT gateways have their own limits and metrics. AWS documents up to 55,000
  concurrent connections per IP address on a NAT gateway (add IP addresses or more NAT
  gateways when you hit it), and its CloudWatch metric `ErrorPortAllocation` counts
  failures to allocate a source port: a value above zero indicates too many concurrent
  connections. Check the cloud provider's NAT dashboard, not just node-level `dmesg`, when
  the SNAT path is a managed resource.

## 3. Sizing and mitigation
- Raise `net.netfilter.nf_conntrack_max` and the bucket count together (a DaemonSet-applied
  sysctl, `/etc/sysctl.d/`, or node-image config), sized to realistic peak concurrent
  connections per node and the memory you can spend.
- Reduce short-lived-connection churn: HTTP keep-alive and connection pooling in clients
  (gRPC reuses connections by design), and `externalTrafficPolicy: Local` instead of
  `Cluster` where the trade-offs in
  `computing-software.cloud-infrastructure-engineering.kubernetes.k8s-networking-and-ingress`
  allow it: Kubernetes documents that with `Local` kube-proxy only sends to local endpoints
  and does not SNAT the client address to another node.
- NodeLocal DNSCache skips iptables DNAT and connection tracking for DNS, which the
  Kubernetes docs say reduces conntrack races and keeps UDP DNS entries from filling the
  conntrack table.
- For SNAT port exhaustion specifically: spread egress across more NAT IPs (multiple cloud
  NAT gateway IPs, multiple CNI egress-gateway nodes; see
  `computing-software.cloud-infrastructure-engineering.kubernetes.egress-gateway-and-static-egress-ip`)
  rather than only raising the conntrack table, since the port space per IP is not governed
  by `nf_conntrack_max`.
- Cilium keeps its own BPF connection-tracking maps. In v1.20 the agent options
  `--bpf-ct-global-tcp-max` (default 524288) and `--bpf-ct-global-any-max` (default 262144)
  size them, and Hubble reports a full map as the drop reason `CT: Map insertion failed`.
  Switching dataplane moves where the limit is configured; it does not remove the limit.

## Debug routine
```bash
# Is the table actually full?
dmesg | grep -i "nf_conntrack: table full"
cat /proc/sys/net/netfilter/nf_conntrack_count /proc/sys/net/netfilter/nf_conntrack_max
# Live breakdown by protocol (conntrack-tools)
conntrack -L | awk '{print $1}' | sort | uniq -c | sort -rn | head
# Raise it (immediate; also persist via sysctl.d or a privileged DaemonSet init container)
sysctl -w net.netfilter.nf_conntrack_max=1048576
```

## Verify
- [ ] `nf_conntrack_count` vs `nf_conntrack_max` is graphed per node, with alerting below
  the ceiling (not discovered via `dmesg` during an incident).
- [ ] A load test that mimics real connection churn (not just throughput) is used to find the
  actual per-node ceiling before production traffic does.
- [ ] SNAT port exhaustion is checked as a separate failure mode from conntrack table
  fullness: both produce "random connection failures under load" but have different fixes.
- [ ] After raising `nf_conntrack_max`, the change is confirmed persistent across node
  reboot/replacement (a runtime-only sysctl reverts on the next node cycle).

## Checked
2026-10-27. Documentation releases: Linux kernel `nf_conntrack-sysctl` and `ip-sysctl` docs (mainline), AWS NAT gateway troubleshooting and metrics pages (current), Kubernetes website main (v1.38 dev tree; latest release v1.37.1), Cilium v1.20.4 agent reference and drop table, kernel source for the "table full" message.
Confirmed: conntrack sysctl semantics and defaults, kernel log text, default ephemeral port range, AWS 55,000-connection guidance and `ErrorPortAllocation`, NodeLocal DNSCache rationale, `externalTrafficPolicy: Local` behaviour, Cilium CT flag names and defaults.
Method: documentation only; no commands were run.
