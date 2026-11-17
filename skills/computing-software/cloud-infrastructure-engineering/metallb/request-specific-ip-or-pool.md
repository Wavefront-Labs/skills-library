---
id: computing-software.cloud-infrastructure-engineering.metallb.request-specific-ip-or-pool
name: request-specific-ip-or-pool
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, loadbalancerips, address-pool-annotation, loadbalancerip, service, annotation]
level: practitioner
status: docs-checked
description: "Request a specific IP (metallb.io/loadBalancerIPs or spec.loadBalancerIP) or a pool (metallb.io/address-pool) for a LoadBalancer Service, and what failure looks like."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/usage/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Requesting specific IPs or pools

Create a Service with `spec.type: LoadBalancer`; MetalLB does the rest. MetalLB attaches informational events to Services: `kubectl describe service <name>`.

Specific IP: MetalLB supports `spec.loadBalancerIP` and the annotation `metallb.io/loadBalancerIPs` (comma-separated list allowed for dual stack). `spec.loadBalancerIP` is planned to be deprecated in the Kubernetes API.
```yaml
metadata:
  name: nginx
  annotations:
    metallb.io/loadBalancerIPs: 192.168.1.100
spec:
  ports:
  - port: 80
    targetPort: 80
  selector:
    app: nginx
  type: LoadBalancer
```
Specific pool, when you want a kind of address but not which one:
```yaml
metadata:
  name: nginx
  annotations:
    metallb.io/address-pool: production-public-ips
```
Failure: if MetalLB does not own the address, or another service uses it, assignment fails and a warning event shows in `kubectl describe service`. A request that conflicts with pool selectors leaves the Service pending (`computing-software.cloud-infrastructure-engineering.metallb.pool-service-allocation-scope`).

Addresses in a pool with `autoAssign: false` can still be specifically allocated this way (`computing-software.cloud-infrastructure-engineering.metallb.pool-auto-assign-and-buggy-ips`). Dual stack: `computing-software.cloud-infrastructure-engineering.metallb.dual-stack-services`.

## Checked

2026-11-04. Confirmed against the MetalLB Usage page (Requesting specific IPs: spec.loadBalancerIP, metallb.io/loadBalancerIPs, comma-separated list for dual stack, planned Kubernetes deprecation, metallb.io/address-pool, failure warning event) and the Advanced AddressPool page (autoAssign, pending when an explicit request does not match). Removed the unsupported Verify line and softened "this way only".

Method: documentation only; no commands were run.
