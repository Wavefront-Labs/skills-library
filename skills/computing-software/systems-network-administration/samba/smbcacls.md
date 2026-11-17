---
id: computing-software.systems-network-administration.samba.smbcacls
name: smbcacls
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, smbcacls, nt-acl, acl-editing, propagate-inheritance, acl]
level: advanced
status: docs-checked
description: "Read and edit NT ACLs on SMB shares with smbcacls: add, modify, delete and set ACEs, ACL string format and flags, chown, inheritance and tree propagation."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smbcacls.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# smbcacls
Usage: `smbcacls //server/share /path [options]`.

Options:
- `-a|--add acl`: add ACEs, existing ones untouched.
- `-M|--modify acl`: change masks of ACEs that exist.
- `-D|--delete acl`: remove ACEs.
- `-S|--set acl`: replace the whole ACL (needs revision, owner, group, ACEs).
- `-C|--chown name`, `-G|--chgrp name`.
- `-I|--inherit allow|remove|copy`.
- `--propagate-inheritance`: push ACEs down a tree by their inheritance flags.
- `--numeric`: show raw SIDs and masks.
- `-t|--test-args`: validate without changing.
- `-n NETBIOSNAME`, `-R|--name-resolve ORDER`.

ACL string:
```
REVISION:1
OWNER:<sid or name>
GROUP:<sid or name>
ACL:<sid or name>:<ALLOWED|DENIED>/<flags>/<mask>
```
Flags (decimal, hex, or the aliases in parentheses, separated by `|`): `(OI)` 0x1, `(CI)` 0x2, `(NP)` 0x4, `(IO)` 0x8, `(I)` 0x10. Mask: decimal or hex number, or letters `R W X D P O`; aliases `READ` (RX), `CHANGE` (RXWD), `FULL` (RWXDPO).

Examples:
```
smbcacls //server/share /dir -a "ACL:alice:ALLOWED/(OI)|(CI)/READ"
smbcacls //server/share /dir -M "ACL:bob:DENIED/0/W"
smbcacls //server/share /parent -a "ACL:alice:ALLOWED/(OI)|(CI)/READ" --propagate-inheritance
smbcacls //server/share /dir -I remove
```
Add `-U user` for credentials. Gotcha: `-M` and `-D` print an error for each ACE that is not already in the ACL.

## Checked

2026-11-04. Confirmed against the smbcacls(1) manual page: all options listed, -S requirements, ACL string format, type ALLOWED/DENIED, flag values and the parenthesised alias form, mask letters and READ/CHANGE/FULL aliases, --propagate-inheritance, -n and -R. Changed the flag aliases and examples to the page's (XX) form, corrected the error gotcha (the page says -M and -D, not -a), and removed the unconfirmed no-option-prints-ACL claim.
Method: documentation only; no commands were run.
