---
id: computing-software.cloud-infrastructure-engineering.external-dns.pod-source-and-ptr
name: pod-source-and-ptr
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, pod-source, pod-source-domain, ignore-non-host-network-pods, rfc2136-reverse-zone]
level: advanced
status: docs-checked
description: "Register Pods in DNS with the pod source: host-network handling, --pod-source-domain naming, and the on-premises forward plus PTR combination with RFC2136."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/pod.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/ptr-records.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/multiple-namespaces.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pod source

The pod source creates DNS entries from `Pod` resources.

- By default it also considers Pods that do not use host networking. `--ignore-non-host-network-pods` ignores them.
- By default it reads the FQDN from Pod annotations. `--pod-source-domain=example.org` builds names instead: a Pod `test-pod` becomes `test-pod.example.org`.
- The Pod source supports `hostname` and `internal-hostname` annotations and `target`; it does not read `ttl` (see the annotation matrix).

**Use case:** on-premises clusters without SNAT on the pod network, where you want to register every Pod with a PTR so the source of outside traffic can be matched to a workload with `nslookup` or `dig` on the pod IP. Useful when running many clusters.

Options used together in the docs:
```sh
--source=pod
--domain-filter=example.org
--domain-filter=10.0.0.in-addr.arpa
--pod-source-domain=example.org
--create-ptr
--rfc2136-zone=example.org
--rfc2136-zone=10.0.0.in-addr.arpa
```

**Notes**
- The reverse zone needs to be in `--domain-filter` and, for RFC2136, in `--rfc2136-zone`.
- Per the PTR page, `--managed-record-types` must include PTR.
- Pod source in multi-namespace mode needs a `ClusterRoleBinding` for nodes.

## Checked

2026-11-04. Confirmed against the ExternalDNS Pod Source page (host networking, pod-source-domain, the on-premises option list), the annotations support table (hostname, internal-hostname, target; no ttl), the PTR page (managed-record-types) and the multiple-namespaces page (nodes ClusterRoleBinding). Removed an unsourced memory-cost sentence.
Method: documentation only; no commands were run.
