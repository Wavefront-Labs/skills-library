---
id: computing-software.cloud-infrastructure-engineering.kubernetes.coredns-corefile-tuning-and-nodelocaldns
name: coredns-corefile-tuning-and-nodelocaldns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, coredns, dns, corefile, nodelocaldns, nodelocal-dnscache, stub-domain, cache-plugin, autoscaling, cluster-dns, udp-conntrack]
level: advanced
status: docs-checked
description: "Tune CoreDNS's Corefile (cache, forward, stub domains) and deploy NodeLocal DNSCache to fix the UDP conntrack races and latency spikes that plain cluster DNS hits at scale."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/dns-custom-nameservers/", "https://kubernetes.io/docs/tasks/administer-cluster/nodelocaldns/", "https://kubernetes.io/docs/tasks/administer-cluster/dns-horizontal-autoscaling/", "https://coredns.io/plugins/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoreDNS tuning and NodeLocal DNSCache — fixing cluster DNS at scale

**Goal:** go beyond "DNS works" to "DNS is fast and doesn't fall over at scale" — tune the
Corefile deliberately and know when to add NodeLocal DNSCache.

**Relation to existing coverage:** this assumes the basics (ndots, CoreDNS exists) covered in
`computing-software.cloud-infrastructure-engineering.kubernetes.k8s-networking-and-ingress`;
this skill goes into the Corefile internals and the NodeLocal DNSCache architecture.

## 1. The default Corefile and what each plugin does
```
.:53 {
    errors
    health { lameduck 5s }
    ready
    kubernetes cluster.local in-addr.arpa ip6.arpa {
        pods insecure
        fallthrough in-addr.arpa ip6.arpa
        ttl 30
    }
    prometheus :9153
    forward . /etc/resolv.conf
    cache 30
    loop
    reload
    loadbalance
}
```
- `kubernetes` plugin: serves cluster-local records from the Kubernetes API. Its own `ttl`
  option defaults to 5 seconds (the Kubernetes default Corefile sets `ttl 30`).
- `cache 30`: the TTL is a maximum; it never extends a record's own TTL. Without an argument the
  maximum is 3600s for NOERROR and 1800s for denial of existence. Minimum cache time defaults to 5s
  (`MINTTL` in the `success` / `denial` blocks).
- `forward . /etc/resolv.conf`: upstream resolution for anything outside cluster zones, using the
  node's resolv.conf. The optional `max_concurrent MAX` caps concurrent queries; new queries above it
  get a REFUSED response (not counted as a health failure) and increment
  `coredns_forward_max_concurrent_rejects_total`. The docs suggest MAX above upstream query rate times latency.
- `loop`: detects simple forwarding loops and halts the server; in Kubernetes the CoreDNS pod
  then goes into CrashLoopBackOff. Check for `forward`s to the zone itself, including via the
  node's resolv.conf.

## 2. Stub domains for split DNS
To route an internal zone (e.g. `corp.internal`) to a different resolver without touching app
code:
```
corp.internal:53 {
    forward . 10.10.0.2 10.10.0.3
}
```
Add this as its own server block in the ConfigMap. Common for hybrid-cloud clusters that need
to resolve on-prem AD/internal zones alongside cluster DNS.

## 3. Scaling CoreDNS itself
- CoreDNS scales horizontally. The Kubernetes DNS horizontal autoscaling task uses the
  cluster-proportional-autoscaler with `replicas = max(ceil(cores / coresPerReplica), ceil(nodes / nodesPerReplica))`.
- Watch `coredns_dns_responses_total{rcode}` and `coredns_dns_request_duration_seconds`
  (served by the `prometheus` plugin on `:9153` in the default Corefile).

## 4. NodeLocal DNSCache — when and why
- Runs a CoreDNS-based DaemonSet pod on **every node**, listening on a link-local IP
  that pods are pointed at instead of the cluster DNS Service IP. The docs say to pick any address
  that cannot collide in your cluster, for example from 169.254.0.0/16 (IPv4) or fd00::/8 (IPv6).
- The documented motivations: pods with high DNS QPS may otherwise reach a CoreDNS on another
  node; skipping iptables DNAT and connection tracking reduces conntrack races and stops UDP DNS
  entries filling the conntrack table; local-to-CoreDNS connections can be upgraded to TCP, which
  cuts tail latency from dropped UDP packets; node-level metrics; and negative caching can be
  re-enabled.
- Deployment: the `nodelocaldns.yaml` manifest with `__PILLAR__` placeholders substituted by sed.
  With kube-proxy in iptables mode the kubelet `--cluster-dns` value does not need to change; with
  kube-proxy in IPVS mode it must be set to the local listen address.
- The cache forwards cache misses for cluster hostnames (`cluster.local` by default) to the CoreDNS Service.

## Debug routine
```bash
kubectl -n kube-system logs -l k8s-app=kube-dns --tail=100
kubectl -n kube-system get cm coredns -o yaml   # the live Corefile
kubectl -n kube-system get pods -l k8s-app=node-local-dns -o wide
kubectl exec -it <any-pod> -- cat /etc/resolv.conf   # confirm it points where expected
```

## Verify
- [ ] `coredns_dns_request_duration_seconds` p99 is tracked and alerted on, not just uptime.
- [ ] If NodeLocal DNSCache is deployed, every pod's `/etc/resolv.conf` actually points at the
  link-local IP (a bad kubelet config can leave some nodes on the old path silently).
- [ ] A load test of concurrent DNS lookups from one node shows no UDP timeouts or retries.
- [ ] Stub domain forwarding resolves the internal zone from inside a pod, not just from a
  node.

## Checked

2026-10-26, against CoreDNS plugin READMEs (coredns/coredns main, latest commit 2026-10-25) and Kubernetes website docs (dns-custom-nameservers, nodelocaldns, dns-horizontal-autoscaling). Confirmed: default Corefile contents, `cache` maximum and MINTTL semantics, `forward max_concurrent` behaviour (REFUSED, not SERVFAIL), `kubernetes` plugin `ttl` default, `loop` behaviour, NodeLocal DNSCache motivations and kube-proxy mode differences, autoscaler formula. Wrong: `coredns_dns_response_rcode_count_total` (current name is `coredns_dns_responses_total`), `max_concurrent` causing SERVFAIL, `max_concurrent 1000` in the default Corefile, NodeLocal default IP 169.254.20.10 (the docs give no default). Removed the unconfirmed interception-mode blackhole claim and the dig loop.

Method: documentation only; no commands were run.
