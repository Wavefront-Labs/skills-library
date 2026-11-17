---
id: computing-software.systems-network-administration.icinga-2.cluster-security-model-and-versions
name: cluster-security-model-and-versions
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, cluster-security, tls, json-rpc, zone-trust, upgrade-order, version-compatibility]
level: advanced
status: docs-checked
description: Icinga 2 cluster trust and security rules - TLS 1.2+, mandatory certificates, one zone per object, parent-only config push - plus version compatibility and upgrade order.
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/06-distributed-monitoring/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cluster security model and versions
Security properties listed in the docs:
- TLS v1.2 or newer is required and cipher lists are hardened by default.
- TLS certificates are mandatory between nodes; the CLI wizards create them.
- Child zones receive updates (check results, commands) only for their configured objects, and cannot push configuration to parent zones.
- Zones cannot interfere with each other. Each checkable host or service object is assigned to one zone only.
- All nodes within a zone trust each other.
- Config sync and remote command endpoint execution only work if the receiving side allows it in its `api` feature.

Trust follows zones. If you do not configure a zone and its parent for an agent or satellite, its parent (for example the master) will not trust it. A parent can send configuration objects, global-zone configuration and commands to a child zone and receives check results back. A child that attempted to send configuration upward would be denied, which prevents one agent from modifying another or injecting a malicious check command.

**Versions.** Use the newest releases, the same version everywhere. Target compatibility: master (2.11) >= satellite (2.10) >= agent (2.9); older agents may work without guarantee. Upgrade the master first, then satellites, then agents. Some features require all instances to be upgraded together, for example the CA Proxy and on-demand signing (since v2.8); check the upgrading docs.

## Checked

2026-11-04. Confirmed against the Icinga 2 distributed monitoring chapter: security properties, trust via zones, version compatibility master 2.11 / satellite 2.10 / agent 2.9, upgrade order, CA Proxy since v2.8.

Method: documentation only; no commands were run.
