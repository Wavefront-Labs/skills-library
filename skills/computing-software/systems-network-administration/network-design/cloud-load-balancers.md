---
id: computing-software.systems-network-administration.network-design.cloud-load-balancers
name: cloud-load-balancers
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, cloud-networking, cloud-load-balancer, alb, nlb, azure-load-balancer, health-checks]
level: practitioner
status: docs-checked
description: "Pick and configure cloud load balancers: L4 vs L7, AWS ALB/NLB/GWLB, Azure Load Balancer/App Gateway/Front Door, GCP options, health checks, source IP and TLS."
sources:
  - https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html
  - https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/load-balancing-overview
  - https://cloud.google.com/load-balancing/docs/choosing-load-balancer
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud load balancers

## Matrix
| Need | AWS | Azure | GCP |
|---|---|---|---|
| HTTP(S) L7 regional, path/host routing, WAF | ALB | Application Gateway | regional external/internal Application LB |
| L4 TCP/UDP, static IP, extreme scale, source IP kept | NLB | Azure Load Balancer (Standard) | Network LB (passthrough) |
| Global anycast HTTP, CDN/WAF at edge | CloudFront + ALB, Global Accelerator | Front Door | global external Application LB |
| Inline appliances (firewalls) | Gateway Load Balancer (GENEVE) | Gateway LB | - |

## Key behaviours
- **Source IP**: L7 load balancers terminate the client connection, so backends see the LB
  address; check each product's documentation for how the client IP is passed on (forwarded
  header at L7, preservation or proxy protocol at L4).
- **Health checks**: point at a real dependency-aware endpoint (`/healthz`), tune interval and
  thresholds; security groups/NSGs must allow the probes.
- **Idle timeouts**: each load balancer type has its own idle timeout (look it up per product);
  long-lived connections need keepalives shorter than the timeout.
- **TLS**: terminate at L7 LB with managed certificates (ACM, Key Vault) or pass through at L4;
  re-encrypt to backends where policy requires.
- **Cross-zone**: when enabled, each load balancer node spreads traffic over targets in all enabled
  AZs, otherwise only its own AZ. ALB has it always on at LB level (can be turned off per target
  group); NLB and GWLB default to off.
- Internal vs internet-facing schemes; NLB gives a static IP per AZ (optionally an Elastic IP),
  while load balancer IPs otherwise change as AWS scales it and updates DNS (TTL 60 s): always use
  the DNS name.

## Verify
- [ ] Health checks green across zones, failover test by stopping one target, client IP visible in backend logs as intended.

## Checked
2026-10-28. Confirmed against the AWS Elastic Load Balancing overview (cross-zone defaults per type, NLB static IP per AZ with optional Elastic IP, DNS TTL of 60 seconds with changing IPs, GWLB with GENEVE) and the Azure and Google Cloud load balancer selection guides (product names in the matrix). Removed: the idle-timeout figures (the AWS page's 60 seconds is a DNS TTL, not an idle timeout), the Azure probe address, inter-AZ charge remark and client-IP preservation detail (not in the fetched pages).
Method: documentation only; no commands were run.
