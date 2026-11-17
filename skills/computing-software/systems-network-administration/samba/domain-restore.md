---
id: computing-software.systems-network-administration.samba.domain-restore
name: domain-restore
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, domain-restore, backup-restore, newservername, samba-tool, disaster-recovery]
level: advanced
status: docs-checked
description: "Restore a Samba AD domain from a samba-tool domain backup file onto a new DC, start it, rejoin old DCs, and avoid the documented restore pitfalls."
sources:
  - https://wiki.samba.org/index.php/Back_up_and_Restoring_a_Samba_AD_DC
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# domain restore
```
sudo samba-tool domain backup restore --backup-file=<tar-file> --newservername=<DC-name> --targetdir=<new-samba-dir>
```
Optional: `--site` (put the DC in a non-default site), `--host-ip` (fix errors from an smb.conf `interfaces` setting that does not match the new server; mainly rename backups), `--debug=3`.

Start: `samba -s <targetdir>/etc/smb.conf`

Order of operations:
1. Stop samba on all old DCs (skip for rename backups).
2. Restore on one new DC.
3. Start samba there.
4. Rejoin each old DC: `samba-tool domain join <dns-realm> DC --server=<restored-dc>`.
5. For rename backups, repoint appliances to the new domain.

Safest pattern: restore onto a temporary DC, rejoin the originals one at a time, then remove the temporary DC with `samba-tool domain demote`.

Cautions:
- Run as root; target directory must be empty or absent.
- `--newservername` must not already exist in the domain.
- Never run samba on a restored copy while it can reach production.
- An untarred backup cannot run samba; use the restore command.
- DNS restores to internal DNS; use `samba_upgradedns` for DLZ.
- If backing up a brand new DC fails with a list index out of range error (no RID allocated yet), add a temporary user to force RID allocation.
- Non-root online backups may restore but fail to start.

## Checked

2026-11-04. Confirmed against the Samba wiki page Back up and Restoring a Samba AD DC: restore command and options, start with -s, order of operations, temporary-DC pattern with domain demote, root requirement, empty targetdir, newservername conflict, --host-ip scope, untarred backup limits, internal DNS and samba_upgradedns, non-root online backups. Corrected the RID index-error line (it applies when backing up a brand new DC).
Method: documentation only; no commands were run.
