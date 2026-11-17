---
id: computing-software.systems-network-administration.samba.smbcontrol-reload
name: smbcontrol-reload
category: computing-software
field: systems-network-administration
product: samba
tags: [systems-network-administration, samba, smbcontrol-reload, smbcontrol, reload-config, daemons, smbd]
level: practitioner
status: docs-checked
description: "Send runtime messages to Samba daemons with smbcontrol: reload-config, debug, ping, close-share, kill-client-ip, num-children, shutdown, plus smbd signals."
sources:
  - https://www.samba.org/samba/docs/current/man-html/smbcontrol.1.html
  - https://www.samba.org/samba/docs/current/man-html/smbd.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# smbcontrol reload
Destinations: `smbd`, `nmbd`, `winbindd`, `all` (every running daemon), or a PID.

```
smbcontrol smbd reload-config
smbcontrol all reload-config
smbcontrol smbd debug 3
smbcontrol smbd ping 3
smbcontrol smbd close-share public
smbcontrol smbd close-share '*'
smbcontrol smbd kill-client-ip 192.168.1.50
smbcontrol smbd num-children
smbcontrol smbd profile count        # on|off|count|flush
smbcontrol nmbd shutdown
smbcontrol nmbd force-election
smbcontrol smbd reload-printers
```
Also `printnotify`, `drvupgrade`, `idmap flush|delete|kill`, `pool-usage`, `ringbuf-log` (needs `logging = ringbuf`), and `reload-certs` (to `ldap_server` on an AD DC).

smbd reloads smb.conf and includes automatically every 3 minutes when they change; force it with SIGHUP or `smbcontrol`. Reload does not affect existing connections: users must reconnect or smbd must restart. Stop smbd with SIGTERM, not SIGKILL.

`close-share` closes client connections to the named share (or all shares with `*`), and `kill-client-ip` closes connections from one IP address. `close-denied-share` leaves users who are still allowed connected.

## Checked
2026-11-04: destinations, message types, parameters, reload timing and signals compared with the smbcontrol and smbd man pages. Removed: an unsaved-data warning the pages do not state.
Method: documentation only; no commands were run.
