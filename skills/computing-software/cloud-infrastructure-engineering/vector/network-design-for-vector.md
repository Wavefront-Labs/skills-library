---
id: computing-software.cloud-infrastructure-engineering.vector.network-design-for-vector
name: network-design-for-vector
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [networking, firewall, proxy, dns, protocols, service-discovery, vector]
level: advanced
status: docs-checked
description: "Apply the architecting guidance on network boundaries, proxies, DNS and protocol choice for Vector."
sources:
  - https://vector.dev/docs/setup/going-to-prod/architecting/
  - https://vector.dev/docs/setup/going-to-prod/sizing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Network design points from the architecting document:

**Boundaries.** Deploy aggregators inside each network boundary (cluster or VPC), across accounts and regions, even if that means several aggregators. This avoids a single point of failure, keeps internal communication easy and secure, and respects the network team's boundaries. Management stays centralised through shared configuration.

**Firewalls and proxies.** Restrict agent communication to your aggregators and aggregator communication to its configured sources and sinks. The docs take no position on HTTP proxies, but Vector offers a global proxy option to route all its HTTP traffic through one.

**DNS and service discovery.** Agents and load balancers should find aggregators through DNS or service discovery. Vector does not resolve DNS itself; it delegates to the system-level resolver, for example Linux resolving.

**Protocols.** When sending data to Vector choose a protocol that load-balances easily and gives application-level delivery acknowledgement. The docs prefer HTTP and gRPC for their ubiquity and tooling.

The sizing guide adds: avoid plain TCP, distribute data across many connections, and avoid stateful transforms on aggregators so a fairer balancing algorithm can be used.

## Checked

Method: docs-checked 2026-11-09 against the full Vector architecting page and the sizing page's load-balancing section (raw markdown from the vectordotdev/vector repo). Dropped an unsourced TLS/subnet verification line.
