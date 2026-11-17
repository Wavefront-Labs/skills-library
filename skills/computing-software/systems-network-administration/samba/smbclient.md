---
id: computing-software.systems-network-administration.samba.smbclient
name: smbclient
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, smbclient, smb-client, list-shares, smb-transfer, file-transfer]
level: intro
status: docs-checked
description: "Use smbclient to list shares, connect, run scripted commands, transfer files, tar backups, view ACLs and set options like protocol, auth file and Kerberos."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smbclient.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# smbclient
Options:
- `-L HOST` list services (`-g` parseable); `-N` no password; `-U [DOMAIN\]user[%pass]`; `-A file` auth file (restrict its permissions).
- `-c 'cmd1; cmd2'` run commands and exit (implies `-N`); `-D DIR` start directory; `-I ip`; `-p port` (default 139); `-m SMB2|SMB3|NT1` max protocol (default SMB3); `-t secs` (default 20); `-d 0-10`.
- `--use-kerberos=desired|required|off`; `--client-protection=sign|encrypt|off`; `-P` machine password; `-R "lmhosts host wins bcast"`.

Interactive commands:
- navigate: `ls`/`dir`, `cd`, `lcd`, `du`, `volume`
- transfer: `get`, `mget`, `put`, `mput`, with `prompt` and `recurse` toggles and `mask`
- manage: `mkdir`, `rmdir`, `rm`/`del`, `deltree`, `rename old new [-f]`
- info: `allinfo`, `altname`, `stat`, `getfacl` (UNIX extensions), `posix`
- Unix extras: `symlink`, `hardlink`, `chmod file octal`, `chown file uid gid`, `utimes`, `setmode file +rsha`
- tar: `tar c|x[IXbgNa]`, `tarmode`, `blocksize` (default 20)

Examples:
```
smbclient -L fileserver -N
smbclient //fileserver/share -U alice -c 'ls; get report.txt'
smbclient //mypc/myshare "" -N -Tc backup.tar users/docs
smbclient //mypc/myshare "" -N -Tx backup.tar
```
Notes from the page: `prompt` toggles per-file confirmation for `mget`/`mput`; the `mask` value is retained indefinitely, so reset it to `*` after using `mget`/`mput`.

## Checked
2026-11-04: options, defaults, interactive commands, tar flags and examples compared with the smbclient man page. Reworded the mget/mput note to what the page states.
Method: documentation only; no commands were run.
