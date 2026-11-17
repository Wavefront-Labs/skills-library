---
id: computing-software.cloud-infrastructure-engineering.external-dns.aws-route53-routing-policies
name: aws-route53-routing-policies
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, aws-weight, aws-failover, aws-region-latency, aws-health-check-id, geolocation-routing]
level: advanced
status: docs-checked
description: "Choose Route53 routing policies from Kubernetes annotations: set-identifier plus one of weight, latency, failover, geolocation, geoproximity or multi-value, and health check IDs."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/aws.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route53 routing policies via annotations

`external-dns.kubernetes.io/set-identifier` **must** be set to use any policy. For a given DNS name use only **one** policy:

| Policy | Annotation(s) |
|---|---|
| Weighted | `aws-weight` |
| Latency | `aws-region` |
| Failover | `aws-failover` (`PRIMARY` or `SECONDARY`) |
| Geolocation | `aws-geolocation-continent-code`, `-country-code`, `-subdivision-code` |
| Geoproximity | `aws-geoproximity-region`, `-local-zone-group`, `-coordinates`, `-bias` |
| Multi-value | `aws-multi-value-answer` |

All use the prefix `external-dns.kubernetes.io/`.

**Weighted example:** two Services with the same `hostname: app.example.com`, identifiers `app-v1` (weight "80") and `app-v2` (weight "20") produce two weighted record sets, 80% and 20%.

**Failover:** two Ingresses with identifiers `my-app-primary` and `my-app-secondary`, `aws-failover: PRIMARY` and `SECONDARY`. Route53 serves PRIMARY while healthy and falls back to SECONDARY when the health check fails.

**Latency:** Services in each region share the hostname, with different identifiers and `aws-region: us-east-1` / `eu-west-1`.

**Health checks:** `external-dns.kubernetes.io/aws-health-check-id: <id>` associates a record with an existing check. ExternalDNS does not create health checks.

**Multi-cluster:** routing policies let one ExternalDNS per cluster publish the same hostname, each owning its own record set.

**TTL:** default 300 s; override with the `ttl` annotation.

## Checked

2026-11-04. Read the AWS tutorial (Custom TTL, Routing policies, Weighted, Failover, Latency, healthchecks). Confirmed the set-identifier requirement, the one-policy-per-name rule, every annotation name in the table, the weighted 80/20 and failover examples, the latency example, aws-health-check-id with no health-check creation, the multi-cluster note and the 300 second default TTL. Removed nothing.

Method: documentation only; no commands were run.
