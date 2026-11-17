---
id: computing-software.cloud-infrastructure-engineering.kubernetes.dns-record-formats
name: dns-record-formats
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, coredns, srv-records, pod-dns-records, headless-service, cluster-dns]
level: practitioner
status: docs-checked
description: "Kubernetes DNS record formats: Service A/AAAA, SRV for named ports, headless per-pod records, pod hostname/subdomain records and pod IP-based names."
sources: ["https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/", "https://coredns.io/plugins/kubernetes/", "https://github.com/kubernetes/dns/blob/master/docs/specification.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Kubernetes DNS record formats

The cluster domain is written below as `cluster.local`; yours may differ (the docs use
`cluster-domain.example`).

## Services
| Record | Name | Answer |
|---|---|---|
| A/AAAA (normal Service) | `my-svc.my-namespace.svc.cluster.local` | the cluster IP |
| A/AAAA (headless) | same form | the set of IPs of the ready endpoints |
| SRV (named port) | `_port-name._port-protocol.my-svc.my-namespace.svc.cluster.local` | port number and the domain name of the Service (headless: of each Pod) |
| CNAME (ExternalName) | same form | the `externalName` value |

SRV records exist only for named ports of normal or headless Services.
```bash
dig +short SRV _http._tcp.web.shop.svc.cluster.local
```

## Pods behind a headless Service
When a Pod sets `spec.hostname` and `spec.subdomain`, and a headless Service with the same name as
the subdomain exists in the same namespace, the DNS server returns A and/or AAAA records for the
Pod's fully qualified name `hostname.subdomain.my-namespace.svc.cluster.local`.

## Pod IP names
The kubernetes plugin of CoreDNS can answer IP-based Pod names such as `1-2-3-4.ns.pod.cluster.local`
with its `pods POD-MODE` option; `disabled` (the plugin default) returns NXDOMAIN, `insecure` answers an A record with
the IP from the request without checking Kubernetes, `verified` answers only if a Pod with that IP
exists in the same namespace. The Corefile that kubeadm generates uses
`pods insecure`.

## Gotchas
- Records for a Pod's own name need the subdomain to match a headless Service in the same
  namespace.
- The Service documentation lists A/AAAA records as being for the Service's ready endpoints.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the DNS for Services and Pods page (record names and forms, SRV for named ports, hostname/subdomain rules), the CoreDNS kubernetes plugin README (pods modes) and kubeadm's DNS manifest source (pods insecure). Removed the hostname 63-character claim, the netshoot test script and the statement about selector-less headless Services.

Method: documentation only; no commands were run.
