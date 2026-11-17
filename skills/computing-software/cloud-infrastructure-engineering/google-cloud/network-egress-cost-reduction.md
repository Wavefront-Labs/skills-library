---
id: computing-software.cloud-infrastructure-engineering.google-cloud.network-egress-cost-reduction
name: network-egress-cost-reduction
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cost-optimisation, egress-cost-reduction, inter-zone-egress, cloud-cdn, private-google-access, network-pricing]
level: practitioner
status: docs-checked
description: "Reduce Google Cloud network egress spend: find the flows with Flow Analyzer, avoid inter-zone and external-IP traffic, use Cloud CDN and Standard Tier."
sources: ["https://cloud.google.com/vpc/network-pricing", "https://cloud.google.com/network-intelligence-center/docs/flow-analyzer/overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network egress cost reduction

## Find it
Export billing data to BigQuery and group network SKUs (egress, inter-zone, data transfer) by SKU description and
project to find the top flows. Then use Flow Analyzer to map them to workloads: it analyses VPC Flow Logs held in a log
bucket (so VPC Flow Logs must be on and the project must have that log bucket), at 5-tuple granularity, and VPC Flow
Logs are documented as usable for expense optimisation. Rates are on the Network pricing page; do not copy figures.

## Levers by traffic type
| Traffic | Lever (as the Network pricing page describes the billing) |
|---|---|
| Between zones in the same region | Billed per GiB using internal or external IPs in the same VPC; keep chatty pairs together. All traffic to and from external IPv4 addresses leaves the zone regardless of destination |
| Between VPC networks using external IPs | Billed at internet data transfer rates; use internal connectivity instead |
| Internet egress to users | Premium Tier is the default; Standard Tier uses the public internet, is lower quality of service and more economical, and must be specified explicitly |
| Static content behind a global external Application Load Balancer | Cloud CDN: objects served from cache do not transit the load balancer, so a good caching strategy reduces outbound data processing |
| To other Google Cloud services in the same region | No charge except for Memorystore for Redis, Filestore, GKE and Cloud SQL, so check those services' own entries |

## Gotchas
- Ingress is free; egress is what you pay for.
- Interconnect, Cloud CDN, CDN Interconnect and peering traffic use their own pricing pages, not the generic rates.
- Unused reserved static external IPs are charged at a higher rate than in-use ones.

## Verify
- [ ] Top egress SKUs reduced month over month with attributable changes.

## Checked
2026-11-09: confirmed against the VPC Network pricing page (inter-zone and external-IP billing rules, tier descriptions,
Cloud CDN caching note, free ingress, service exceptions, unused static IP charge) and the Flow Analyzer overview.
Removed: the SQL (column names unread), Private Google Access and NAT-processing claims, Media CDN, Cross-Cloud, compression
and GKE-topology advice, and all figures. The Well-Architected networking cost page is a landing page and was not used.
Method: documentation only; no commands were run.
