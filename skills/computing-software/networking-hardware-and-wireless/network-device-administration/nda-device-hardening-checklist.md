---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-device-hardening-checklist
name: nda-device-hardening-checklist
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [network-device-hardening, cis-benchmark-network, control-plane-policing]
level: advanced
status: draft
description: "Apply a hardening baseline: control-plane policing, disabled services, DHCP snooping/DAI on edge, uRPF, and encrypted secrets."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hardening baseline

- Control-plane policing/protection limits traffic punted to the CPU.
- Layer 2 edge: DHCP snooping, Dynamic ARP Inspection, IP Source Guard, port security or MAC limits, BPDU guard.
- uRPF on edge routed interfaces; disable IP source routing and directed broadcasts.
- Strong password storage (type 8/9 on IOS-XE), disable unused ports, and log-in banners.
- Use the CIS Benchmarks and the vendor's hardening guide as the checklist; document exceptions.

## Verify
- [ ] An automated compliance scan against the baseline reports no unexplained failures.
