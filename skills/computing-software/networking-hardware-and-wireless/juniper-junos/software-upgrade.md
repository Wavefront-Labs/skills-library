---
id: computing-software.networking-hardware-and-wireless.juniper-junos.software-upgrade
name: software-upgrade
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, software-upgrade, request-system-software-add, validate, junos-image]
level: practitioner
status: draft
description: "Upgrade Junos safely with validate, request system software add, reboot and rollback of the previous image."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Junos software upgrade
Goal: upgrade with a tested rollback path.

```
user@host> show version
user@host> file copy scp://admin@192.0.2.70/images/junos-install.tgz /var/tmp/
user@host> request system software validate /var/tmp/junos-install.tgz
user@host> request system software add /var/tmp/junos-install.tgz reboot
user@host> request system snapshot
user@host> request system software rollback
```

- Dual-RE: upgrade the backup RE first with `request system software add ... re1`, switch mastership, then upgrade the other (confirm exact steps in the release notes for your platform).
- ISSU/NSSU (`request system software in-service-upgrade` / `nonstop-upgrade`) need GRES and NSR set up; support varies by platform and release: confirm.
- `request system software delete-backup` frees space.

Gotcha: read the release notes for required intermediate versions and package name (`jinstall`, `junos-install`, `-limited`/`-signed`). Installing the wrong package type fails validation, or in worse cases boots without features.

Operational tip: take a configuration backup and `request system snapshot` before starting, schedule a maintenance window with console access, and check the vendor's known-issues list for the target release.

## Verify
- `show version` shows the target release on all REs.
- `show system alarms` and `show chassis alarms` are clear.
