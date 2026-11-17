---
id: computing-software.systems-network-administration.glusterfs.start-stop-glusterd
name: start-stop-glusterd
category: computing-software
field: systems-network-administration
product: glusterfs
tags: [glusterfs, glusterd, systemctl, daemon, init-script]
level: intro
status: docs-checked
description: "Start, stop and enable the glusterd management daemon with systemd or init scripts, including on-boot enablement on Red Hat, Debian and other systems."
sources:
  - https://raw.githubusercontent.com/gluster/glusterdocs/master/docs/Administrator-Guide/Start-Stop-Daemon.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Start and stop glusterd

glusterd is the Gluster elastic volume manager. It oversees the glusterfs processes and coordinates volume operations across storage servers. It must be started on all GlusterFS servers after installation.

Systemd systems:

```
systemctl start glusterd
systemctl stop glusterd
```

Systems without systemd:

```
/etc/init.d/glusterd start
/etc/init.d/glusterd stop
```

## Start at boot

Systemd: enable and start in one step, or disable and stop:

```
systemctl enable --now glusterd
systemctl disable --now glusterd
```

Without systemd:

- Red Hat and Fedora: `chkconfig glusterd on`
- Debian and Ubuntu: `update-rc.d glusterd defaults`
- Other systems: append `glusterd` to `/etc/rc.local` (`echo "glusterd" >> /etc/rc.local`)

## Checked

2026-11-04: every command and distribution split was read against the glusterdocs page Start-Stop-Daemon (Managing the glusterd Service), including the note that glusterd must be started on all servers. Nothing removed.

Method: documentation only; no commands were run.
