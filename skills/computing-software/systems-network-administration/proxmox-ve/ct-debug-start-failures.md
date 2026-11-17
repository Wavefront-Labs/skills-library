---
id: computing-software.systems-network-administration.proxmox-ve.ct-debug-start-failures
name: ct-debug-start-failures
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [lxc, lxc-start, debug-log, ct-start-fails]
level: practitioner
status: docs-checked
description: "Collect debug logs when a Proxmox VE container will not start, using pct start --debug or lxc-start in the foreground."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pct.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When `pct start` cannot start a container, gather debug output. The simplest option adds a flag:

```
pct start CTID --debug
```

Alternatively run LXC directly in the foreground and write a debug log to a file (replace CTID with the container ID):

```
lxc-start -n CTID -F -l DEBUG -o /tmp/lxc-CTID.log
```

`-F` keeps it in the foreground, so stop the container from a second terminal with `pct shutdown CTID` or `pct stop CTID`. The log is written to `/tmp/lxc-CTID.log`.

If you changed the container configuration since the last start attempt, run `pct start` at least once first. That step regenerates the configuration that `lxc-start` uses, so otherwise you debug stale settings.

Two related causes worth checking:

- Container start fails if the configured `ostype` differs from the type auto detected inside the container. Detection reads `/etc/os-release` first, then distribution release files such as `/etc/debian_version`. Setting `ostype` to `unmanaged` disables all OS specific modifications.
- To trace AppArmor denials use `dmesg | grep apparmor`. Disabling AppArmor with `lxc.apparmor.profile = unconfined` in `/etc/pve/lxc/CTID.conf` is not recommended for production.

## Checked

2026-11-09. Compared with the Obtaining Debugging Logs, Guest Operating System Configuration and AppArmor sections of https://pve.proxmox.com/pve-docs/chapter-pct.html; commands, log path, ostype behaviour and the pct start caveat all match.

Method: documentation only; no commands were run.

