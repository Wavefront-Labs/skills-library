---
id: computing-software.systems-network-administration.patch-management.linux-security-only-updates
name: linux-security-only-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [linux-patching, security-only-updates, updateinfo, dnf-security, apt-security-pocket, advisory-filter, errata, patch-management, dnf-upgrade-minimal]
level: practitioner
status: docs-checked
description: "Apply only security updates on Linux: dnf --security/--advisory with updateinfo, Ubuntu security pocket via unattended-upgrades or apt sources, and why errata metadata matters."
sources:
  - https://dnf.readthedocs.io/en/latest/command_ref.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/reposync.html
  - https://github.com/mvo5/unattended-upgrades/blob/master/README.md
  - https://documentation.ubuntu.com/server/how-to/software/automatic-updates/
  - https://documentation.suse.com/sles/15-SP6/html/SLES-all/cha-sw-cl.html
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Security-only updates on Linux

**Goal:** close vulnerabilities quickly on systems where you want minimal change, without
pulling every feature and bug-fix update.

## RHEL family (dnf with updateinfo)
```sh
dnf updateinfo summary
dnf updateinfo list --security            # advisories applicable to this host
dnf updateinfo list --sec-severity=Critical
dnf upgrade --security                    # all security advisories
dnf upgrade --advisory=RHSA-2026:1234     # one advisory
dnf upgrade-minimal --security            # nearest version that provides the security fix
```
- Requires repositories that publish **updateinfo** (errata); many third-party repos do not,
  so check `dnf updateinfo summary` on your own repositories. Local mirrors must sync all
  metadata (`dnf reposync --download-metadata`).
- `upgrade-minimal` moves each package only to the nearest version that carries the fix,
  which keeps change smaller than `upgrade`.

## Ubuntu/Debian
- Ubuntu publishes security fixes in the `<codename>-security` archive.
- unattended-upgrades applies only the origins listed in `Unattended-Upgrade::Allowed-Origins`
  (format `origin:archive`); a security-only list is
  `Unattended-Upgrade::Allowed-Origins { "${distro_id}:${distro_codename}-security"; };`.
  The file shipped with a release may list more origins (a current Ubuntu LTS example in the
  Ubuntu Server documentation allows the release pocket, `-security` and ESM origins), so
  review `/etc/apt/apt.conf.d/50unattended-upgrades` and remove what you do not want.
- Manual one-off: `apt list --upgradable 2>/dev/null | grep -- -security` then
  `apt install --only-upgrade <pkgs>`.

## SUSE
`zypper list-patches --category security` then `zypper patch --category security` (see the
`zypper-patch-on-suse` skill).

## Gotchas
- Security-only patching still needs reboots for kernels and restarts for libraries
  (check `needs-restarting -r`, `needrestart`).
- Skipping non-security updates for long periods makes the eventual full update bigger
  and riskier; do full updates on a slower cadence.
- A security fix may depend on a non-security update; dnf/apt pull it automatically.

## Verify
`dnf updateinfo list --security` returns nothing (or only accepted exceptions); on Ubuntu,
`/var/log/unattended-upgrades/unattended-upgrades.log` shows the packages applied; scanner
shows the CVEs closed.

## Checked

Checked 2026-10-27 against the DNF command reference, dnf-plugins-core reposync page, SUSE zypper manual page, the unattended-upgrades README and the Ubuntu Server automatic-updates page.
- `dnf updateinfo summary|list`, `--security`, `--sec-severity`, `--advisory`, `upgrade-minimal`: confirmed in the DNF command reference.
- `dnf reposync --download-metadata`: confirmed. zypper `list-patches --category` and `patch --category`: confirmed.
- Allowed-Origins format and the Ubuntu default origins (release, security, ESM): confirmed; the earlier claim that the default is security only was wrong and is corrected.
- Removed unconfirmed: per-distribution errata availability list, Debian security pocket naming, the alternate sources-list trick, Ubuntu Pro ESM scope.
- The sources entry that pointed at a blocked Red Hat page was replaced with readable pages.
Method: documentation only; no commands were run.
