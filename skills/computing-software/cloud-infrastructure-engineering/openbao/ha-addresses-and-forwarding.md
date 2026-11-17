---
id: computing-software.cloud-infrastructure-engineering.openbao.ha-addresses-and-forwarding
name: ha-addresses-and-forwarding
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, high-availability, api-addr, cluster-addr, request-forwarding]
level: practitioner
status: docs-checked
description: "Configure OpenBao HA: api_addr and cluster_addr, request forwarding vs 307 redirects, default ports and load balancer pitfalls."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/ha.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HA addresses and forwarding

- A redirect address is always required for HA. Some storage drivers detect it, often you set it by hand.
- Startup output shows `(HA available)` when the data store supports HA.

## Addresses

- `api_addr`: a full URL including scheme (`http`/`https`), not just IP and port. Env var `BAO_API_ADDR` overrides it. With direct client access each node uses its own address; behind a load balancer that is the only access path, every node uses the load balancer's.
- `cluster_addr`: host or IP with port that standbys use to reach the active node. Scheme is forced to https. Env var `BAO_CLUSTER_ADDR` overrides it.

## Forwarding vs redirect

- Request forwarding is on by default: standbys relay to the active node over mutually authenticated TLS 1.2.
- A client forces redirection by sending `X-Vault-No-Request-Forwarding` with any non-empty value.
- Redirection returns HTTP 307 to the active node's redirect address, and is the fallback when forwarding is off or fails.

## Ports

Examples use 8200 for the API. Cluster listeners default to the address port plus one (8201). Only the active node runs cluster listeners.

## Gotchas

- HA by itself does not add scalability; the data store is usually the bottleneck. Since v2.5.0 Raft standbys can serve reads that do not write to storage (PostgreSQL since v2.7.0); `disable_standby_reads=true` turns this off.
- A load balancer as the only access path can cause redirect loops; avoid when possible.

## Checked

2026-11-04. Confirmed against the High availability concepts page: HA available output, api_addr and cluster_addr rules and environment variables, forwarding over mutually authenticated TLS 1.2, the X-Vault-No-Request-Forwarding header, 307 redirects, cluster listener port plus one, active-only listeners and the load balancer redirect loop. Corrected the scalability gotcha: the page also says standbys can serve reads since v2.5.0 (Raft) and v2.7.0 (PostgreSQL).

Method: documentation only; no commands were run.
