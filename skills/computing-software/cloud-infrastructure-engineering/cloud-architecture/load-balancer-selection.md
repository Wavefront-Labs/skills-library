---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.load-balancer-selection
name: load-balancer-selection
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, network-topology, load-balancer-selection, alb, nlb, application-gateway, front-door, cloud-load-balancing, l4-vs-l7, ingress-architecture]
level: practitioner
status: draft
description: "Select load balancers and design ingress: L4 vs L7, regional vs global, internal vs external, TLS termination, health checks, source IP preservation and WAF placement."
sources: ["https://learn.microsoft.com/azure/architecture/guide/technology-choices/load-balancing-overview", "https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html", "https://cloud.google.com/load-balancing/docs/choosing-load-balancer"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Load balancer selection and ingress architecture

## Decision axes
1. **Layer**: L7 (HTTP routing, host/path rules, header manipulation, WAF) vs L4 (TCP/UDP, TLS
   passthrough, static IPs, extreme throughput, non-HTTP protocols).
2. **Scope**: global anycast (Azure Front Door, Google global external ALB, AWS CloudFront +
   Global Accelerator) vs regional.
3. **Exposure**: internet-facing vs internal.

## Mapping (common choices)
| Need | AWS | Azure | Google Cloud |
|---|---|---|---|
| Regional HTTP(S) | ALB | Application Gateway | Regional external/internal ALB |
| Global HTTP(S) | CloudFront (+ ALB origins) | Front Door | Global external ALB |
| L4 TCP/UDP | NLB | Load Balancer (Standard) | Network LB (passthrough / proxy) |
| Static anycast IPs, non-HTTP global | Global Accelerator | Cross-region LB | Global proxy NLB |
| Kubernetes ingress | AWS LB Controller | AGIC / App Gateway for Containers | GKE Gateway |

## Design checklist
- TLS termination point and certificate management; end-to-end TLS where required.
- Health checks hit a meaningful endpoint (dependency-aware readiness, not just `/`).
- Source IP: L7 uses `X-Forwarded-For`; L4 passthrough preserves client IP or uses Proxy Protocol.
- Idle timeouts aligned with app/keepalive (ALB default 60 s).
- Cross-zone load balancing behaviour and cost.
- WAF attached at the edge (Front Door/CloudFront/Cloud Armor) or regional L7.

## Gotchas
- Health checks too aggressive cause flapping; too lenient keep sending to broken instances.
- Long-lived connections (WebSockets, gRPC) need L7 support and sensible timeouts.

## Verify
- [ ] Instance/zone failure test: traffic drains within health-check interval x threshold.
- [ ] Client IP visible in app logs as required.
