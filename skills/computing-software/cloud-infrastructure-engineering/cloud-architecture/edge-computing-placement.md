---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.edge-computing-placement
name: edge-computing-placement
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, edge-computing-placement, edge-computing, local-zones, wavelength, cdn-edge-functions, iot-edge, distributed-cloud, latency-placement]
level: advanced
status: draft
description: "Place compute across region, metro edge, CDN edge functions and on-site edge: latency budgets, offline needs, data volume, fleet management, what stays central."
sources: ["https://aws.amazon.com/about-aws/global-infrastructure/localzones/", "https://learn.microsoft.com/azure/iot-edge/about-iot-edge", "https://cloud.google.com/distributed-cloud", "https://developers.cloudflare.com/workers/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Edge and distributed cloud placement

## Tiers
| Tier | Latency to user/device | Examples | Use for |
|---|---|---|---|
| Region | tens of ms | standard cloud regions | most workloads, data of record |
| Metro edge | single-digit ms in a city | AWS Local Zones, Wavelength (5G), Azure Extended Zones | gaming, media production, real-time interaction |
| CDN edge | close to every user | CloudFront Functions/Lambda@Edge, Cloudflare Workers, Fastly Compute, Front Door rules | auth checks, redirects, personalisation, A/B routing |
| On-site edge | on premises | Azure IoT Edge / Azure Local, AWS Outposts/Greengrass, Google Distributed Cloud | factories, stores, offline operation, bandwidth reduction |

## Decide per function
1. Latency budget: does physics require proximity?
2. Offline operation needed when WAN is down?
3. Data volume: process/filter locally when raw data is too big to ship (video, sensor streams).
4. Data residency at site level.
Keep central: system of record, heavy analytics, training, control plane.

## Fleet management
GitOps or IoT fleet tooling for hundreds of sites, staged rollouts, remote health, secure boot
and device identity, update rollback, local caching of config and secrets.

## Gotchas
- Edge locations offer a subset of services and capacity.
- State at the edge needs conflict resolution when sites sync.

## Verify
- [ ] Placement table per function with latency/offline/data-volume justification.
