---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.service-oriented-architecture-with-some-ip
name: service-oriented-architecture-with-some-ip
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [soa-someip, someip, some-ip, service-discovery, service-oriented-architecture, ara-com, ethernet-middleware, dds, service-interface, zonal-architecture, autosar-adaptive]
level: practitioner
status: gated
description: "Design vehicle service-oriented communication with SOME/IP: services, methods, events and fields, service discovery, versioning, latency and security considerations."
sources:
  - "AUTOSAR SOME/IP Protocol Specification, R22-11 (https://www.autosar.org/fileadmin/standards/R22-11/FO/AUTOSAR_PRS_SOMEIPProtocol.pdf)"
  - "AUTOSAR SOME/IP Service Discovery Protocol Specification, R22-11 (https://www.autosar.org/fileadmin/standards/R22-11/FO/AUTOSAR_PRS_SOMEIPServiceDiscoveryProtocol.pdf)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Service-oriented architecture with SOME/IP

## 1. Concept
Instead of broadcasting signals on a bus, ECUs offer **services** that other ECUs find and use at run time. SOME/IP (Scalable service-Oriented MiddlewarE over IP) defines message format and service discovery over Ethernet (UDP or TCP), used by AUTOSAR Classic and Adaptive platforms (Adaptive exposes it through the ara::com API (gated: unconfirmed, source is paywalled or blocked)). Other middleware such as DDS also appears in vehicles; the same architectural reasoning applies.

## 2. Service model
- **Method (request/response or fire-and-forget):** call a function on a provider.
- **Event:** provider notifies subscribed consumers on change or cycle.
- **Field:** a stateful value with getter, setter and notifier.
Each service interface has an ID, a major version (the SOME/IP header's 8-bit interface version) plus a minor version carried in service discovery, and method/event identifiers; define in ARXML or the platform's description.

## 3. Service discovery (SOME/IP-SD)
Providers send Offer entries (unicast or multicast); consumers send Find entries (multicast) and Subscribe entries for eventgroups; entries include a TTL in seconds, major and minor version of the service, and endpoint options. Design startup order and timers so services are available within the ECU boot time requirement; plan for stop-offer on shutdown and failure detection by TTL.

## 4. Design guidance
- Design coarse-grained, stable interfaces (avoid chatty per-signal services). Group by function, not by ECU.
- Choose UDP for events and small methods (low latency) and TCP where reliability matters; mind MTU and fragmentation.
- Version policy: breaking changes increment major version; consumers may support several versions.
- Timing: budget end-to-end latency (serialisation, stack, switch, network scheduling); use time-sensitive Ethernet (TSN) shaping or priority for control traffic; do not run hard real-time control loops over best-effort service communication without proof.
- Safety: end-to-end protection (E2E) for safety-relevant data.
- Security: authentication and encryption where needed (SecOC variants, IPsec, MACsec or TLS), access control on who may find and call services.

## 5. Tooling and test
Service description in ARXML or Franca-like IDL and generators; Wireshark dissectors for SOME/IP and SD (gated: unconfirmed, source is paywalled or blocked); tools such as CANoe for simulation (gated: unconfirmed, source is paywalled or blocked); automated tests for discovery, subscription, error cases, version mismatch, and load.

## Verify
- [ ] Service interfaces defined, versioned and reviewed by provider and consumer teams.
- [ ] Discovery timing meets the startup budget.
- [ ] End-to-end latency measured under load.
- [ ] Safety (E2E) and security measures defined where required.
