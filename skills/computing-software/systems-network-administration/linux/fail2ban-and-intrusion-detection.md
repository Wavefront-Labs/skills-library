---
id: computing-software.systems-network-administration.linux.fail2ban-and-intrusion-detection
name: fail2ban-and-intrusion-detection
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fail2ban, aide, intrusion-detection, rootkit, rkhunter, chkrootkit, hids, file-integrity, jail-local, banaction, nftables-ban, firewalld-ban, brute-force, sshd-jail, recidive, aide-init, aide-check, integrity-database, lpic-2, security, sysadmin, failregex, fail2ban-client, aide-conf]
level: practitioner
status: docs-checked
description: "Stop brute-force and detect compromise on Linux: fail2ban jails with nftables/firewalld bans, custom filters, AIDE file-integrity baselines and daily checks, and rkhunter scans."
sources:
  - https://github.com/fail2ban/fail2ban/blob/master/config/jail.conf
  - https://github.com/fail2ban/fail2ban/tree/master/config/action.d
  - https://github.com/aide/aide/blob/master/doc/aide.1
  - https://github.com/aide/aide/blob/master/doc/aide.conf.5
  - https://github.com/Rootkit-Hunter/rkhunter/blob/master/files/rkhunter.8
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# fail2ban and host intrusion detection — ban the noise, notice the change

**Goal:** automatic bans for repeated auth failures across sshd/web/mail, a file-integrity
baseline that flags unexpected changes, and periodic rootkit scans — all cron/timer driven
and reporting somewhere a human reads.

## 1. fail2ban
```bash
dnf install fail2ban       # or apt install fail2ban; upstream jail.conf ships jails disabled unless enabled=true
```
Never edit `jail.conf`; create `/etc/fail2ban/jail.local`:
```ini
[DEFAULT]
ignoreip = 127.0.0.1/8 ::1 10.0.0.0/8      # never ban yourself / the bastion / monitoring
bantime  = 1h
findtime = 10m
maxretry = 5
bantime.increment = true                   # repeat offenders get longer bans
bantime.maxtime = 1w
backend = systemd                           # read the journal; the jail.conf default "auto" picks pyinotify, polling or systemd
banaction = nftables-multiport              # or firewallcmd-rich-rules on firewalld hosts, iptables-multiport legacy
banaction_allports = nftables-allports
destemail = ops@example.com
action = %(action_mw)s                      # ban + mail with whois; %(action_)s = ban only

[sshd]
enabled = true
mode = aggressive                           # sshd filter modes: normal (default), ddos, extra, aggressive (combines all)
port = ssh,2222

[nginx-http-auth]
enabled = true
logpath = /var/log/nginx/*error.log

[postfix-sasl]
enabled = true                              # upstream jail uses filter postfix[mode=auth]

[recidive]
enabled = true                              # bans IPs that were banned 5x in a day, for a week, all ports
logpath = /var/log/fail2ban.log
bantime = 1w
findtime = 1d
maxretry = 5
```
```bash
systemctl enable --now fail2ban
fail2ban-client status; fail2ban-client status sshd          # banned list, counters
fail2ban-client set sshd unbanip 203.0.113.9
fail2ban-client set sshd banip 203.0.113.9
fail2ban-regex /var/log/nginx/error.log /etc/fail2ban/filter.d/nginx-http-auth.conf   # test a filter
fail2ban-regex systemd-journal /etc/fail2ban/filter.d/sshd.conf   # against the journal
nft list table inet f2b-table                                      # see the actual ban set
```
Custom filter for an app log (`/etc/fail2ban/filter.d/myapp.conf`):
```ini
[Definition]
failregex = ^.* Login failed for .* from <HOST>$
ignoreregex =
```
plus a `[myapp]` jail with `logpath` and `port`. `<HOST>` is mandatory; test with `fail2ban-regex`.
- Behind a reverse proxy/CDN you ban the proxy. Log the real client IP (`X-Forwarded-For` → `$http_x_forwarded_for`
  in the log format) and point the filter at it; never enable auto-bans on a shared ingress IP.
- On firewalld hosts, the `firewallcmd-*` actions add rich rules; with plain nftables the `nftables-*`
  actions create their own table so your ruleset is untouched.
- IPv6: the `nftables` action's `table_family` defaults to `inet` (other values `ip`, `ip6`); check that your banaction covers IPv6.
- Logs: `/var/log/fail2ban.log`; `loglevel = INFO` in `fail2ban.local`.

## 2. AIDE — file integrity baseline
```bash
dnf install aide     # or apt install aide
# aide.conf: selection lines like  /etc  <group> ;  !/var/lib/docker  (a leading ! excludes a regex); group names such as
# PERMS, CONTENT_EX, LOG are defined by your distribution's aide.conf, not by AIDE itself
aide --init                                              # writes the database named by database_out in aide.conf
mv <database_out file> <database_in file>                # paths come from aide.conf (defaults: see `aide --version`)
aide --check                                             # compare the filesystem with the database
aide --update                                            # check and write a new database; then move it into place after a known patch run
```
- Copy the database and `aide.conf` off-box (or sign them); an attacker with root can
  regenerate the baseline. `database_in` also accepts a URL, so the database can be read from elsewhere.
- Re-baseline **right after** every package update, in the same change window, or every
  report is noise. Pattern: `dnf update -y && aide --update && mv …` in the patch job.
- Exclude churn: `/var/log`, `/var/cache`, container storage, `/home` caches; include
  `/boot`, `/etc`, `/usr/bin`, `/usr/sbin`, `/usr/lib*`, `/root`, systemd dirs.
- Timer: `/etc/systemd/system/aide-check.timer` daily → `aide --check | mail -s "AIDE $(hostname)" ops@example.com`
  (or ship to the SIEM); exit code 0 = no change, bits set otherwise.

## 3. Rootkit scanners
```bash
dnf install rkhunter      # EPEL / apt
rkhunter --propupd                    # baseline file properties (after a clean install/patch)
rkhunter --check --skip-keypress --report-warnings-only   # cron-friendly; the log is LOGFILE in rkhunter.conf (default /var/log/rkhunter.log)
```
The man page says to run `--check` regularly and to run `--propupd` again after legitimate file changes
(otherwise the file-properties check warns). Treat rkhunter as a second opinion, not a control:
AIDE + auditd + centralised logs are the controls.

## 4. What to do on a hit
A true AIDE change on `/usr/bin` or `/boot` without a package explanation (`rpm -Vf <file>`,
`debsums -c`) → treat as compromise: isolate from the network, capture volatile state
(`ps auxf`, `ss -tunap`, `lsmod`, `last`, audit logs) to another host, then rebuild from a
known-good image. Don't "clean" a rooted box in place.

## Verify
- [ ] From a test IP, 6 wrong SSH passwords → `fail2ban-client status sshd` lists it banned and `nc -zv host 22` times out; `unbanip` restores it.
- [ ] `aide --check` after a deliberate `touch /etc/test-aide` reports exactly that file; re-baseline clears it.
- [ ] The daily check's output lands in a mailbox/SIEM and someone is on the hook to read it.

## Checked

Checked 2026-10-26 against fail2ban/fail2ban master (last commit 2026-10-10: config/jail.conf, fail2ban.conf, action.d/nftables*.conf, filter.d/sshd.conf and postfix.conf), aide/aide master (last commit 2026-10-18: doc/aide.1 and doc/aide.conf.5) and the Rootkit-Hunter/rkhunter GitHub mirror (files/rkhunter.8 and rkhunter.conf; the mirror's last commit is 2018, so behaviour of current rkhunter releases beyond these files is not covered). Confirmed: jail.conf defaults and action_mw meaning, bantime.increment and bantime.maxtime options, backend values, recidive defaults, nftables table f2b-table with family inet, action file names, sshd filter modes, aide exit-status bits, database_in/database_out semantics, rkhunter --propupd, --check, --skip-keypress and --report-warnings-only, default log file. Corrected: the postfix-sasl jail does not use mode=more (its filter is postfix[mode=auth]); AIDE database paths and rule group names come from the distribution's aide.conf. Removed: the 0.10 IPv6 version claim, distro default-jail claims, the STIG and prelink remarks, chkrootkit and unhide remarks.

Method: documentation only; no commands were run.
