---
id: computing-software.systems-network-administration.samba.winbind-parameters
name: winbind-parameters
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, winbind-parameters, winbind-enum, winbindd, smb-conf, daemon]
level: practitioner
status: docs-checked
description: "Tune winbind smb.conf parameters with defaults and run winbindd correctly: enum users and groups, cache time, offline logon, nested groups, daemon flags, signals."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smb.conf.5.html
  - https://www.samba.org/samba/docs/current/man-html/winbindd.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# winbind parameters
smb.conf defaults:
- `winbind enum users` / `winbind enum groups`: `no` (enumeration returns nothing).
- `winbind use default domain`: `no` (discouraged).
- `winbind offline logon`: `no`.
- `winbind cache time`: `300` seconds (not for authentication).
- `winbind refresh tickets`: `no`.
- `winbind nested groups`: `yes` (needs nss_winbind).
- `template shell`: `/bin/false`; `template homedir`: the `%D/%U` path under the home root (`/home` by default).

winbindd flags:
- `-D` daemonize; `-F` foreground (process supervisors); `-i` interactive, logs to stdout.
- `-n` disable some caching (slower, can hang if a DC is silent).
- `-d LEVEL` 0-10 (default 0); `--debug-stdout`; `--option=name=value`.
- `--no-process-group`.

Signals: `SIGHUP` reloads smb.conf, clears cached user/group info and reloads trusted domains (or use `smbcontrol`); `SIGUSR2` writes status to the log.

Files: `winbindd_cache.tdb` (cache), `winbindd_idmap.tdb` (RID mappings), pipe under `winbindd/pipe` (directory and pipe must be owned by root), `winbindd_privileged/pipe` for ntlm_auth (root group by default).

Test with `getent passwd` and `getent group`.

## Checked

2026-11-04. Confirmed against the smb.conf(5) manual page: every default in the list (including the advice to avoid winbind use default domain) and against the winbindd(8) manual page: -D, -i, -F, -n, -d (0-10, default 0), --no-process-group, SIGHUP and SIGUSR2, the pipe ownership rule, winbindd_privileged for ntlm_auth (root group by default), winbindd_idmap.tdb and winbindd_cache.tdb. The getent test is used on the Samba wiki member troubleshooting page. Made the template homedir default explicit.
Method: documentation only; no commands were run.
