---
id: computing-software.cloud-infrastructure-engineering.netdata.journald-retention
name: journald-retention
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, journald-conf, log-retention, wevtutil]
level: practitioner
status: docs-checked
description: "Set log retention for logs Netdata reads: systemd-journal limits in journald.conf, journal-remote limits and the Windows Event Log size and retention flags."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/logs/log-storage-and-retention.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
systemd journal, `/etc/systemd/journald.conf`:

```
Storage=persistent
SystemMaxUse=
SystemKeepFree=
SystemMaxFileSize=
SystemMaxFiles=
MaxRetentionSec=
MaxFileSec=
```

Documented defaults: `SystemMaxUse` 10% of filesystem (max 4G), `SystemKeepFree` 15% (max 4G), `SystemMaxFileSize` 1/8 of SystemMaxUse (max 128M), `SystemMaxFiles` 100, `MaxRetentionSec` 0 (off), `MaxFileSec` 1 month.

Apply: `systemctl restart systemd-journald` (first `systemctl kill --signal=SIGUSR1 systemd-journald` to flush volatile entries). Verify: `journalctl --disk-usage`.

Gotchas:
- Volatile storage (`/run/log/journal`) is lost on reboot; set `Storage=persistent` on nodes whose logs must survive a reboot.
- Time-based deletion is off by default; set `MaxRetentionSec=`.
- The smaller of `SystemMaxUse=` and `SystemKeepFree=` wins.
- Journal files take roughly the raw log text size.
- Namespaces use `/etc/systemd/journald@NAMESPACE.conf`; centralization points use `[Remote]` in `/etc/systemd/journal-remote.conf` (`MaxUse=`, `KeepFree=`, `MaxFileSize=`, `MaxFiles=`, `SplitMode=`).

Windows Event Log:

```
wevtutil sl Application /ms:1073741824 /rt:false
```

`/ms` max bytes (minimum 1048576, multiples of 64 KB); `/rt:false` overwrites oldest; `/rt:true` discards new events; `/ab:true` archives when full and requires `/rt:true`.

## Checked

2026-11-04. Confirmed against the Netdata Log Storage and Retention page: the journald option defaults, restart and SIGUSR1 flush, `journalctl --disk-usage`, the smaller-limit rule, the size planning rule, namespace and journal-remote configuration, and the wevtutil flags. Reworded the Storage gotcha: the page does not say volatile is the default.

Method: documentation only; no commands were run.
