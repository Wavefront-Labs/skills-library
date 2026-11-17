---
id: computing-software.digital-privacy-hygiene.device-hardening.iot-and-smart-device-firmware-updates
name: iot-and-smart-device-firmware-updates
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, iot-firmware-updates, smart-home, firmware-updates, end-of-support]
level: practitioner
status: draft
description: "Keep cameras, plugs, TVs and other smart devices patched: turn on auto-update, check support periods, and isolate or replace devices that stop getting fixes."
sources:
  - "https://www.cisa.gov/secure-our-world/update-software"
  - "https://www.legislation.gov.uk/ukpga/2022/46"
  - "https://www.fcc.gov/CyberTrustMark"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# IoT and smart-device firmware updates

**Goal:** no device on your network running years-old firmware with public exploits.

## Inventory and settings
1. List every connected device (router client list, vendor apps). Note make, model, firmware version.
2. In each vendor app, turn on **automatic firmware updates** (often off by default on cameras, NAS units and smart TVs).
3. For devices without auto-update, add a calendar reminder to check quarterly.
4. Update the vendor app itself and the hub/bridge (Hue bridge, SmartThings hub, Home Assistant).

## Support periods
- The UK PSTI regime (in force April 2024) requires makers to publish how long a device gets security updates; look
  for it on the box or website. The US Cyber Trust Mark label signals similar commitments.
- Before buying, check the published support end date; cheap no-name devices often get none.
- When a device reaches end of support: replace it, or move it to an isolated IoT/guest network with no inbound
  access, and block its internet access if it works locally.

## Verify updates applied
The device page in the app shows the version; compare to the vendor's release notes. A device that never shows a new
version for a year is probably abandoned.

## Gotchas
- Some updates reset settings (re-enable UPnP, cloud features); recheck privacy settings afterwards.
- Do not install firmware from forums or third-party sites; only from the vendor app or official site.
- Routers are IoT too and the most important one; see the router lockdown skill.
