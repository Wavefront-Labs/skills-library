---
id: computing-software.systems-network-administration.cisco-networking.wlc-ap-image-predownload-rolling-upgrade
name: wlc-ap-image-predownload-rolling-upgrade
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-wireless, catalyst-9800, ap-image-predownload, rolling-ap-upgrade, n-plus-one-upgrade, ap-upgrade, wlc-upgrade, efficient-ap-join]
level: practitioner
status: draft
description: "Upgrade a Catalyst 9800 and its APs with minimal outage: AP image predownload, Rolling AP Upgrade (N+1 / ISSU) and verifying APs on the new image."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg/m_predownloading_image_ap.html
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/17-9/config-guide/b_wl_17_9_cg/m_n1_rolling_ap_upgrade.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AP image predownload and Rolling AP Upgrade

## Problem
When a WLC reboots onto a new release, every AP must download the matching image before it can
join; hundreds of APs downloading over WAN links means long outages.

## Predownload (single controller)
```
install add file bootflash:C9800-80-universalk9_wlc.17.09.05.SPA.bin
ap image predownload               ! push the new AP image to APs while they keep serving
show ap image                      ! Predownload Status: Complete/Initiated/Failed per AP
install activate                   ! WLC reboots; APs swap images and rejoin faster
install commit
```
Predownload runs in the background; control concurrency with `ap upgrade staggered` settings
on some releases. Over WAN, use **FlexConnect Efficient AP Image Upgrade** (one master AP per
site model downloads and shares with peers).

## Rolling AP Upgrade
Used with N+1 (APs moved to a second WLC) or HA SSO ISSU: APs are rebooted in batches chosen
by RRM neighbour data so neighbouring APs keep coverage.
```
ap image upgrade destination <WLC2-NAME> <WLC2-IP>   ! N+1 rolling upgrade
ap image upgrade percentage 15                         ! batch size 5/15/25%
show ap upgrade
```

## Gotchas
- Flash space on old AP models; predownload fails silently for some. Check `show ap image` for failures.
- APs on unsupported models for the new release never join. Check the compatibility matrix first.
- Keep the old release in bootflash until all APs have joined and are stable.
- Changes to AP join profiles mid-upgrade complicate rollback; freeze config.

## Verify
- [ ] `show ap image` all APs predownloaded before `install activate`.
- [ ] After activation, `show ap summary` count matches pre-upgrade count; `show ap uptime` reasonable.
