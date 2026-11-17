---
id: computing-software.systems-network-administration.samba.net-idmap
name: net-idmap
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, net-idmap, idmap-dump, idmap-restore, net, winbind]
level: advanced
status: docs-checked
description: "Inspect, back up, restore, check and edit Samba ID mappings with net idmap dump, restore, get/set range and config, delete, and check, plus net cache flush."
sources:
  - https://www.samba.org/samba/docs/current/man-html/net.8.html
  - https://www.samba.org/samba/docs/current/man-html/winbindd.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# net idmap
```
net idmap dump <local tdb file>
net idmap restore [input file]
net idmap set secret <DOMAIN> <secret>
net idmap set range <RANGE> <SID> [index] [--db=DB]
net idmap set config <config> [--db=DB]
net idmap get range <SID> [index] [--db=DB]
net idmap get ranges [SID] [--db=DB]
net idmap get config [--db=DB]
net idmap delete mapping [-f] [--db=DB] <ID>
net idmap delete range [-f] [--db=DB] <RANGE>|(<SID> [INDEX])
net idmap delete ranges [-f] [--db=DB] <SID>
net idmap check [-v] [-r] [-a] [-T] [-f] [-l] [--db=DB]
```
The winbindd page says the Windows rid to UNIX id mapping is stored in `$STATEDIR/winbindd_idmap.tdb` and that it is the only place winbindd keeps these mappings, so if it is deleted or corrupted they are lost. IDs allocated by winbindd are valid only on the local machine unless a shared `idmap config * : backend` is configured. `dump` is useful for mappings produced by the idmap_tdb backend. `set secret` stores the password for the bind DN of idmap_ldap domains. The `range`, `config` and `delete range` forms act on the autorid database. `check` is read-only unless a repair option is given; `-r` is interactive, `-a` automatic, `-T` a dry run.

Related:
- `net cache flush` removes all items from the gencache.
- SIGHUP (or a reload request via smbcontrol) makes winbindd reload smb.conf and clear cached user and group information.
- `smbcontrol <dest> idmap flush [uid|gid]` flushes the sid to id caches and `idmap delete <ID>` removes one cached mapping. `net idmap delete mapping` says to use `smbcontrol all idmap ...` to notify running smbd instances.

## Checked
2026-11-04: subcommands, options and check behaviour compared with the net man page; storage file, signals and local-only IDs compared with the winbindd man page; idmap messages compared with the smbcontrol man page. Removed: a gotcha about an `idmap secret` form and a claim that cache flush is needed after an AD ID change, neither stated.
Method: documentation only; no commands were run.
