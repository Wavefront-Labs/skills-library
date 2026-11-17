---
id: computing-software.systems-network-administration.cisco-networking.wlan-creation-catalyst-9800
name: wlan-creation-catalyst-9800
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, wlc, catalyst-9800, wireless-lan-controller, wlan-configuration, wlan-profile, policy-profile, policy-tag, wpa2-psk, wpa3, 802-1x, ssid, client-vlan, wlan-gui]
level: practitioner
status: draft
description: "Create a WLAN end to end on a Catalyst 9800: WLAN profile and security, policy profile with VLAN, policy tag mapping, applying tags to APs, PSK and 802.1X variants, verification."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/technical-reference/c9800-config-model.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg/m_wlan_wlan_9800.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Creating a WLAN on a Catalyst 9800 (CCNA 2.9 / 5.10)

Three objects: **WLAN profile** (SSID + security), **policy profile** (VLAN, switching,
ACL/QoS), joined in a **policy tag** that is applied to APs. GUI path: Configuration >
Tags & Profiles. CLI equivalent below.

## WPA2/WPA3 PSK (staff devices, IoT)
```
wlan CORP-PSK 2 CORP-PSK               ! profile-name, WLAN ID, SSID
 no security wpa akm dot1x
 security wpa akm psk
 security wpa psk set-key ascii 0 <PASSPHRASE>
 security wpa wpa2 ciphers aes          ! default
 no shutdown
```
WPA3 transition: add `security wpa wpa3` + `security wpa akm sae` (and `security pmf optional`);
WPA3-only requires `pmf mandatory`.

## 802.1X enterprise
```
aaa new-model
radius server ISE1
 address ipv4 10.1.1.20 auth-port 1812 acct-port 1813
 key <RADIUS_SECRET>
aaa group server radius ISE-GROUP
 server name ISE1
aaa authentication dot1x ISE-AUTH group ISE-GROUP
wlan CORP 3 CORP
 security dot1x authentication-list ISE-AUTH     ! default akm is dot1x
 no shutdown
```

## Policy profile and tag
```
wireless profile policy CORP-POLICY
 vlan 20                     ! or a VLAN name/group
 no shutdown
wireless tag policy HQ-POLICY-TAG
 wlan CORP-PSK policy CORP-POLICY
 wlan CORP policy CORP-POLICY
ap 00a1.b2c3.d4e5
 policy-tag HQ-POLICY-TAG    ! or tag by AP name regex / bulk via the GUI tag wizard
```
APs keep `default-policy-tag` (which only maps nothing in recent releases) until retagged.

## Verify
```
show wlan summary
show wireless tag policy detailed HQ-POLICY-TAG
show ap tag summary
show wireless client summary
show wireless client mac-address <MAC> detail     ! VLAN, policy profile, auth state
```

## Gotchas
- Policy profiles and WLANs ship `shutdown`; forgetting `no shutdown` = SSID not broadcast.
- Retagging an AP makes it rejoin (short outage).
- The WLAN ID must be unique; IDs above 16 are not broadcast on some AP models' radios.
- VLAN must exist on the WLC (central switching) or at the AP's switch (FlexConnect local).

## Verify
- [ ] SSID visible from a client; client gets an IP in the intended VLAN.
- [ ] `show wireless client ... detail` shows Run state and the right policy profile.
