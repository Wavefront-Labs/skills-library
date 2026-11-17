---
id: computing-software.messaging-and-integration.dapr.placement-service-production-config
name: placement-service-production-config
category: computing-software
field: messaging-and-integration
product: dapr
tags: [placement, actors, raft, helm, keepalive, production, high-availability]
level: advanced
status: docs-checked
description: "Recommended Placement service Helm values for production actors: HA, in-memory Raft log, disabling the metadata endpoint, and the keepAlive and disseminate timeouts."
sources:
  - https://github.com/dapr/docs/blob/v1.15/daprdocs/content/en/operations/hosting/kubernetes/kubernetes-production.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Placement service distributes actor addresses to sidecars via the placement table. The production guidelines recommend:

1. High availability, three replicas that survive node failures: `dapr_placement.ha=true`.
2. In-memory Raft log for faster writes: `dapr_placement.cluster.forceInMemoryLog=true`. The tradeoff is more table disseminations (and network traffic) after a Placement pod failure.
3. No metadata endpoint, because `/placement/state` is unauthenticated and exposes the placement table: `dapr_placement.metadataEnabled=false`.
4. Timeouts, which have defaults but can be tuned to network conditions:
   - `dapr_placement.keepAliveTime`: interval of gRPC keep-alive pings from Placement to sidecars. Lower values give shorter actor rebalancing after a pod failure.
   - `dapr_placement.keepAliveTimeout`: how long sidecars have to answer a ping before Placement closes the connection. Lower also means faster rebalancing.
   - `dapr_placement.disseminateTimeout`: delay of dissemination after a membership change (usually pod restarts), to avoid repeated dissemination during several restarts. Higher values mean fewer disseminations but a longer wait for the table to update.

As a values file this maps to a `dapr_placement:` block with `ha`, `cluster.forceInMemoryLog` and `metadataEnabled`. The page lists Placement as an optional control plane deployment, needed for Dapr Actors. Timeout ranges and defaults on the page: keepAliveTime 1s-10s (default 2s), keepAliveTimeout 1s-10s (default 3s), disseminateTimeout 1s-3s (default 2s).

## Checked

2026-11-08. Read the cited dapr/docs v1.15 page in full and compared each claim; wording tightened where it went beyond the page, the remaining claims are unchanged.

Method: documentation only; no commands were run.
