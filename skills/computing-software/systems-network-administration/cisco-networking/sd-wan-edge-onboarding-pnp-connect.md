---
id: computing-software.systems-network-administration.cisco-networking.sd-wan-edge-onboarding-pnp-connect
name: sd-wan-edge-onboarding-pnp-connect
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-sd-wan, sdwan-onboarding, pnp-connect, ztp, vmanage, sd-wan-manager, c8000, vbond, device-list, bootstrap-config]
level: practitioner
status: draft
description: "Onboard Cisco Catalyst SD-WAN edges: device list sync from PnP Connect, ZTP vs bootstrap file, template/config group attach, and fixing devices stuck in staging."
sources:
  - https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/sdwan-xe-gs-book/cisco-sd-wan-overlay-network-bringup.html
  - https://www.cisco.com/c/en/us/td/docs/routers/sdwan/configuration/sdwan-xe-gs-book/pnp-ztp.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SD-WAN edge onboarding and PnP Connect

## Pieces
- **Smart Account / Plug and Play Connect** (software.cisco.com): lists device serials and the
  controller profile (Validator/vBond address, org name) they belong to.
- **SD-WAN Manager (vManage)**: syncs the device list (Configuration > Devices > Sync Smart Account,
  or upload the signed serial file `.viptela`).
- **Validator (vBond)**: authenticates edges by serial/chassis number and certificate.

## Onboarding flow (ZTP)
1. Order or add the device in PnP Connect; associate with the controller profile.
2. Sync to SD-WAN Manager; device appears in the WAN Edge list.
3. Attach a device template or configuration group, fill per-device variables (system IP, site ID,
   hostname, transport IPs).
4. Ship. Edge boots with no config, gets DHCP on a WAN port, contacts PnP Connect (devicehelper.cisco.com),
   learns the validator, authenticates, joins Manager, downloads config.
5. Device moves from staging to valid / in sync.

## Without internet ZTP: bootstrap
Generate a bootstrap file in Manager (WAN Edge list > Generate Bootstrap Configuration, cloud-init
format), put it on USB/bootflash as `ciscosdwan_cloud_init.cfg`, boot the device.

## Converting an autonomous IOS XE router
`controller-mode enable` (17.2+) reboots into controller (SD-WAN) mode and erases config.

## Stuck devices
| Symptom | Check |
|---|---|
| Not reaching PnP | DHCP on WAN, DNS resolution of devicehelper.cisco.com, firewall TCP 443 |
| vBond auth fail | serial not in synced list, `show sdwan control connection-history` errors (BIDNTVRFD, CRTREJSER) |
| Org name mismatch | `show sdwan control local-properties` organization-name vs controllers |
| Certificate/time | clock (NTP) wrong: certificate not yet valid |
| Template push failure | variable errors in Manager task log |

```
show sdwan control connections
show sdwan control connection-history
show sdwan control local-properties
show sdwan certificate serial
```

## Verify
- [ ] Device shows Reachable / In Sync; control connections up to all controllers.
