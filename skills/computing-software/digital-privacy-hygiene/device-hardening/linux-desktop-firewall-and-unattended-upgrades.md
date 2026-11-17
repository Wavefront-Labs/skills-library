---
id: computing-software.digital-privacy-hygiene.device-hardening.linux-desktop-firewall-and-unattended-upgrades
name: linux-desktop-firewall-and-unattended-upgrades
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, linux-desktop-security, ufw, firewalld, unattended-upgrades, dnf-automatic, linux, automatic-updates]
level: practitioner
status: docs-checked
description: "Baseline a personal Linux laptop: host firewall (ufw or firewalld) denying inbound, and automatic security updates via unattended-upgrades or dnf-automatic."
sources:
  - "https://www.privacyguides.org/en/os/linux-overview/"
  - "https://help.ubuntu.com/community/UFW"
  - "https://wiki.debian.org/UnattendedUpgrades"
  - "https://docs.fedoraproject.org/en-US/quick-docs/autoupdates/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux desktop firewall and automatic updates

**Goal:** two settings that close most of the gap between a fresh Linux install and a
reasonably hardened laptop.

## Firewall (Ubuntu and derivatives: ufw)
ufw ("Uncomplicated Firewall") is Ubuntu's default firewall tool and is **disabled by default**. When enabled, the
default profile denies incoming traffic with some exceptions meant to ease home use.
```bash
sudo ufw enable
sudo ufw status verbose       # expect: Default: deny (incoming), allow (outgoing)
sudo ufw allow from 192.168.1.0/24 to any port 22 proto tcp   # only if you need SSH from the LAN
sudo ufw status numbered      # rule order matters; first match wins
```
- Rules are evaluated in order and the first match applies, so put specific rules before generic ones.
- `sudo ufw show raw` lists the exceptions to the default deny; `sudo ufw logging on` turns logging on.
- `gufw` is a GUI front end.
- ufw allows ICMP ping by default; the wiki shows editing `/etc/ufw/before.rules` to change that.

## Firewall (Fedora: firewalld)
Fedora's automatic-updates guide recommends a host-based firewall using firewalld as extra protection while updates
are pending. Check your distribution's documentation for zones and commands; this skill does not repeat them.

## Automatic security updates
**Debian/Ubuntu (unattended-upgrades)**
```bash
sudo apt install unattended-upgrades      # reinstalling is harmless if already present
sudo dpkg-reconfigure unattended-upgrades # asks whether to download and install stable updates: answer yes
```
- Put local settings in `/etc/apt/apt.conf.d/52unattended-upgrades-local` (copied from `50unattended-upgrades`); the
  default configuration auto-installs security updates, not new features. The `Unattended-Upgrade::Origins-Pattern`
  section lists what is allowed.
- Look at `/var/log/dpkg.log` and `/var/log/unattended-upgrades/`; `sudo unattended-upgrade -d` runs it manually for
  debugging. Consider `apt-listchanges` for email about changes.
- Schedule comes from the systemd timers `apt-daily.timer` and `apt-daily-upgrade.timer`.
- Laptops: by default it refuses to run when not on AC power, and a skipped run is not reported, so updates can be
  delayed. Forcing it with `Unattended-Upgrade::OnlyOnACPower "false";` is a risk the wiki flags (an interrupted
  upgrade could leave the system unbootable).
- Alternative on GNOME: enable automatic updates in the Software app. Do not run alternatives at the same time.

**Fedora (dnf-automatic)**
```bash
sudo dnf install dnf5-plugin-automatic
sudo systemctl enable --now dnf-automatic.timer
systemctl status dnf-automatic.timer
```
- Config is `/etc/dnf/automatic.conf`. By default it downloads updates but does not install them. For install and
  reboot when needed, set `apply_updates=True` and `reboot=when-needed` under `[commands]`.
- The timer runs once daily by default; monitor `/var/log/dnf5.log`. Kernel updates are excluded by default in
  Fedora's `dnf.conf`.

## Other updates
Some distributions do not download firmware updates automatically; Privacy Guides says to install fwupd for that.
Debian-based and Arch systems may need the package manager run by hand for security updates.

## Gotchas
- A kernel update does not take effect until reboot, and some services need a restart. Updating without rebooting
  leaves a window where the system looks patched but is not (Fedora guide).
- Fedora advises against automatic updates on critical servers that cannot tolerate unplanned downtime.

## Verify
- [ ] `sudo ufw status verbose` shows active, default deny incoming (Ubuntu).
- [ ] Unattended upgrade log or `/var/log/dnf5.log` shows recent runs.

## Checked
Confirmed 2026-11-08 against the Ubuntu UFW wiki page, the Debian PeriodicUpdates/unattended-upgrades wiki page, the
Fedora automatic-updates quick doc and Privacy Guides' Linux overview. Removed: the `ufw default` commands, the
firewalld zone commands, `ss -tulpn` advice, "Ubuntu enables security updates by default on desktop", the Flatpak
update note, livepatch, and the Docker-bypasses-ufw claim, none of which the pages state.
Method: docs-only read of cited pages, 2026-11-08
