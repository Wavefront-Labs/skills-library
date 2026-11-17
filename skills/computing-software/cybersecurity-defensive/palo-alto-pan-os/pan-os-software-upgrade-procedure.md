---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-software-upgrade-procedure
name: pan-os-software-upgrade-procedure
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [pan-os-upgrade, pan-os, software-upgrade, upgrade-path, preferred-release, ha-upgrade, rollback-version]
level: practitioner
status: draft
description: "Upgrade PAN-OS safely - check upgrade path, download, install, restart, HA ordering and rollback - on firewalls and Panorama."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-upgrade"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: move to a supported release without outage or lost config.

Pre-checks
- Read release notes and the upgrade/downgrade considerations; check Panorama and managed firewall version compatibility (Panorama must be same or newer).
- Export config: `save config to pre-upgrade.xml` and export it off-box.
- Content version minimum for the target.
- Upgrade path: you generally must pass through the major (x.0) base image before a later maintenance release in a new major. Check the listed path (confirm).

```
request system software check
request system software download version 11.1.0
request system software install version 11.1.0
request restart system
show jobs all
show system info | match sw-version
```

HA pair: upgrade the passive first (suspend the active temporarily if preempt causes surprises), verify state, fail over, then upgrade the other. Keep the same version only briefly; mismatch is tolerated during the process but not long term.

Gotchas
- Downloading latest first can skip a required base image; download each in order.
- Disk space: delete old images (`delete software version <x>`) if the download fails for space.
- Plugin and content compatibility for Panorama managed firewalls.
- Rollback is installing the previous image from the same menu; configs saved on a newer version may not load on an older one.

## Verify
```
show system info
show high-availability state
show jobs all
```
New version listed, HA peers healthy, and traffic/GlobalProtect/VPN counters recovering.
