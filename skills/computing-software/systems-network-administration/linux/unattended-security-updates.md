---
id: computing-software.systems-network-administration.linux.unattended-security-updates
name: unattended-security-updates
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, unattended-upgrades, dnf-automatic, yum-cron, patching, patch-management, security-updates, automatic-updates, apt-daily, needrestart, reboot-required, kpatch, livepatch, patch-cadence, maintenance-window, apt-listchanges, dnf-updateinfo, cve, lpic-1, sysadmin, unattended-upgrades-conf, package-blacklist]
level: practitioner
status: docs-checked
description: "Automate security patching: unattended-upgrades (origins, blacklists, reboot policy, timers), dnf-automatic (security-only, apply vs download), reboot detection with needrestart, and a patch cadence."
sources:
  - https://github.com/mvo5/unattended-upgrades
  - https://github.com/Debian/apt/tree/main/debian
  - https://dnf.readthedocs.io/en/latest/automatic.html
  - https://dnf-plugins-core.readthedocs.io/en/latest/needs_restarting.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Unattended security updates and patch cadence

**Goal:** security fixes land within a day without a human, everything else lands in
a planned window, and a host that needs a reboot says so (or reboots when you allow it).

## 1. Policy first (two sentences, then automate them)
- *Security* updates: automatic, daily, from the distro security origin only.
- *Everything else* (feature, kernel, third-party repos): weekly/monthly window, staged
  (canary → 10% → all), with reboot. Automating full upgrades on servers is a choice,
  not a default; automating them on fleet-managed stateless nodes is fine.
- Reboots: either allowed in a fixed slot per host group, or surfaced to monitoring
  (`/var/run/reboot-required`, `dnf needs-restarting -r`) and done by a human.

## 2. Debian/Ubuntu: `unattended-upgrades`
```bash
apt install unattended-upgrades apt-listchanges
dpkg-reconfigure -plow unattended-upgrades     # writes /etc/apt/apt.conf.d/20auto-upgrades
```
The upstream `20auto-upgrades` contains these two lines:
```
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
```
Tune `/etc/apt/apt.conf.d/50unattended-upgrades` (keep the vendor file, override in a
`52local` file to survive package upgrades):
```
Unattended-Upgrade::Allowed-Origins {
    "${distro_id}:${distro_codename}-security";
    "${distro_id}ESMApps:${distro_codename}-apps-security";   // Ubuntu Pro
    "${distro_id}ESM:${distro_codename}-infra-security";
    // "${distro_id}:${distro_codename}-updates";   // enable only if you want non-security too
};
Unattended-Upgrade::Package-Blacklist { "linux-image-*"; "postgresql-*"; };
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";              // or "true" with:
Unattended-Upgrade::Automatic-Reboot-Time "03:30";
Unattended-Upgrade::Automatic-Reboot-WithUsers "false";
Unattended-Upgrade::Mail "ops@example.com";
Unattended-Upgrade::MailReport "on-change";                // only-on-error | on-change | always
Unattended-Upgrade::MinimalSteps "true";                   // install in small steps so a shutdown mid-run is safe
Unattended-Upgrade::SyslogEnable "true";
```
Origins can also be matched with `Unattended-Upgrade::Origins-Pattern`, for example the Debian security entries
`"origin=Debian,codename=${distro_codename}-security,label=Debian-Security";` and
`"origin=Debian,codename=${distro_codename},label=Debian-Security";`. Stock patterns are kept unless you use `#clear`
before your own list (upstream README). Third-party repos are not upgraded unless their origin is listed.

Timing is driven by `apt-daily.timer` (download; 06:00 and 18:00 with a 12 h random delay upstream) and `apt-daily-upgrade.timer`
(install; upstream `OnCalendar=*-*-* 6:00`, `RandomizedDelaySec=60m`). Change with
`systemctl edit apt-daily-upgrade.timer` →
```
[Timer]
OnCalendar=
OnCalendar=*-*-* 03:00
RandomizedDelaySec=30m
```
Dry run and logs:
```bash
unattended-upgrade --dry-run -d          # shows what would be installed and why not
cat /var/log/unattended-upgrades/unattended-upgrades.log
journalctl -u apt-daily-upgrade.service
```
Gotchas: unattended-upgrades checks for conffile prompts; a package that would need one is not upgraded unless you
set a dpkg option (`Dpkg::Options { "--force-confdef"; "--force-confold"; }` keeps the old config; see
`unattended-upgrade(8)` and the upstream README). `/var/run/reboot-required` is checked when
`Unattended-Upgrade::Automatic-Reboot` is true; alert on it otherwise. Phased updates can defer some packages on
Ubuntu; that is intended behaviour, not a failure.

## 3. RHEL/Fedora/Rocky: `dnf-automatic`
```bash
dnf install dnf-automatic
```
`/etc/dnf/automatic.conf`:
```ini
[commands]
upgrade_type = security     # default | security (documented default: default)
random_sleep = 1800         # seconds; documented default 0 (the systemd timers add up to 1 h)
download_updates = yes
apply_updates = yes         # no = download/notify only
reboot = when-needed        # never (default) | when-needed | when-changed
reboot_command = "shutdown -r +5 'Rebooting after automatic updates'"   # this is also the default

[emitters]
emit_via = stdio,motd       # also: email, command, command_email (documented default: email, stdio, motd)
[email]
email_from = root@example.com
email_to = ops@example.com
email_host = localhost
```
Enable **one** timer, which decides behaviour regardless of `apply_updates`:
```bash
systemctl enable --now dnf-automatic-install.timer   # install
# dnf-automatic-download.timer | dnf-automatic-notifyonly.timer | dnf-automatic.timer (uses the conf)
systemctl list-timers 'dnf-automatic*'
systemctl edit dnf-automatic-install.timer           # OnCalendar=*-*-* 03:00
```
`upgrade_type = security` looks only at updates with an issued security advisory (repo `updateinfo` metadata). Exclusions: `excludepkgs=kernel*,postgresql*` in
`/etc/dnf/dnf.conf` or per-repo `exclude=`; `dnf versionlock add pkg` for pinned
versions. Check manually: `dnf updateinfo list --security`, `dnf check-update --security`,
`dnf update --security --assumeno`. After the run:
`dnf needs-restarting -r` (`--reboothint`: exit code 1 if a reboot is required, 0 if not) and `dnf needs-restarting -s`
(`--services`: affected systemd services that can be safely restarted).

## 4. Cadence and verification
- Security: daily automatic as above. Full update: a fixed window per environment
  (dev Monday, staging Tuesday, prod Thursday) so a bad package is caught before prod.
- Report, don't trust: a nightly job that collects `apt list --upgradable` /
  `dnf check-update --security -q` plus the reboot flag into monitoring is what tells you automation silently stopped.
- Keep the history: `dnf history list`, `grep ' install \| upgrade ' /var/log/dpkg.log`.

## Verify
- [ ] `unattended-upgrade --dry-run -d` lists only security-origin packages (or
      `dnf update --security --assumeno` lists the expected set).
- [ ] `systemctl list-timers` shows `apt-daily-upgrade.timer` / `dnf-automatic-*.timer`
      with the next run in your window.
- [ ] A test host with a known pending security update applies it on the next run and
      the log/email reports it.
- [ ] Monitoring alerts when `/var/run/reboot-required` exists or
      `dnf needs-restarting -r` exits 1 for longer than the agreed window.

## Checked

Checked against the unattended-upgrades upstream repository (mvo5/unattended-upgrades: README.md, data/50unattended-upgrades.Debian and .Ubuntu, data/20auto-upgrades, man page; last push 2026-10-24), the apt repository `debian/apt-daily*.timer` files, dnf4 `automatic.rst` and dnf-plugins-core `needs_restarting.rst` and dnf4 conf_ref/command_ref.
Confirmed: `Unattended-Upgrade::Allowed-Origins` patterns for Ubuntu security and ESM, `Package-Blacklist`, `Remove-Unused-Dependencies`, `Automatic-Reboot`, `Automatic-Reboot-Time`, `Automatic-Reboot-WithUsers`, `Mail`, `MailReport` values, `MinimalSteps`, `SyslogEnable`, `Origins-Pattern` syntax and `#clear`, `--debug --dry-run`, log directory, `/var/run/reboot-required`, apt-daily timer schedules; dnf-automatic `upgrade_type`, `random_sleep`, `download_updates`, `apply_updates`, `reboot` values and default, `reboot_command` default, `emit_via` values, timer names, `/etc/dnf/automatic.conf`, `needs-restarting -r/-s`.
Removed as unconfirmed: the AutocleanInterval line, apt-cache policy origin lookup, apt-locked and metered-connection skip reasons, needrestart settings, version gates for phased updates and dnf-automatic reboot, yum-cron, Livepatch and kpatch section, exporter and snapshot-staging remarks.

Method: documentation only; no commands were run.
