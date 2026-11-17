---
id: computing-software.systems-network-administration.samba.sysvol-acls
name: sysvol-acls
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, sysvol-acls, sysvolreset, ntacl, sysvolcheck, samba-tool, sysvol]
level: advanced
status: docs-checked
description: "Check and reset SYSVOL ACLs with samba-tool ntacl sysvolcheck and sysvolreset, read and set NT ACLs on files, and handle SYSVOL replication limits."
sources:
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
  - https://wiki.samba.org/index.php/Joining_a_Samba_DC_to_an_Existing_Active_Directory
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# sysvol acls
```
samba-tool ntacl sysvolcheck
samba-tool ntacl sysvolreset
samba-tool ntacl get FILE
samba-tool ntacl set ACL FILE
```
- `sysvolcheck` compares SYSVOL ACLs with the defaults; `sysvolreset` restores them.
- The man page lists these options under `ntacl changedomsid` (run `--help` to see which apply to `ntacl set`): `--use-ntvfs`, `--service=SERVICE`, `--use-s3fs`, `--xattr-backend=[native|tdb]`, `--eadb-file`, `--recursive`, `--follow-symlinks`, `--verbose`. `ntacl getdosinfo FILE` also exists.

After joining a new DC, run `samba-tool ntacl sysvolreset`. The wiki warns it errors if SYSVOL holds non-default GPOs that have not been synced first.

Samba has no built-in SYSVOL replication; use a community rsync or Robocopy workaround.

All DCs must share the same built-in ID mappings for the SYSVOL workaround: back up `idmap.ldb` on the PDC emulator (`tdbbackup -s .bak <path>/private/idmap.ldb`), place it on the new DC as `idmap.ldb`, then run `net cache flush`. Re-sync periodically.

Backups preserve sysvol NTACLs, and restore keeps them (needs root).

## Checked

2026-11-04. Confirmed against the samba-tool(8) manual page: ntacl get/set/sysvolcheck/sysvolreset descriptions and the option list; against the Samba wiki join page: sysvolreset after join and its error with non-default GPOs, no built-in SYSVOL replication, rsync and Robocopy workarounds, idmap.ldb sync from the PDC emulator with tdbbackup and net cache flush; against the wiki restore page: NTACL preservation and root. Reattributed the option list to ntacl changedomsid and removed the unconfirmed Group Policy sentence.
Method: documentation only; no commands were run.
