---
id: computing-software.systems-network-administration.samba.vfs-fruit-time-machine
name: vfs-fruit-time-machine
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, vfs-fruit-time-machine, fruit, time-machine, macos, vfs]
level: advanced
status: docs-checked
description: "Configure vfs_fruit for macOS clients and Time Machine: module order, resource and metadata storage, encoding, time machine options and defaults."
sources:
  - https://www.samba.org/samba/docs/current/man-html/vfs_fruit.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# vfs fruit time machine
The page says fruit should be stacked with catia when character conversion is enabled and must be stacked with streams_xattr; its example uses the order `catia fruit streams_xattr`.
```
[share]
    vfs objects = catia fruit streams_xattr
    fruit:resource = file
    fruit:metadata = netatalk
    fruit:locking = netatalk
    fruit:encoding = native
```
Time Machine share (the man page has no Time Machine example; size value illustrative):
```
[timemachine]
    vfs objects = catia fruit streams_xattr
    fruit:time machine = yes
    fruit:time machine max size = 1T
```
Defaults:
- `fruit:aapl` yes (global); `fruit:nfs_aces` yes (global); `fruit:copyfile` no (global)
- `fruit:model` MacSamba (Finder icon)
- `fruit:resource` file (also `xattr`, `stream` experimental)
- `fruit:metadata` netatalk (or `stream`)
- `fruit:encoding` private (`native` needs catia)
- `fruit:time machine` no; yes advertises FULLSYNC, registers with mDNS (if built with mDNS support), forces durable handles on and kernel oplocks, kernel share modes and POSIX locking off
- `fruit:time machine max size` caps reported size from band size and count only; the volume must hold nothing else
- `fruit:locking` none
- `fruit:veto_appledouble` yes; `fruit:delete_empty_adfiles` no; `fruit:wipe_intentionally_left_blank_rfork` no
- `fruit:zero_file_id` yes; `fruit:convert_adouble` yes; `fruit:validate_afpinfo` yes

mDNS setup is not covered here; the page says `fruit:time machine = yes` registers the share with mDNS if Samba is built with mDNS support.

## Checked
2026-11-04: example, global and per-share options, defaults and Time Machine behaviour compared with the vfs_fruit man page. Nothing removed beyond the module-order wording.
Method: documentation only; no commands were run.
