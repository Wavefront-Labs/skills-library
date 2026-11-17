---
id: computing-software.systems-network-administration.netbox.circuits-providers-terminations
name: circuits-providers-terminations
category: computing-software
field: systems-network-administration
product: netbox
tags: [circuits, providers, circuit-termination]
level: practitioner
status: docs-checked
description: "Record carrier circuits, A/Z terminations and provider networks."
sources: ["https://netboxlabs.com/docs/netbox/features/circuits/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Circuits

Goal: track transit and peering connectivity.

**Providers.** Any organization providing Internet or private connectivity, typically carriers but possibly regional providers or internal services.

**Provider networks.** For networks you cannot see into (drawn as clouds on topology diagrams), model a provider network.

**Circuits.** A circuit is a physical connection between two points, installed and maintained by an external provider, such as an Internet connection delivered over fibre. Each has:

- a provider and a circuit ID that must be unique to that provider
- a user-defined type and an operational status
- up to two terminations, A and Z

Each termination attaches to a site or a provider network. For a site, a cable can run between the circuit termination and a device interface.

**Physical vs virtual.** The circuit model represents physical connections. Provider-offered virtual circuits overlaid on physical infrastructure, such as a VLAN-tagged subinterface, are a different thing; model overlays with L2VPN and overlay features.

**Checklist**

1. Create the provider first.
2. Use unique circuit IDs per provider.
3. Terminate A and Z, then cable.

## Checked

Method: docs-checked 2026-11-09 against https://netboxlabs.com/docs/netbox/features/circuits/ (downloaded and searched for provider, provider network, circuit, termination and virtual circuit passages; all claims confirmed).
