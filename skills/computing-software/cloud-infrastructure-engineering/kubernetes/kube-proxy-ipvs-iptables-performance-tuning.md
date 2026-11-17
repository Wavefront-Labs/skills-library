---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-proxy-ipvs-iptables-performance-tuning
name: kube-proxy-ipvs-iptables-performance-tuning
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-proxy, ipvs, iptables, performance, scaling, conntrack, service-proxy, sync-latency, large-clusters]
level: advanced
status: docs-checked
description: "Know how kube-proxy iptables mode scales, why nftables replaces the deprecated IPVS mode, and the sync-latency and conntrack knobs that matter before blaming the CNI."
sources: ["https://kubernetes.io/docs/reference/networking/virtual-ips/", "https://kubernetes.io/docs/reference/instrumentation/metrics/", "https://kubernetes.io/docs/reference/config-api/kube-proxy-config.v1alpha1/", "https://github.com/kubernetes/kubernetes/blob/master/cmd/kube-proxy/app/server_linux.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# kube-proxy: iptables, nftables and IPVS, and why Service count is a scaling axis

**Goal:** diagnose kube-proxy as the cause of Service-routing slowness before blaming the
CNI or the app, and know which proxy mode and knobs actually help.

## 1. How iptables mode scales
- iptables mode creates a few rules for every Service and a few for each endpoint IP. In clusters
  with tens of thousands of Pods and Services that means tens of thousands of rules, and kube-proxy
  may take a long time to update the kernel when Services or EndpointSlices change.
- Since v1.28 the iptables mode only updates the rules for Services or EndpointSlices that actually
  changed, instead of rewriting everything on each sync.
- First place to look: `kubeproxy_sync_proxy_rules_duration_seconds` (labels: `ip_family`) and
  `kubeproxy_sync_proxy_rules_last_timestamp_seconds`, before any packet-level debugging.

## 2. Knobs for iptables mode
```yaml
iptables:
  minSyncPeriod: 1s     # minimum time between rule resyncs (default 1s)
  syncPeriod: 30s
```
- `minSyncPeriod` batches changes: with `0s` deleting a 100-pod Deployment can cause 100 separate
  updates. The docs say the `1s` default suits most clusters; if the average sync time is much larger
  than 1 second in a very large cluster, raising it may help. If you raised it before v1.28, try removing
  the override.
- `syncPeriod` controls housekeeping such as noticing external interference with kube-proxy's rules.
  Very large values (for example `1h`) are no longer recommended.

## 3. nftables is the recommended replacement
- The `nftables` mode (kernel 5.13 or later; GA in 1.33) processes Service and endpoint changes faster
  than iptables and handles packets more efficiently, though the packet-path gain only becomes
  noticeable with tens of thousands of Services. See `kube-proxy-configuration-and-nftables-mode`.
- The `ipvs` mode is deprecated (since v1.35), is disabled by default from v1.40 (re-enable with the
  `KubeProxyIPVS` feature gate) and is removed in v1.43. The docs say the IPVS kernel API was a poor match
  for the Service API and never implemented all Service edge cases. kube-proxy logs an error and emits a
  Warning event `IPVSDeprecation` when it starts in this mode, and refuses to start if IPVS prerequisites are
  missing ("can't use the IPVS proxier"). Where nftables is not possible (old kernels), the docs suggest
  trying iptables rather than ipvs.
- IPVS schedulers (`rr`, `wrr`, `lc`, `wlc`, `lblc`, `lblcr`, `sh`, `dh`, `sed`, `nq`, `mh`) are set with
  `ipvs.scheduler` if you still run it.

## 4. eBPF alternatives
A CNI that replaces kube-proxy removes this component entirely; check that CNI's own documentation for its
scaling behaviour and Kubernetes version support before relying on it for this problem.

## 5. conntrack
Every mode relies on kernel connection tracking for NAT. kube-proxy's `conntrack` section controls it:
`maxPerCore` (maximum tracked NAT connections per CPU core, `0` leaves the kernel limit as-is and ignores
`min`), `min`, and timeouts such as `tcpEstablishedTimeout`, `tcpCloseWaitTimeout`, `udpTimeout`. A table limit
problem is a kernel-table problem, not a proxy-mode problem; see
`computing-software.cloud-infrastructure-engineering.kubernetes.conntrack-and-connection-scaling`.

## 6. When to act
- If sync durations are persistently much larger than the 1 second default, tune `minSyncPeriod` and plan a
  move to nftables mode.
- On a small cluster, proxy mode rarely matters; do not switch modes without a measured problem. Set
  `mode` explicitly either way, because the default will change from iptables to nftables in a future release.

## Debug routine
```bash
kubectl -n kube-system logs <kube-proxy-pod>            # "Using iptables Proxier" / nftables / ipvs
curl -s http://127.0.0.1:10249/proxyMode                 # run on the node
kubectl -n kube-system get cm kube-proxy -o yaml         # data.config.conf: mode
```

## Verify
- [ ] Active proxy mode confirmed from kube-proxy's own log line or `/proxyMode`, not just the configured flag.
- [ ] `kubeproxy_sync_proxy_rules_duration_seconds` is scraped and alertable.
- [ ] After a mode change, a Service create/update is timed end to end (apply to first successful connection).
- [ ] conntrack limits checked separately from proxy-mode choice.

## Checked

2026-10-26: kubernetes.io virtual-ips page and generated metrics reference (v1.37 docs, kubernetes/website main 2026-10-25), the kube-proxy config API source and server source (kubernetes/kubernetes main), and the KubeProxyIPVS feature-gate page. Rewritten: the old text recommended IPVS as the scaling fix and said a missing IPVS module silently falls back to iptables; the docs and source show IPVS is deprecated (1.35, disabled by default 1.40, removed 1.43), kube-proxy refuses to start without IPVS prerequisites, iptables mode has updated only changed rules since 1.28, and nftables is the recommended replacement. Removed unconfirmed per-packet linear-cost claims, thresholds and host command pipelines.

Method: documentation only; no commands were run.
