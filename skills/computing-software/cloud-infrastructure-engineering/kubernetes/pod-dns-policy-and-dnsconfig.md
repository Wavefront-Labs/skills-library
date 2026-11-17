---
id: computing-software.cloud-infrastructure-engineering.kubernetes.pod-dns-policy-and-dnsconfig
name: pod-dns-policy-and-dnsconfig
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, dns, dnspolicy, dnsconfig, clusterfirstwithhostnet, ndots, hostaliases, ckad]
level: practitioner
status: docs-checked
description: "Set pod DNS behaviour: dnsPolicy (ClusterFirst, ClusterFirstWithHostNet, Default, None), dnsConfig nameservers/searches/options like ndots, and hostAliases for static entries."
sources: ["https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy", "https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-dns-config", "https://kubernetes.io/docs/tasks/network/customize-hosts-file-for-pods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pod dnsPolicy and dnsConfig

## dnsPolicy
| Policy | Behaviour | Use |
|---|---|---|
| `ClusterFirst` (default) | queries that do not match the cluster domain suffix are forwarded to the upstream nameserver inherited from the node | normal pods |
| `ClusterFirstWithHostNet` | cluster DNS for pods with `hostNetwork: true` | host-network pods that must resolve Services |
| `Default` | the pod inherits the name resolution configuration of the node it runs on | pods that must not depend on cluster DNS |
| `None` | ignore the cluster's DNS settings; everything comes from `dnsConfig` | fully custom |
Gotcha: a `hostNetwork: true` pod with `dnsPolicy: ClusterFirst` falls back to the `Default`
behaviour, so set `ClusterFirstWithHostNet`. `ClusterFirstWithHostNet` is not supported for Pods
on Windows nodes.

## dnsConfig
Optional with any policy; required when `dnsPolicy: None` (then at least one nameserver is
needed). The fields are merged into the policy's result, with duplicates removed.
```yaml
spec:
  dnsPolicy: ClusterFirst
  dnsConfig:
    options:
    - {name: ndots, value: "2"}
    - {name: edns0}
    searches: [my.dns.search.suffix]
    nameservers: [192.0.2.1]
```
- `nameservers`: at most 3 addresses.
- `searches`: at most 32 search domains; the total length of all search domains must not exceed
  2048 characters. Some older container runtimes have their own, lower limits.
- `options`: list of `name` (and optional `value`) objects.
The default resolv.conf of a ClusterFirst pod has `options ndots:5`, so a name with fewer than
5 dots is tried against the search list first. Lowering `ndots`, or using fully qualified names
with a trailing dot, reduces the extra lookups for external names; short in-cluster names still
need to resolve, so test the value you pick.

## hostAliases (static /etc/hosts entries)
```yaml
spec:
  hostAliases:
  - ip: "10.1.2.3"
    hostnames: [legacy.internal, legacy]
```
The kubelet manages the pod's hosts file; changes made any other way may be overwritten on pod
creation or restart. Prefer a DNS record or a selector-less Service where you can.

## Verify
```bash
kubectl exec <pod> -- cat /etc/resolv.conf
```
- [ ] hostNetwork pods resolve Services; resolv.conf shows the intended ndots, search and nameservers.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the DNS for Services and Pods page (policy descriptions, hostNetwork fallback, Windows limitation, dnsConfig merge rules, the 3 nameserver, 32 search domain and 2048 character limits, ndots:5 default) and the customize-hosts-file task (kubelet may overwrite other changes). Removed the glibc option comments, the timeout option, the claim that limits start at 1.28 and the getent test.

Method: documentation only; no commands were run.
