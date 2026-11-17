---
id: computing-software.systems-network-administration.samba.vfs-full-audit
name: vfs-full-audit
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, vfs-full-audit, full-audit, audit-log, audit, vfs, syslog]
level: advanced
status: docs-checked
description: "Audit Samba file operations with vfs_full_audit and the simpler vfs_audit: prefix, success and failure operation lists, syslog facility and priority, defaults."
sources:
  - https://www.samba.org/samba/docs/current/man-html/vfs_full_audit.8.html
  - https://www.samba.org/samba/docs/current/man-html/vfs_audit.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vfs full audit
Example:
```
[records]
    path = /data/records
    vfs objects = full_audit
    full_audit:prefix = %u|%I
    full_audit:success = open opendir
    full_audit:failure = all !open
    full_audit:facility = LOCAL7
    full_audit:priority = ALERT
```
Options:
- `full_audit:prefix`: default `%u|%I`; smb.conf substitutions apply.
- `full_audit:success` / `full_audit:failure`: operations to log; default none; `all` and `none` are special; prefix `!` to unset.
- `full_audit:facility`, `full_audit:priority`: syslog(3) names; no default.
- `full_audit:syslog`: default `true`; `false` logs at debug level 1 instead.
- `full_audit:log_secdesc`: default `false`; true logs the SDDL of ACLs clients set.

Record format: `smbd_audit: PREFIX|OPERATION|RESULT|FILE`. An unknown operation name makes the module fail to load, and clients are refused on that share.

Simple alternative, `vfs_audit`, logs connect, disconnect, opendir, mkdir, rmdir, open, close, rename, unlink, chmod and fchmod:
```
[global]
vfs objects = audit
audit:facility = LOCAL1
audit:priority = NOTICE
```

## Checked

2026-11-04. Confirmed against the vfs_full_audit(8) and vfs_audit(8) manual pages: all options and defaults, the all/none special names, the record format, the unknown-operation failure, the full_audit example, the vfs_audit operation list and its example. Removed the generic syslog routing advice (not on the pages).
Method: documentation only; no commands were run.
