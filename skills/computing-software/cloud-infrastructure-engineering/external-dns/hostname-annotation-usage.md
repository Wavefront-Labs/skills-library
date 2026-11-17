---
id: computing-software.cloud-infrastructure-engineering.external-dns.hostname-annotation-usage
name: hostname-annotation-usage
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, hostname-annotation, ignore-hostname-annotation, multi-hostname, domain-filter-match]
level: intro
status: docs-checked
description: "Use the external-dns.kubernetes.io/hostname annotation for Services, Ingresses and Pods: comma lists, overriding derived hosts, and the domain filter requirement."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The hostname annotation

`external-dns.kubernetes.io/hostname` specifies additional domains for a resource's DNS records.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
  annotations:
    external-dns.kubernetes.io/hostname: app.example.com
spec:
  type: LoadBalancer
```

ExternalDNS creates an A or CNAME record pointing at the Service's external IP or hostname.

- **Several names:** comma-separate them, for example `api.example.com,api.internal.example.com`. Two records result. Empty entries are ignored.
- **Ingress:** it adds to, or overrides alongside, names derived from `spec.rules[].host`. It also lets you manage DNS on an Ingress with no host in its rules.
- **Pods:** targets are the Pod's `Status.PodIP`; with `hostNetwork: true` the NodeExternalIP is used for IPv4 and NodeInternalIP for IPv6.
- Hostnames must match the domain filter set in ExternalDNS (for example `--domain-filter=example.com`).
- `--ignore-hostname-annotation` disables it for the sources marked in the support table (Contour, Gateway, Ingress, Istio, Kong, OpenShift, Service, Skipper, Traefik).
- The docs mark it alpha, subject to change.

The support table lists no hostname annotation for the Ambassador, F5, Gloo, Node, CRD or Connector sources.

## Checked

2026-11-04. Confirmed against the ExternalDNS annotations page (hostname section, use cases, support table and its footnote). Removed an unsourced verification line and a vague sentence.
Method: documentation only; no commands were run.
