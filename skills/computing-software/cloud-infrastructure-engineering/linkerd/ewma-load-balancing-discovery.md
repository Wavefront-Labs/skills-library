---
id: computing-software.cloud-infrastructure-engineering.linkerd.ewma-load-balancing-discovery
name: ewma-load-balancing-discovery
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, load-balancing, ewma, grpc, service-discovery]
level: practitioner
status: docs-checked
description: "Understand Linkerd's EWMA request-level load balancing and when it falls back to direct routing for pods and headless Services."
sources:
  - https://linkerd.io/2.19/features/load-balancing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For HTTP, HTTP/2 and gRPC connections, Linkerd balances individual requests across all endpoints with no configuration. For plain TCP it balances connections. The algorithm is EWMA, an exponentially weighted moving average of latency, which sends requests to the fastest endpoints and can reduce end-to-end latency.

Discovery behaviour:

- Destinations outside Kubernetes are balanced across endpoints returned by DNS.
- In Kubernetes, Linkerd looks up the destination IP in the API. If it belongs to a Service, it balances across that Service's endpoints and applies the Service's policy and profile.
- If the IP belongs to a Pod, there is no load balancing and no Service Profile applies.
- For headless Services the endpoints cannot be retrieved, so Linkerd does not balance and routes only to the target IP.

This is why gRPC benefits so much: Kubernetes' default connection-level balancing does not spread load across long-lived HTTP/2 connections, whereas Linkerd balances each request.

Practical consequences:

- Have clients call the Service name, not pod IPs, to get balancing and route policy.

## Checked

2026-11-03. Confirmed against: https://linkerd.io/2.19/features/load-balancing/.

Removed or reworded: Connection-pinning and circuit-breaking/retry bullets, which the page does not state.

Method: documentation only; no commands were run.
