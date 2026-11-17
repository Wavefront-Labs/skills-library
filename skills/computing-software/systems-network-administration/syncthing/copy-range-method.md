---
id: computing-software.systems-network-administration.syncthing.copy-range-method
name: copy-range-method
category: computing-software
field: systems-network-administration
product: syncthing
tags: [syncthing, copyrangemethod, copy-on-write, reflink]
level: advanced
status: docs-checked
description: "Choose Syncthing copyRangeMethod to use copy-on-write or kernel copies and speed up large local block copies."
sources: ["https://docs.syncthing.net/advanced/folder-copyrangemethod.html", "https://docs.syncthing.net/users/tuning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# copyRangeMethod

A folder setting, added in version 1.8.0, giving a choice of method for copying data between files. It can optimise copies on network filesystems, improve the speed of large copies or clone data using copy-on-write if the filesystem supports it.

## Values
- `standard` (default): reads data from the source file into application memory and writes it into the destination file (the method used before this option existed). All platforms.
- `copy_file_range`: Linux syscall, introduced in Linux 4.5. Uses copy-on-write semantics if the filesystem supports it. Some network filesystems might use it for server-side copies. The page lists it as tested on BTRFS, EXT4, XFS and ZFS (its prose mentions XFS and BTRFS).
- `ioctl`: ioctl syscall with the `FICLONERANGE` option, Linux. Tested on BTRFS. Will fail if the underlying filesystem does not support it.
- `sendfile`: the sendfile syscall, an in-kernel copy that avoids copying data into application memory. Linux and Solaris. Tested on BTRFS, XFS and EXT4.
- `duplicate_extents`: Windows Block Cloning via `FSCTL_DUPLICATE_EXTENTS_TO_FILE`. Needs Windows 10 v1607 / Windows Server 2016 or later and a compatible filesystem (ReFS, SMB 3.1.1, CsvFS); tested on ReFS. Will fail if unsupported.
- `all`: tries the methods in the order `ioctl`, `copy_file_range`, `sendfile`, `duplicate_extents`, `standard`.

```xml
<folder id="default" path="/path/to/folder">
  <copyRangeMethod>all</copyRangeMethod>
</folder>
```

## Checked
2026-11-04. Read the copyRangeMethod page, the config page (element name `copyRangeMethod`, default `standard`) and Configuration Tuning (performance note). Value list, platforms, tested filesystems, Linux 4.5, Windows requirements and the `all` order are confirmed. Removed the closing "Choosing" advice, which the pages do not state.
Method: documentation only; no commands were run.
