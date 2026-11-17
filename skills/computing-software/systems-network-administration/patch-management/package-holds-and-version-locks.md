---
id: computing-software.systems-network-administration.patch-management.package-holds-and-version-locks
name: package-holds-and-version-locks
category: computing-software
field: systems-network-administration
product: patch-management
tags: [package-hold, versionlock, apt-mark, dnf-versionlock, zypper-addlock, linux-patching, patch-exceptions]
level: practitioner
status: docs-checked
description: "Hold specific packages during patching with apt-mark hold, dnf versionlock and zypper locks, document holds as time-limited exceptions, and release them safely."
sources:
  - https://manpages.debian.org/bookworm/apt/apt-mark.8.en.html
  - https://manpages.debian.org/stable/apt/apt_preferences.5.en.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/versionlock.html
  - https://dnf.readthedocs.io/en/latest/conf_ref.html
  - https://documentation.suse.com/sles/15-SP6/html/SLES-all/cha-sw-cl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Package holds and version locks

**Goal:** keep a known-bad or incompatibility-sensitive package on its current version while everything else patches.

## Debian/Ubuntu
```bash
apt-mark hold linux-image-generic postgresql-16
apt-mark showhold
apt-mark unhold postgresql-16
```
A held package is not automatically installed, upgraded or removed. Pinning in `/etc/apt/preferences.d/` (`Pin` and `Pin-Priority` records, see apt_preferences(5)) gives finer control, for example keeping a package on a specific origin or version.

## RHEL/Fedora
```bash
# install the versionlock plugin from dnf-plugins-core (package name varies by release)
dnf versionlock add nvidia-driver              # locks to the installed version
dnf versionlock add --raw 'kernel-5.14.0-427.*' # --raw keeps the pattern as written
dnf versionlock list
dnf versionlock delete nvidia-driver
```
`dnf versionlock exclude <spec>` blocks one specific bad version instead. Alternatively `excludepkgs=kernel*` on a repository section excludes packages from all operations, but excludes are easy to forget; prefer versionlock, which lists its entries.

## SUSE
```bash
zypper addlock kernel-default
zypper locks
zypper removelock kernel-default
```

## Windows equivalent
Decline or do not approve the specific KB in WSUS/ConfigMgr for the affected group, or hide it on single hosts.

## Treat holds as exceptions
- Record each hold: host/group, package, reason (ticket, vendor bug), expiry date, owner.
- A held package can block security fixes for itself and anything depending on it; the vulnerability scanner will keep reporting it.
- Review holds at every patch cycle; report them in compliance reports.

## Find holds fleet-wide
```bash
ansible all -m shell -a 'apt-mark showhold 2>/dev/null; dnf versionlock list 2>/dev/null; zypper -q locks 2>/dev/null'
```

## Verify
Fleet hold list matches the exception register exactly; expired holds are removed and the package updated.

## Checked

Checked 2026-10-27 against the Debian apt-mark and apt_preferences manual pages, the dnf-plugins-core versionlock page, the DNF configuration reference and the SUSE zypper manual page.
- `apt-mark hold`, `showhold`, `unhold`; held packages are not automatically installed, upgraded or removed: confirmed.
- `dnf versionlock add|exclude|list|delete|clear`, `--raw` for patterns, plugin config in `/etc/dnf/plugins/versionlock.conf`: confirmed.
- `excludepkgs` on repository sections: confirmed. zypper `addlock`, `locks`, `removelock`: confirmed.
- apt Pin / Pin-Priority records: confirmed.
- Removed unconfirmed: the versionlock package name, the claim that unattended-upgrades honours holds, and the PSWindowsUpdate cmdlet name.
Method: documentation only; no commands were run.
