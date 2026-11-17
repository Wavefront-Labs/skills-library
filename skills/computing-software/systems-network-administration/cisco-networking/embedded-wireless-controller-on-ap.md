---
id: computing-software.systems-network-administration.cisco-networking.embedded-wireless-controller-on-ap
name: embedded-wireless-controller-on-ap
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-wireless, catalyst-9800, embedded-wireless-controller, ewc, mobility-express, catalyst-9100, controller-on-ap]
level: practitioner
status: draft
description: "Deploy the Catalyst 9800 Embedded Wireless Controller on a Catalyst 9100 AP: limits, conversion, primary/standby election and when to use a real WLC."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/ewc/b_c9800_wireless_controller_ewc_cg_17_9.html
  - https://www.cisco.com/c/en/us/products/collateral/wireless/embedded-wireless-controller-on-catalyst-access-points/nb-06-embed-wirel-cont-cat-ap-faq-ctp-en.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Embedded Wireless Controller (EWC) on Catalyst APs

## What it is
EWC runs the Catalyst 9800 controller code as a container on a Catalyst 9100 AP (9115/9120/9130 etc.).
One AP is the active controller and also serves clients; others join it via CAPWAP. Successor to
Mobility Express on Aironet APs.

## Limits (check the data sheet for your release)
- Roughly 50-100 APs and 1000-2000 clients depending on the controller-capable AP model.
- FlexConnect local switching only (no central switching of client data).
- No N+1 or SSO across sites; standby is another EWC-capable AP on the same subnet.
- Fewer features than an appliance WLC (no anchor/foreign guest tunnelling on many releases).

## Bring-up
1. Factory AP with EWC image boots and broadcasts a provisioning SSID `CiscoAirProvision`
   (or use the console Day 0 wizard / Cisco Wireless app).
2. Set management IP, admin user, country, NTP and the first WLAN.
3. Other APs on the same L2 discover the EWC via CAPWAP broadcast or DHCP option 43.
4. Election: a configured preferred active (`wireless ewc-ap preferred-master <AP-NAME>`) wins;
   otherwise the most capable AP model, then lowest MAC. A second capable AP becomes standby.
```
show wireless summary
show ap summary
show ap config general | include Image
```

## Converting
- CAPWAP AP to EWC (AP CLI): `ap-type ewc-ap tftp://<SERVER>/<AP-IMAGE> tftp://<SERVER>/<EWC-IMAGE>`.
- EWC to CAPWAP (when you outgrow it): `ap-type capwap` on each AP, then point to an appliance WLC.

## Gotchas
- All APs must run images compatible with the EWC release; mismatched models download from the
  image server you configure.
- The active AP reboots = controller failover = brief client disruption; place EWC APs where
  they will not be power-cycled casually.

## Verify
- [ ] `show wireless summary` lists active and standby EWC.
- [ ] Pull power on the active AP: standby takes over and APs rejoin.
