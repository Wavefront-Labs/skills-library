---
id: computing-software.networking-hardware-and-wireless.kea.forensic-logging-hook
name: forensic-logging-hook
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, hooks, libdhcp-legal-log, forensic-logging, log-rotation]
level: practitioner
status: docs-checked
description: "Record lease assignments for legal retention with libdhcp_legal_log: path, base-name, time-unit and count rotation, file naming and pre/post-rotate scripts."
sources:
  - https://kea.readthedocs.io/en/latest/arm/hooks.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# forensic logging hook
`libdhcp_legal_log.so` writes a record of lease events for jurisdictions that require them. Custom formatting can extract data from the inbound request or outbound response; use with caution, it may affect performance. Custom format cannot be used for control channel commands. The library can only be loaded by kea-dhcp4 or kea-dhcp6; when both run, the log names must be distinct.

```json
{ "library": "libdhcp_legal_log.so", "parameters": {
  "path": "/var/log/kea", "base-name": "kea-forensic4" } }
```

Text file parameters:
- `path`: directory, which must exist. Since Kea 2.7.9 legal logs may only be written to the compiled output directory (`[kea-install-dir]/var/log/kea`); override with `KEA_LEGAL_LOG_DIR`, or just omit `path`.
- `base-name`: default kea-legal.
- `time-unit`: second, day, month or year; default day.
- `count`: time units before rotation; any positive number; 0 disables rotation (a new file is created on library load). Default 1.
- `prerotate` / `postrotate`: external executable or script called with the name of the file being closed or opened; Kea does not wait for it. Scripts must be in `[kea-install-dir]/share/kea/scripts/` (override with `KEA_HOOK_SCRIPTS_PATH`).
- `mark-continuation-lines` (since Kea 3.3.0, default true): continuation lines of a multi-line record get a hyphen instead of a space after the timestamp.

File names: for day, month and year `path/base-name.CCYYMMDD.txt`; for second `path/base-name.TXXXXXXXXXXXXXXXXXXXX.txt` with seconds since the UNIX epoch. The `type` parameter can also be mysql, postgresql or syslog (absent or logfile means files).

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kea ARM hooks chapter section libdhcp_legal_log.so: Forensic Logging (file naming, parameters and defaults, 2.7.9 path rule, rotation scripts). Removed the unsupported advice to load it last. Added mark-continuation-lines and the script directory from the same section.
