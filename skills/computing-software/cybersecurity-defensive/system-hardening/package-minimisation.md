---
id: computing-software.cybersecurity-defensive.system-hardening.package-minimisation
name: package-minimisation
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [package-minimisation, minimal-install, attack-surface-reduction, linux-hardening, cis-benchmarks, compilers-removal]
level: practitioner
status: draft
description: "Minimise installed packages on Linux servers: minimal install profiles, finding and removing unneeded packages and their dependencies, preventing reinstalls, and verifying."
sources: ["https://www.cisecurity.org/cis-benchmarks", "https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/security_hardening/index", "https://csrc.nist.gov/pubs/sp/800/123/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Package minimisation

Every installed package is code to patch and a possible tool for an attacker (compilers, network clients,
interpreters). NIST SP 800-123 and CIS Benchmarks both start server hardening by removing what is not needed.

## Start minimal
- RHEL/Rocky/Alma: "Minimal Install" environment group in kickstart (`%packages --excludedocs` with
  `@^minimal-environment`); add only role packages.
- Debian/Ubuntu: server/minimal images; `debootstrap --variant=minbase` for custom images;
  `APT::Install-Recommends "false";` in `/etc/apt/apt.conf.d/` to stop recommended extras.
- Containers: distroless or slim bases (see distroless-minimal-images).

## Find what to remove on existing hosts
```bash
# RHEL family
dnf list installed | wc -l
dnf repoquery --userinstalled            # explicitly installed, not dependencies
dnf group list --installed
# Debian/Ubuntu
apt-mark showmanual
dpkg-query -W -f='${Installed-Size}\t${Package}\n' | sort -n | tail -30
```
CIS-listed candidates on servers: X Window System (`xorg-x11*`, `xserver-xorg*`), Avahi, CUPS, DHCP/DNS/FTP/
HTTP/IMAP/Samba/NFS/SNMP/NIS/rsync servers when not the host's role, `telnet`, `rsh`, `talk`, `ypbind`,
`tftp`, `ldap` clients if unused.
Optional for hardened production: compilers (`gcc`, `make`) and debuggers, which help attackers build tools
on the host.

## Remove safely
```bash
dnf remove telnet xorg-x11-server-common && dnf autoremove
apt purge telnet avahi-daemon cups && apt autoremove --purge
```
Review the dependency list before confirming; removing a library can take out needed packages.

## Keep it minimal
- Config management state: Ansible `package: name=telnet state=absent`, Puppet `ensure => absent`.
- `dnf`/`apt` pinning to block reinstall of forbidden packages (apt preferences with `Pin-Priority: -1`).
- Golden images built from code; drift detection compares package lists to the baseline.
- Software inventory (CIS Control 2) alerts on unauthorised packages.

## Gotchas
- Removing Python on modern distros breaks package managers and tools; minimise extras, not the platform.
- Monitoring/backup agents may pull dependencies you removed; test on staging images.
- Desktop-oriented meta-packages (`ubuntu-desktop`) removing pulls many packages; rebuild from minimal instead.

## Verify
Package count and list match the role baseline; vulnerability scanner findings per host drop; config management
reports no forbidden packages present.
