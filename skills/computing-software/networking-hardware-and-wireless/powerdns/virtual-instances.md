---
id: computing-software.networking-hardware-and-wireless.powerdns.virtual-instances
name: virtual-instances
category: computing-software
field: networking-hardware-and-wireless
product: powerdns
tags: [powerdns, virtual-instances, config-name, systemd, sysv, pdns-at-name]
level: practitioner
status: docs-checked
description: "Run several PowerDNS Authoritative instances on one host with pdns-NAME.conf, config-name, systemd pdns@NAME or SysV symlinks."
sources:
  - https://raw.githubusercontent.com/PowerDNS/pdns/master/docs/guides/virtual-instances.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Virtual instances

Use when instances must be separated, for example to isolate customers' zones.

1. Create `pdns-NAME.conf` in the configuration directory (usually `/etc/powerdns`).

systemd:
```
systemctl start pdns@myinstance.service
systemctl enable pdns@myinstance.service
```
with `pdns-myinstance.conf` already present.

SysV init:
1. Symlink the `pdns` init script to `pdns-NAME`.
2. The script runs the binary with `config-name` set to `NAME`, so `pdns-NAME.conf` is loaded instead of `pdns.conf`.
3. The PID file is `pdns-NAME.pid` in `socket-dir`.

Caveats (SysV):
- `NAME` must not contain a hyphen; it confuses the script.
- The init.d `force-stop` action kills every PowerDNS instance, not only one.

## Checked

2026-11-08. Read in full: PowerDNS docs guides/virtual-instances.rst. Confirmed the pdns-NAME.conf file, config-name option, pid file in socket-dir, the hyphen warning, the force-stop warning and the systemctl pdns@NAME commands. Nothing removed.

Method: documentation only; no commands were run.
