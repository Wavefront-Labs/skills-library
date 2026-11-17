---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-unifi-controller-model
name: nda-unifi-controller-model
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [unifi-network-controller, unifi-adoption, unifi-site-management]
level: practitioner
status: draft
description: "Understand the UniFi Network controller: adoption of devices, sites, settings push, backups and where the data plane lives."
sources:
  - https://help.ui.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UniFi controller model

- The UniFi Network application (self-hosted or on a Cloud Gateway/console) holds the configuration; devices are adopted by it and provisioned with the site's settings.
- Adoption: the device must reach the controller (L2 discovery, DHCP option 43, or `set-inform` to the controller URL). A device stuck in "Adopting" often cannot reach the inform URL.
- Sites separate configuration sets; one controller can manage many.
- Devices keep forwarding if the controller is offline, but config changes and some features (e.g. guest portal, stats) depend on it.
- Always take controller backups (settings backup, auto-backup) before upgrades.
- UI names and menus change between releases; consult the current help centre.

## Verify
- [ ] The device shows "Connected" and the last configuration provisioned time matches your change.
