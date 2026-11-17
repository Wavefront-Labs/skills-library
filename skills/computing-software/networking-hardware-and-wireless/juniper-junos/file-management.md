---
id: computing-software.networking-hardware-and-wireless.juniper-junos.file-management
name: file-management
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, file-management, request-system-snapshot, file-copy, storage]
level: practitioner
status: draft
description: "Browse, copy and clean the Junos file system and take system snapshots and configuration archives."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# File management and storage
Goal: manage logs, images and backups from the CLI.

```
user@host> file list /var/tmp detail
user@host> file copy /config/juniper.conf.gz scp://backup@192.0.2.70/backups/edge1.conf.gz
user@host> file show /var/log/messages | last 20
user@host> request system storage cleanup
user@host> request system snapshot
user@host> show system storage
```

```
set system archival configuration transfer-on-commit
set system archival configuration archive-sites "scp://backup@192.0.2.70/configs/" password "<redacted>"
```

- `/config` holds juniper.conf and rolling backups; `/var/tmp` is scratch; `/var/log` logs.
- `request system storage cleanup` proposes deleting old logs/images and asks for confirmation.
- `request system snapshot` writes the running OS to the alternate media so it can boot if primary fails (platform specific; confirm on your hardware).

Gotcha: a full `/var` makes commits and log writes fail. Check `show system storage` before upgrades and clean up first.

Operational tip: schedule a recurring `request system storage cleanup` review, and store configuration archives on a server with its own retention policy so a device failure never takes the only backup with it.

## Verify
- `show system archival` shows last transfer successful after a commit.
