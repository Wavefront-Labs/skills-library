---
id: computing-software.cloud-infrastructure-engineering.gateway-api.tcproute-and-udproute-l4-routing
name: tcproute-and-udproute-l4-routing
category: computing-software
field: cloud-infrastructure-engineering
product: gateway-api
tags: [tcproute, udproute, l4, tcp, udp, standard-channel]
level: practitioner
status: docs-checked
description: "Use TCPRoute and UDPRoute for non-HTTP traffic: listener protocol TCP or UDP, port-based routing, per-connection weighting, and oldest-Route-wins on shared listeners."
sources:
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/tcproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/reference/api-types/udproute.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/tcp.md
  - https://github.com/kubernetes-sigs/gateway-api/blob/main/site/content/en/guides/user-guides/udp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`TCPRoute` and `UDPRoute` forward layer-4 traffic. There is no hostname or path to match, so routing is by listener port.

Listener: define a listener with `protocol: TCP` or `protocol: UDP` and a `port`. A Route attaches to it through `parentRefs`, optionally with `sectionName` or `port`; with neither, a TCPRoute attaches to every TCP listener of the Gateway (likewise UDP). A TCPRoute or UDPRoute cannot attach to an HTTP or HTTPS listener, and the route is then not accepted.

Route: a Route has a single rule whose `backendRefs` (1 to 16) list the target Services and ports. There are no hostnames, matches or filters. With several backends, TCP connections (each new SYN is one unit) or UDP datagrams are distributed by `weight`; weight support is Extended. An invalid backendRef (missing object, or a Service with no endpoints) must be actively rejected for TCP or dropped for UDP, respecting weight.

Conflicts: with no hostname, SNI or path to differentiate connections, several TCPRoutes (or UDPRoutes) attached to the same listener are all `Accepted`, but only the oldest (by `metadata.creationTimestamp`, then alphabetically by `namespace/name`) receives traffic. Use separate listeners, selected with `sectionName`, for separate backends.

Typical uses: databases (PostgreSQL, MySQL, Redis), message brokers (Kafka, RabbitMQ, NATS), mail protocols such as SMTP and IMAP for TCP; DNS, VoIP, gaming, RTP/RTCP streaming and IoT telemetry for UDP. An implementation MAY support a TCP and a UDP listener on the same port, for example DNS on port 53.

When you need TLS-aware routing without terminating, prefer TLSRoute with SNI instead of a raw TCPRoute.

Channel: the TCPRoute, UDPRoute and TCP routing pages say the resources are GA and in the Standard Channel since v1.6.0 (the UDP routing guide has no channel banner). Check your installed CRD version and your implementation's documentation, since implementations may support only some route kinds.

## Checked

2026-11-08. Read in full: the TCPRoute and UDPRoute reference pages and the TCP routing and UDP routing guides (raw markdown on GitHub). Confirmed: Standard Channel since v1.6.0 (TCP and UDP reference pages and the TCP guide), listener protocol:port classification, no hostnames, matches or filters, single rule with 1 to 16 backendRefs, Extended weight support, per-SYN weighting for TCP, invalid backend handling, attach to every listener of that protocol when sectionName and port are absent, no attachment to HTTP or HTTPS listeners, oldest-route-wins on a shared listener, and TCP plus UDP on one port. Replaced: the earlier Experimental statement. Removed: the supportedFeatures and supportedKinds pointer.

Method: documentation only; no commands were run.
