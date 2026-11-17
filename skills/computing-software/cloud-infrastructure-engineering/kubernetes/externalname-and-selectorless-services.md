---
id: computing-software.cloud-infrastructure-engineering.kubernetes.externalname-and-selectorless-services
name: externalname-and-selectorless-services
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, services, externalname, service-without-selector, manual-endpointslices, external-database, endpointslice-managed-by]
level: practitioner
status: docs-checked
description: "Point in-cluster names at external systems: ExternalName Services (DNS CNAME) and their TLS/Host caveats, versus selector-less Services with hand-managed EndpointSlices."
sources: ["https://kubernetes.io/docs/concepts/services-networking/service/#externalname", "https://kubernetes.io/docs/concepts/services-networking/service/#services-without-selectors", "https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# ExternalName and selector-less Services

Goal: apps use a stable in-cluster name (`db.prod.svc`) while the backend lives outside the
cluster (managed database, on-prem DB, another cluster) and can be moved in later without app
changes.

## ExternalName (DNS alias)
```yaml
apiVersion: v1
kind: Service
metadata: {name: db, namespace: prod}
spec:
  type: ExternalName
  externalName: my.database.example.com
```
Looking up `db.prod.svc.cluster.local` returns a `CNAME` record with the value of
`externalName`. Redirection happens at DNS level, not by proxying; the cluster DNS server is the
only way to reach an ExternalName Service.
Caveats:
- HTTP and TLS: clients use the in-cluster hostname, which differs from the external name. HTTP
  requests carry a `Host:` header the origin does not recognise, and TLS servers cannot present a
  certificate matching the in-cluster name.
- `externalName` must be a DNS name. An IPv4-looking string is treated as a DNS name made of
  digits and is not resolved; to map to an IP use a headless or selector-less Service.
- Anyone who can create Services can alias internal names to arbitrary hosts; review this in
  multi-tenant clusters.

## Selector-less Service + EndpointSlice (fixed IPs)
```yaml
apiVersion: v1
kind: Service
metadata: {name: legacy-api, namespace: prod}
spec:
  ports: [{name: http, port: 80, targetPort: 8080, protocol: TCP}]
---
apiVersion: discovery.k8s.io/v1
kind: EndpointSlice
metadata:
  name: legacy-api-1
  namespace: prod
  labels:
    kubernetes.io/service-name: legacy-api
    endpointslice.kubernetes.io/managed-by: platform-team    # your own value, not the controller's
addressType: IPv4
ports: [{name: http, port: 8080, protocol: TCP}]
endpoints:
- addresses: ["10.20.0.15"]
- addresses: ["10.20.0.16"]
```
Without a selector the control plane does not create EndpointSlices for the Service; you create
and maintain them, and pick your own `managed-by` value. Endpoint IPs must not be loopback
(127.0.0.0/8, ::1/128) or link-local (169.254.0.0/16, 224.0.0.0/24, fe80::/64). Remove dead
addresses yourself.

## Verify
```bash
kubectl get endpointslices -n prod -l kubernetes.io/service-name=legacy-api
```
- [ ] Apps reach the external backend via the Service name; cutover = changing only the Service.

## Checked

2026-10-23, Kubernetes documentation (kubernetes/website main, v1.36 docs) and kubernetes/kubernetes source. Confirmed against the Service concept page (ExternalName CNAME behaviour, HTTP/TLS caution, IPv4-string note, loopback and link-local restrictions on endpoint IPs, managed-by label guidance) and the EndpointSlice page. Removed unconfirmed claims about port handling, NetworkPolicy visibility, kube-proxy load balancing detail and the busybox command.

Method: documentation only; no commands were run.
