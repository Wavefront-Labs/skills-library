---
id: computing-software.systems-network-administration.linux.service-minimisation-attack-surface
name: service-minimisation-attack-surface
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, service-minimisation, attack-surface, systemctl-mask, listening-services, unneeded-packages, hardening, cis-benchmark, security, sysadmin]
level: practitioner
status: draft
description: "Reduce a Linux host's attack surface: inventory listening and enabled services, map them to packages, disable or mask and then remove what isn't needed, and keep it that way."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemctl.html
  - https://www.cisecurity.org/cis-benchmarks
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/security_hardening/index
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Service minimisation

**Goal:** a host runs and exposes only what its role requires — fewer packages to patch,
fewer ports to defend.

## 1. Inventory
```bash
ss -tulpn                                              # what listens, on which address, which process
systemctl list-unit-files --state=enabled --type=service,socket,timer
systemctl list-units --type=service --state=running
rpm -qf $(readlink -f /proc/<PID>/exe)                 # Debian: dpkg -S <path> — map process → package
dnf repoquery --userinstalled | wc -l                  # apt-mark showmanual — what was explicitly installed
```
Write down the role ("nginx reverse proxy + node_exporter") and justify every listener and enabled unit against it.

## 2. Usual suspects on servers
`avahi-daemon`, `cups`, `bluetooth`, `ModemManager`, `rpcbind` (unless NFS v3), `nfs-server`, `smb`,
`vsftpd`, `telnet.socket`, `rsh`/`rlogin`, `xinetd`, `postfix` listening on non-loopback, `dnsmasq`,
`gdm`/graphical.target, `cockpit.socket` (if not used), `snmpd` with default community, `kdump` (keep if you analyse crashes).

## 3. Disable → mask → remove
```bash
systemctl disable --now avahi-daemon.socket avahi-daemon.service   # stop + don't start at boot
systemctl mask avahi-daemon.service                                 # can't be started even as a dependency
systemctl set-default multi-user.target                             # no GUI on servers
dnf remove avahi cups                                               # apt purge … — best: gone means unpatchable risk gone
dnf autoremove                                                      # orphaned deps
```
Disable socket units as well as services (`*.socket` re-activates the service on connection).
Removing beats masking where package dependencies allow; mask when another package pulls it in.
Loopback-only services (postfix `inet_interfaces = loopback-only`, chronyd `port 0`) are acceptable when needed locally.

## 4. Keep it minimal
- Start from minimal images/kickstart `%packages --excludedocs` with `@core` only.
- Enforce with config management: Ansible `ansible.builtin.systemd: name=cups state=stopped enabled=false masked=true` and a package denylist.
- Alert on new listeners: compare `ss -Htulpn` to an approved list in monitoring.

## Gotchas
- Masking a unit another service `Requires=` makes that service fail — check `systemctl list-dependencies --reverse <unit>` first.
- `rpcbind` is needed for NFSv3 and NIS; `systemd-resolved` 127.0.0.53 is local only and fine.
- Removing packages may remove dependents; read the transaction summary before confirming.

## Verify
- [ ] `ss -tulpn` shows only role-justified listeners; non-local listeners match the firewall's open ports.
- [ ] `systemctl is-enabled` reports `masked`/`disabled` (or not-found after removal) for every removed service, and the role's services still pass health checks after reboot.
