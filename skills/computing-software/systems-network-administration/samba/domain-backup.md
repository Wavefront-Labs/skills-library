---
id: computing-software.systems-network-administration.samba.domain-backup
name: domain-backup
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, domain-backup, backup-online, backup-offline, samba-tool, active-directory]
level: practitioner
status: docs-checked
description: "Back up a Samba AD domain with samba-tool domain backup online or offline, what the tar.bz2 contains and omits, and checks to run first."
sources:
  - https://wiki.samba.org/index.php/Back_up_and_Restoring_a_Samba_AD_DC
  - https://www.samba.org/samba/docs/current/man-html/samba-tool.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# domain backup
Online (clones a running DC's database; local or remote):
`sudo samba-tool domain backup online --targetdir=<output-dir> --server=<DC-server> -UAdministrator`
Remote runs also need `--configfile` so the right smb.conf settings are included.

Offline (copies local files; DC need not stop; needs Samba 4.10+ and the lmdb-utils package):
`sudo samba-tool domain backup offline --targetdir=<output-dir>`

`domain backup rename` produces a backup with the domain renamed, intended only as a temporary replacement (see the wiki's Domain rename tool page).

What you get: one `.tar.bz2` covering the whole domain from a single DC, with a `backup.txt`. Offline backups also include local replication metadata. A local run includes smb.conf. Sysvol files are saved with NTACLs.

Not included: per-server data such as `private/tls` certificates (regenerate); `bind-dns/` is empty.

Rules:
- Run as root (NTACL handling).
- Run `samba-tool dbcheck` first; problems carry into the backup.
- The archive holds all domain secrets; protect it.
- It is a whole-domain backup, not a way to recover one DC (rejoin instead).
- Windows DCs usually fail on sysvol because of the DFSR lock.

Restore: see domain-restore.

## Checked
2026-11-04: online and offline commands and requirements, archive contents, omissions and the rules compared with the Back up and Restoring a Samba AD DC wiki page. Nothing removed.
Method: documentation only; no commands were run.
