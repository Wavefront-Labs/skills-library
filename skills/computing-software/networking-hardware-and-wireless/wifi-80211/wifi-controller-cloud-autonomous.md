---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-controller-cloud-autonomous
name: wifi-controller-cloud-autonomous
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wlan-architectures, cloud-managed-wifi, wireless-lan-controller, wifi-architectures]
level: practitioner
status: draft
description: "Compare controller-based, cloud-managed and autonomous AP architectures for data-plane location, failure modes and licensing."
sources:
  - https://www.cisco.com/
  - https://help.ui.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WLAN architectures

- Autonomous APs: each configured individually; fine for a few APs, painful at scale.
- Controller-based: centralised management; data plane may be tunnelled (CAPWAP) or local-switched (FlexConnect/local bridging). Know what survives a WAN or controller outage.
- Cloud-managed: cloud control plane, local data plane; APs continue forwarding if the cloud is unreachable but configuration changes wait. Check licence-expiry behaviour before buying.
- Questions: where does user traffic exit, what happens on controller loss, how are RADIUS requests sourced, and how firmware rollouts are staged.

## Verify
- [ ] Failure test: unplug the controller/WAN and confirm existing clients stay connected and new clients can still associate as designed.
