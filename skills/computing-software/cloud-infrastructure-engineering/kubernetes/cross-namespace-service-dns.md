---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cross-namespace-service-dns
name: cross-namespace-service-dns
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, namespace, cross-namespace-dns, coredns, service-discovery]
level: practitioner
status: docs-checked
description: "Reach Services in other namespaces by DNS (svc.ns, FQDN), how search paths resolve short names, and NetworkPolicy and ExternalName considerations."
sources: ["https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/", "https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/#namespaces-and-dns"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cross-namespace Service DNS

## Names
| From a pod in `web` | Resolves |
|---|---|
| `api` | `api.web.svc.cluster.local` (same namespace only) |
| `api.backend` | `api.backend.svc.cluster.local` |
| `api.backend.svc` | same |
| `api.backend.svc.cluster.local.` | same, absolute, no search path |

Pod `/etc/resolv.conf` (documented default):
```
search web.svc.cluster.local svc.cluster.local cluster.local
options ndots:5
```
A short name such as `api.backend` has fewer than 5 dots, so the resolver walks the search list
before trying the name as given. Use a fully qualified name with a trailing dot to avoid the
extra lookups.

The cluster domain may not be `cluster.local`; the documentation writes it as
`cluster-domain.example`.

## Access control
DNS answers do not depend on NetworkPolicy. Traffic still has to be allowed:
- an ingress rule in `backend` that admits the `web` namespace (select it with the
  `kubernetes.io/metadata.name` label);
- if egress is restricted in `web`, rules that allow `backend` and the cluster DNS Service.

## Alias a remote Service locally
```yaml
apiVersion: v1
kind: Service
metadata: {name: api, namespace: web}
spec:
  type: ExternalName
  externalName: api.backend.svc.cluster.local
```
Apps keep using `api`. ExternalName is a DNS CNAME: HTTP `Host` headers and TLS server names are
still the in-cluster name the client used, which may not match what the server expects.

## Verify
```bash
kubectl -n web run t --rm -it --image=<image-with-nslookup> --restart=Never -- nslookup api.backend
```
Use a DNS test image you trust; the Kubernetes DNS debugging page uses an agnhost-based `dnsutils`
Pod.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the DNS for Services and Pods page (name forms, default resolv.conf with ndots:5, search list), the Service page (ExternalName CNAME caveats) and the NetworkPolicy page (namespace label selector). Removed the claim about the exact resolution order and NXDOMAIN steps, the CoreDNS ConfigMap lookup for the domain, and the busybox/netshoot images and curl command.

Method: documentation only; no commands were run.
