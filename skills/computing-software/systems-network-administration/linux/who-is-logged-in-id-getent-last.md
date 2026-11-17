---
id: computing-software.systems-network-administration.linux.who-is-logged-in-id-getent-last
name: who-is-logged-in-id-getent-last
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, users-groups, id-command, getent, who, w, last, lastb, lastlog, utmp, wtmp, login-history, audit, lpic-1, rhcsa, sysadmin]
level: practitioner
status: verified
description: "Answer who a user is and who has been on the box: id and getent through NSS, who/w for current sessions, last/lastb/lastlog for login history, and the wtmp/btmp files behind them."
sources:
  - https://man7.org/linux/man-pages/man1/id.1.html
  - https://man7.org/linux/man-pages/man1/getent.1.html
  - https://man7.org/linux/man-pages/man1/last.1.html
  - https://man7.org/linux/man-pages/man5/utmp.5.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# id, getent, who, w, last

**Goal:** quickly establish identity (UIDs, groups, source directory) and login activity for
troubleshooting access problems or investigating an incident.

## 1. Identity
```bash
id alice                     # uid, gid, all groups (from NSS: files, sssd, ldap…)
id -nG alice                 # group names only
id                           # YOUR current process credentials (may differ from DB until re-login)
getent passwd alice          # resolves through nsswitch.conf — local or directory
getent group wheel
getent passwd                                 # enumerates the databases NSS can list (a directory service may not list everyone)
getent shadow alice          # root only
getent hosts db01; getent ahosts db01         # same NSS mechanism for names
grep -E '^(passwd|group|shadow|hosts)' /etc/nsswitch.conf
```
If `getent passwd` with no arguments does not list directory users while `getent passwd alice` finds them, the directory
service is probably not set up to enumerate; lookups by name still work.

## 2. Who's here now
```bash
who -a                    # sessions from utmp: user, tty, login time, remote host
w                         # + idle time, JCPU, what they're running, load
loginctl list-sessions; loginctl session-status <id>    # systemd-logind view (includes non-tty sessions)
users
```

## 3. History
```bash
last -F -n 30                # recent logins/reboots from /var/log/wtmp, full timestamps
last alice; last reboot; last -s yesterday -t today
last -i                      # IP addresses instead of hostnames
lastb -n 20                  # FAILED logins from /var/log/btmp (root)
lastlog                      # last login per account, from the lastlog database (do not rotate that file)
journalctl -u sshd --since today | grep -E 'Accepted|Failed'   # authoritative for SSH
```
Some distributions are moving from `/var/log/wtmp` to `wtmpdb`, a Y2038-safe replacement database; it provides its own `wtmpdb last`. On Debian 13 `last`, `lastb` and `lastlog` are not part of util-linux: install `wtmpdb` (its `last` reads a database such as `/var/log/wtmp.db` and fails with `Cannot open database` until one exists, and has no `--help`) and `lastlog2`; `lastb` was still missing afterwards.

## Gotchas
- wtmp is usually rotated by the distribution's log rotation; `last -f <file>` reads an older or alternate file.
- Non-interactive logins (scp, sftp, `ssh host cmd`) often don't create utmp/wtmp entries — check auth logs.
- An attacker with root can edit wtmp; correlate with journal/remote logs.
- `who` reads login records only; it does not list service processes.

## Verify
- [ ] `id <user>` group list matches what access control expects.
- [ ] Login history from `last` agrees with `journalctl -u sshd` for the same period.

## Checked

Documentation check. Checked 2026-10-27 against man-pages project (man7.org) id(1) and lastlog(8), the util-linux last(1) source, and the wtmpdb README: `id -nG`, `-G`, `-n`; `last -F` (full times), `-i`/`--ip`, `-s`/`--since`, `-f` file, and that lastb reads /var/log/btmp; the lastlog database must not be rotated; wtmpdb is the Y2038-safe wtmp replacement. Removed the sssd `enumerate` claim, the lastlog2 command name, the monthly rotation claim and the container remark, which no checked page states.
Method: documentation, plus commands run 2026-11-01 in a Debian 13 (trixie) rootless Podman container (util-linux 2.41.5, wtmpdb installed): id, id -nG, -G, -un, getent passwd/group/shadow/hosts/ahosts and enumeration (38 local entries), nsswitch.conf lines, who -a (system boot line), w, users, the empty wtmp/btmp/lastlog files, and the wtmpdb `last` option list (-F, -i, -n, -s, -t, -f, -x). Corrected: Debian 13 does not install `last`, `lastb` or `lastlog`. Not run: output of last/lastlog with real logins, lastb, loginctl, journalctl.
