---
id: computing-software.cloud-infrastructure-engineering.external-dns.internal-hostname-and-node-addresses
name: internal-hostname-and-node-addresses
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, internal-hostname, access-annotation, endpoints-type, nodeport, headless-service]
level: advanced
status: docs-checked
description: "Pick which IPs ExternalDNS publishes: internal-hostname for ClusterIP and PodIP, the access annotation for NodePort, and endpoints-type for headless Services."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Internal hostnames and address selection

**`internal-hostname`:** a domain for internal networks. On a `LoadBalancer` Service it resolves to the `ClusterIP`; on a Pod, to `Status.PodIP`. It differs from `hostname` only for `ClusterIP` or `LoadBalancer` Services.

```yaml
metadata:
  annotations:
    external-dns.kubernetes.io/internal-hostname: my-service.internal.example.com
```

**`access`** (Service source only, NodePort Services):
- `public`: Nodes' `ExternalIP` addresses plus IPv6 `InternalIP`.
- `private`: Nodes' `InternalIP`.
- Absent: behaves as `public` if any `ExternalIP` exists, otherwise `private`.
Every other source ignores it, including Ingress.

**`endpoints-type`** (headless Services):
- `NodeExternalIP`: each Pod's Node `ExternalIP` plus IPv6 `InternalIP`. Requires `--service-type-filter=ClusterIP` and `--service-type-filter=Node`, or no filter flag.
- `HostIP`: each Pod's `Status.HostIP`. `--publish-host-ip` has the same effect.
- Otherwise: the IP of each Endpoints address.

## Checked

2026-11-04. Confirmed against the ExternalDNS annotations page (internal-hostname, access and endpoints-type sections, support table footnote 2). Removed an unsourced gotcha and a verification line.
Method: documentation only; no commands were run.
