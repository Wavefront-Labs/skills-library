---
id: computing-software.systems-network-administration.patch-management.wireless-ap-image-predownload
name: wireless-ap-image-predownload
category: computing-software
field: systems-network-administration
product: patch-management
tags: [ap-image-predownload, wireless-lan-controller, catalyst-9800, aruba, network-device-patching, patch-management]
level: practitioner
status: draft
description: "Upgrade wireless controllers and APs with image predownload: Catalyst 9800 predownload and rolling AP upgrade, Aruba cluster live upgrade, and verification."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-12/config-guide/b_wl_17_12_cg/m_predownload_ap_image.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/technical-reference/n-plus-1-rolling-ap-upgrade.html
  - https://www.arubanetworks.com/techdocs/ArubaOS-8.x-Books/810/ArubaOS-8.10.0.0-User-Guide.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Wireless AP image predownload

When a controller upgrades, every AP must download the new image. Without predownload, hundreds of APs fetch at once after the reload and stay down for 10-30 minutes.

## Cisco Catalyst 9800
1. Add the new controller image (install mode) without activating:
```text
install add file bootflash:C9800-80-universalk9_wlc.17.12.04.SPA.bin
```
2. Predownload AP images:
```text
ap image predownload
show ap image                       ! Predownload Status per AP: Complete / Initiated / Failed
```
3. Activate and commit once predownload is Complete for (nearly) all APs:
```text
install activate
install commit
```
APs swap to the predownloaded image and rejoin quickly (one AP reboot).
Alternative: **N+1 Rolling AP Upgrade** with a second controller, or **Rolling AP upgrade** on SSO pairs (`ap image upgrade destination` / percentage per iteration) to keep coverage by upgrading neighbouring APs in turns.

## Aruba (AOS 8 Mobility Conductor)
**Live Upgrade** (cluster): APs preloaded with new image by partitions, then upgraded in groups so neighbouring APs stay up; requires cluster of managed devices.

## Planning
- Check AP model support in the target release (older APs drop out of new releases).
- Branch APs over WAN: predownload hours before; rate-limit to protect WAN links (Cisco `ap image predownload` uses efficient upgrade with master APs per site in FlexConnect).

## Gotchas
- APs that fail predownload will download during activation; fix them first (flash full, unreachable).
- Mixed AP models need images for each; predownload handles them but takes longer.

## Verify
After activation all APs joined on the new version (`show ap summary`, `show ap image`), client counts back to baseline, no APs stuck downloading.
