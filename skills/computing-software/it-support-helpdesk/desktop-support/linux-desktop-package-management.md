---
id: computing-software.it-support-helpdesk.desktop-support.linux-desktop-package-management
name: linux-desktop-package-management
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, linux-client, linux-package-management, dnf, unattended-upgrades, versionlock, fedora, debian]
level: practitioner
status: docs-checked
description: "Support Fedora desktops with dnf (install, upgrade, exclude, versionlock, dnf-automatic) and Debian desktops with unattended-upgrades and the apt systemd timers."
sources:
  - "https://docs.fedoraproject.org/en-US/quick-docs/dnf/"
  - "https://wiki.debian.org/UnattendedUpgrades"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# linux-desktop-package-management

Goal: keep Linux desktops patched and fix a bad update without guessing.

## Fedora (dnf)
```bash
dnf search packagename
sudo dnf install packagename
sudo dnf remove packagename
sudo dnf upgrade
```
- `check-update` checks without downloading or installing; `downgrade` reverts to the previous version of a package;
  `reinstall` reinstalls; `autoremove` removes dependencies no longer required; `info` shows name, version, release.
- Fedora Atomic Desktops and CoreOS work differently (image-based); the page points to the Atomic Desktops guide.
- Current Fedora releases (since 41) use DNF5 by default; its documentation is separate from the DNF4 pages.
- **Hold a bad update**: `sudo dnf upgrade --exclude=packagename`, or `excludepkgs=packagename` in
  `/etc/dnf/dnf.conf` (or in a repo file under `/etc/yum.repos.d/`); `--disableexcludes` overrides it per command.
- **Versionlock** (plugin in dnf-plugins-core): `sudo dnf install 'dnf-command(versionlock)'`, then
  `sudo dnf versionlock add package` and `sudo dnf versionlock delete package`; `list` shows locks, `clear`
  deletes all.
- Automatic updates: the `dnf-automatic` package downloads and installs updates and can report by email.

## Debian (unattended-upgrades)
- Check it is enabled: `sudo dpkg-reconfigure unattended-upgrades` should ask whether to automatically download and
  install stable updates (answer yes).
- Local config: copy `/etc/apt/apt.conf.d/50unattended-upgrades` to `/etc/apt/apt.conf.d/52unattended-upgrades-local`
  and edit the `Unattended-Upgrade::Origins-Pattern` section. The default installs security updates but not new
  features. `Unattended-Upgrade::Mail` needs a local MTA.
- Debug with `sudo unattended-upgrade -d`; logs are in `/var/log/dpkg.log` and `/var/log/unattended-upgrades/`.
- Schedule comes from systemd timers `apt-daily.timer` (downloads) and `apt-daily-upgrade.timer` (upgrades); change
  with `systemctl edit`, clearing `OnCalendar=` before setting a new one.
- Laptops: unattended-upgrades refuses to run on battery by default (`Unattended-Upgrade::OnlyOnACPower`), and the
  skipped upgrade is not announced, so updates can be delayed much longer than configured.
- `needrestart` packages identify processes that must restart to apply security updates without a reboot.

## Verify
`dnf check-update` is empty after updating, or the Debian logs show the unattended run, and the app launches from the
user's session.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Fedora DNF quick-doc and the Debian UnattendedUpgrades wiki page. The Ubuntu package-management
page returned an empty stub, so apt, dpkg lock, snap, flatpak, RHEL subscription, pip and Ubuntu defaults were
removed as unsourced, as were `dnf history undo`, `provides` and `clean all`.
