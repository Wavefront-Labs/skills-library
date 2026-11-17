---
id: computing-software.systems-network-administration.glusterfs.mandatory-locks
name: mandatory-locks
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, mandatory-locks, locks, locking, smb]
level: sme
status: docs-checked
description: "Set GlusterFS locks.mandatory-locking to off, file, forced or optimal, what each mode does, and the known caveats with performance translators."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Mandatory-Locks.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mandatory locks

```
gluster volume set <VOLNAME> locks.mandatory-locking <off / file / forced / optimal>
```

Modes:

- `off`: disabled; the default.
- `file`: Linux kernel-style mandatory locking via mode bits; described as not well tested.
- `forced`: checks for conflicting byte-range locks on every data-modifying operation.
- `optimal`: POSIX clients keep advisory-lock semantics, while mandatory locks taken by other clients such as SMB are still honoured.

Caveats:

- Option changes take effect only after the volume is subsequently started or restarted.
- For full functionality in any mode, turn off the performance translators: client-side translators can return early success to open, read and write calls, which undermines mandatory locks because the locks translator runs on the server (Bugzilla 1194546).
- A race window exists between mandatory locks and in-flight reads and writes (Bugzilla 1287099).

## Checked

2026-11-04. Confirmed against the glusterdocs Mandatory Locks page: the option and its four values, off by default, the meaning of each mode, restart requirement, the advice to turn off performance translators and both Bugzilla references. Nothing removed.

Method: documentation only; no commands were run.
