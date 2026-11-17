---
id: computing-software.cloud-infrastructure-engineering.kubernetes.kube-proxy-service-datapath-troubleshooting
name: kube-proxy-service-datapath-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, kube-proxy, kube-proxy-troubleshooting, stale-iptables, service-datapath, iptables, ipvs, conntrack, iptables-save, ipvsadm, conntrack-cli]
level: advanced
status: docs-checked
description: "Trace a Service VIP to its pods through kube-proxy rules (iptables, IPVS, nftables), find stale or missing rules, and fix unreachable Services that have healthy endpoints."
sources: ["https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/", "https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/", "https://kubernetes.io/docs/reference/networking/virtual-ips/", "https://kubernetes.io/docs/reference/command-line-tools-reference/kube-proxy/", "https://github.com/kubernetes/kubernetes/blob/master/pkg/proxy/ipvs/proxier.go"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# kube-proxy and the Service datapath

Use when: `curl <pod-ip>:<port>` works but `curl <cluster-ip>:<port>` (or NodePort) doesn't.

## 1. Confirm the inputs kube-proxy sees
```bash
kubectl get svc web -o wide                       # ClusterIP, ports, selector
kubectl get endpointslices -l kubernetes.io/service-name=web -o wide   # ready endpoints & ports
```
No ready endpoints → not a kube-proxy problem (selector/readiness).

## 2. Is kube-proxy healthy on that node?
```bash
kubectl -n kube-system get pods -l k8s-app=kube-proxy -o wide | grep <node>
kubectl -n kube-system logs <kube-proxy-pod> | tail -50     # sync errors; "Using <mode> Proxier" line
curl -s http://<node-ip>:10256/healthz                       # lastUpdated recent, nodeEligible true; 503 = overdue sync or ineligible node
kubectl -n kube-system get cm kube-proxy -o yaml            # data.config.conf: mode, clusterCIDR
```
If a CNI replaces kube-proxy there are no kube-proxy rules; use that CNI's own tooling.

## 3. Inspect rules on the node (`kubectl debug node/<n> -it --image=<image with iptables/nft tools>`; the node's root filesystem is at `/host`)
**iptables mode**
```bash
iptables-save -t nat | grep KUBE-SERVICES    # per-Service jump to a KUBE-SVC-* chain
iptables-save -t nat | grep KUBE-SVC-XXXX    # one KUBE-SEP-* chain per endpoint
iptables-save -t nat | grep KUBE-SEP-YYYY    # DNAT to <pod-ip>:<port>
```
**IPVS mode** (deprecated): Service IPs are bound to a dummy interface named `kube-ipvs0`; `ipvsadm -Ln` lists the virtual servers.
**nftables mode**: `nft list table ip kube-proxy` and `nft list map ip kube-proxy service-ips`.

## 4. Common causes
| Finding | Cause |
|---|---|
| no rules for the Service, logs show sync errors | read the kube-proxy errors for the failing step; `healthz` shows an overdue sync |
| rules point to old pod IPs (stale) | kube-proxy is not receiving updates; check its logs and API access, restart the pod |
| works from other nodes, not this one | that node's kube-proxy is unhealthy or on a different mode/config |
| NodePort works on some nodes only | `externalTrafficPolicy: Local` (only nodes with endpoints answer), by design; or `nodePortAddresses` excludes that address (nftables default is `primary`) |
| NodePort fails on `127.0.0.1` in nftables mode | loopback NodePorts are not served by default there; see the nftables skill |

On start kube-proxy removes stale rules left by another mode; `kube-proxy --cleanup` removes rules and exits.

## Verify
- [ ] From a pod on each node, `curl <cluster-ip>:<port>` succeeds; `kubeproxy_sync_proxy_rules_last_timestamp_seconds` fresh on all kube-proxies.

## Checked

2026-10-26: kubernetes.io debug-a-running-pod page (kubectl debug node, /host), virtual-ips, kube-proxy reference and generated metrics reference (v1.37 docs, kubernetes/website main 2026-10-25) plus kube-proxy iptables, ipvs, nftables and healthcheck source (kubernetes/kubernetes main). Confirmed: chain prefixes KUBE-SERVICES, KUBE-SVC- and KUBE-SEP-, the kube-ipvs0 dummy device, nft table and map names, healthz fields and 503 cases, nodePortAddresses defaults, --cleanup behaviour. Removed unconfirmed causes (legacy versus nft backend, conntrack tool, hairpin mode), third-party debug image and eBPF CLI commands.

Method: documentation only; no commands were run.
