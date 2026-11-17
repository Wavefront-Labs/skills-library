---
id: computing-software.networking-hardware-and-wireless.f5-big-ip.software-volumes-and-upgrades
name: software-volumes-and-upgrades
category: computing-software
field: networking-hardware-and-wireless
product: f5-big-ip
tags: [networking-hardware-and-wireless, f5-big-ip, software-install, boot-locations, upgrade]
level: practitioner
status: draft
description: "Install a new BIG-IP image onto an inactive boot volume, boot into it, and roll back safely."
sources:
  - https://www.f5.com/pdf/certification/exams/blueprint-tmos-administration.pdf
  - https://techdocs.f5.com/en-us/bigip-15-1-0/big-ip-system-initial-configuration.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Software volumes, hotfixes and upgrades

BIG-IP installs to a separate boot volume (HD1.1, HD1.2 ...), so the old version stays bootable.
```
tmsh show sys software status
tmsh install sys software image BIGIP-15.1.8.iso volume HD1.2 create-volume
tmsh show sys software status          # wait for status complete
tmsh reboot volume HD1.2
tmsh switchboot volume HD1.1           # roll back
```
- Upload the ISO to `/shared/images` and verify its MD5/checksum first (`md5sum`; compare with the F5 download page).
- Upgrade the standby unit first, force it active with a planned failover, validate, then upgrade the former active. Mixed versions are only supported briefly; check the upgrade guide for the supported pairs (confirm on your version).
- Before upgrading: `tmsh save sys ucs pre-upgrade`, `tmsh run sys failover standby` only after testing, and download a qkview (`qkview`) for support.
- Config roll-forward happens at first boot of the new volume; rolling back to the old volume restores its previous config unless `cpcfg` was used to copy configuration (`tmsh install sys software ... create-volume` then `cpcfg --source=HD1.1 HD1.2`).
- Gotcha: a full `/shared` or `/var` makes the install hang at "installing".

Verify: `tmsh show sys version`, `tmsh show sys failover`, `tmsh show ltm virtual` for availability, and run the pre-saved smoke tests through the VS.
