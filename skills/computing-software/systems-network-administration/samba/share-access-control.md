---
id: computing-software.systems-network-administration.samba.share-access-control
name: share-access-control
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, share-access-control, valid-users, hosts-allow, guest-ok, smb-conf]
level: practitioner
status: docs-checked
description: "Control who can reach a Samba share: valid and invalid users, read and write lists, hosts allow and deny, admin users, guest settings, read only, browseable."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# share access control
Defaults from smb.conf(5):
- `read only`: `yes`; `writeable` is the inverted synonym (`no`).
- `valid users`: no list (anyone may log in); entries also in `invalid users` are denied.
- `invalid users`: none; supports `@group`, `+`, `&` prefixes and `%S`. Example `root fred admin @wheel`.
- `read list`: users or `@groups` forced read-only (`mary, @students`).
- `write list`: users or groups with write access regardless of `read only` (`admin, root, @staff`).
- `admin users`: empty; listed users act as root on the share.
- `hosts allow`: none (all hosts permitted); localhost always allowed unless denied. Example `150.203.5. myhost.mynet.edu.au`.
- `hosts deny`: none; where lists conflict, `hosts allow` takes precedence.
- `guest ok` (synonym `public`): `no`; `guest only`: `no` and needs `guest ok`; `guest account`: `nobody`.
- `browseable`: `yes`; `access based share enum`: `no`; `max connections`: `0` (unlimited).
- `follow symlinks`: `yes`.
- `map to guest`: `Never`; `Bad User` maps unknown users to guest.
- `restrict anonymous`: `0` (1 blocks anonymous SAMR; 2 also blocks IPC$).

Example:
```
[Demo]
   path = /srv/samba/Demo/
   read only = no
   valid users = +SAMDOM\"Domain Users"
   hosts allow = 127.0.0.1 10.99.0.0/24
```
Verify with `testparm -s` and `testparm --parameter-name="hosts allow"`; `testparm configfile hostname hostIP` checks hosts allow/deny.

## Checked

2026-11-04. Confirmed against the smb.conf(5) manual page: every default and example listed above, the read only/writeable inverted synonym, public as synonym of guest ok, guest only needing guest ok, admin users acting as root, localhost always allowed, hosts allow precedence, the + and & prefixes and %S, and restrict anonymous levels 1 and 2. The share example is illustrative; the testparm hostname form is confirmed on the testparm(1) page.
Method: documentation only; no commands were run.
