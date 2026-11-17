---
id: computing-software.cloud-infrastructure-engineering.external-dns.target-and-ttl-annotations
name: target-and-ttl-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, target-annotation, ttl-annotation, cname-from-target, default-targets]
level: practitioner
status: docs-checked
description: "Override ExternalDNS record targets and TTL with annotations: how targets become A, AAAA or CNAME records, TTL range, and the Traefik gotcha."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# target and ttl annotations

**`external-dns.kubernetes.io/target`** overrides a resource's record targets (RDATA) with a comma-separated list; empty entries are ignored.

- A target that parses as IPv4 becomes an A record.
- A target that parses as IPv6 becomes an AAAA record.
- Anything else becomes a CNAME.

```yaml
annotations:
  external-dns.kubernetes.io/hostname: app.example.com
  external-dns.kubernetes.io/target: ipv4-only-target.example.com
```

**Traefik gotcha:** Traefik CRDs expose no load balancer IP or hostname in status, so they need an explicit `target` annotation. Without it no endpoint is generated and `--default-targets` cannot apply.

**Gateway API:** the `target` annotation is read from the Gateway (and ListenerSet), not the Route. See the Gateway API placement skill.

**`external-dns.kubernetes.io/ttl`** sets the TTL, as a duration or an integer number of seconds, between `1` and `2,147,483,647`. A value of `0` means TTL is not configured, so the default is used.

Sources that read `ttl`: Ambassador, Contour, F5, Gateway, Gloo (on the listener's VirtualService), Ingress, Istio, Kong, Node, OpenShift, Service, Skipper, Traefik. The Pod source does not. For Gateway API, `ttl` is read from the Route resources, not the Gateway.

**Verify:** query the record (`dig`) and compare the returned TTL and answer type with the annotation.

## Checked

2026-11-04. Read the annotations page (support table, target, ttl, Gateway API Annotation Placement, Traefik footnote). Confirmed the A/AAAA/CNAME rules, empty-entry handling, the 1 to 2,147,483,647 range, 0 meaning not configured, the source list and the Traefik requirement. Added the Gateway API note that ttl is read from Routes.

Method: documentation only; no commands were run.
