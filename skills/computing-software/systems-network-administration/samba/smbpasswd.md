---
id: computing-software.systems-network-administration.samba.smbpasswd
name: smbpasswd
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, smbpasswd, samba-password, smb-password, local-account, passdb]
level: intro
status: docs-checked
description: "Manage local Samba passwords with smbpasswd: add, delete, disable, enable users, scripted input, remote password change, and the null-password and machine flags."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smbpasswd.8.html
  - https://wiki.samba.org/index.php/Setting_up_Samba_as_a_Standalone_Server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# smbpasswd
Root-only options:
- `-a user` add (acts as a password change if present)
- `-x user` delete
- `-d user` disable (writes a `D` flag)
- `-e user` enable
- `-n user` blank password; requires `null passwords = yes` in `[global]`
- `-m` machine account; `-i` interdomain trust account

Any user:
- no args: change your own password
- `-r REMOTE_MACHINE [-U user]`: change on a remote SMB server (default is local host)
- `-s`: silent; read old and new passwords from stdin for scripts
- `-c /path/to/smb.conf`; `-D 0-10` debug (default 0); `-R ORDER` name resolve order
- `-w password` / `-W`: store the `ldap admin dn` password in `secrets.tdb` (LDAP builds)

Examples:
```
sudo smbpasswd -a bob
sudo smbpasswd -d bob
sudo smbpasswd -e bob
smbpasswd -r fileserver -U alice
```
The default passdb backends need the user to exist in the system password file before `-a`. The standalone-server wiki page says Samba uses the `tdbsam` backend by default, stored in `passdb.tdb`, and denies access if the account is disabled locally.

`-d`/`-e` fail on old-format smbpasswd files (no room for the flag).

## Checked
2026-11-04: root-only and any-user options, defaults and the null-password rule compared with the smbpasswd man page; tdbsam default and local-disable behaviour compared with the Standalone Server wiki page. Removed: a pdbedit pointer the page does not state.
Method: documentation only; no commands were run.
