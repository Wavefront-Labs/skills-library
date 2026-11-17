---
id: computing-software.systems-network-administration.linux.pam-access-and-pam-time-restrictions
name: pam-access-and-pam-time-restrictions
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pam, pam-access, access-conf, pam-time, time-conf, login-restrictions, allowgroups, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Restrict who may log in from where and when: pam_access rules in access.conf (users, groups, hosts, networks, ttys) and pam_time schedules in time.conf, per service."
sources:
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_access/access.conf.5.xml
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_access/pam_access.8.xml
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_time/time.conf.5.xml
  - https://github.com/linux-pam/linux-pam/blob/master/NEWS
  - https://github.com/authselect/authselect/blob/master/profiles/sssd/README
  - https://github.com/SSSD/sssd/blob/master/src/man/sssd-simple.5.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pam_access and pam_time

**Goal:** "only the ops group may log in to production, only from the admin network; root
only on the console; contractors only during business hours."

## 1. Enable pam_access
- RHEL: `authselect enable-feature with-pamaccess && authselect apply-changes` (the sssd profile then includes
  `account required pam_access.so` in its account stack).
- Debian: add `account required pam_access.so` to `/etc/pam.d/sshd` (or `common-account` for all services).
Per-service file: `account required pam_access.so accessfile=/etc/security/access-sshd.conf`.

## 2. /etc/security/access.conf
`permission : users/groups : origins` — first match wins; `+` allow, `-` deny.
```
+ : root : LOCAL                     # root for non-network logins only (login, su)
+ : (wheel) (ops) : 10.20.0.0/16     # groups in parentheses
+ : backup : 10.30.5.10              # one host
+ : root : cron crond                # PAM service names are valid origins when there is no tty
- : ALL : ALL                        # everything else denied
```
Origins: tty names (non-network logins), X `$DISPLAY` values or PAM service names (non-network logins
without a tty), host names, domain names (leading dot), IP addresses, network/netmask, `ALL`, `LOCAL`, `EXCEPT`.
`LOCAL` matches non-network connections (su, login); `ssh user@localhost` is a network connection and does
not match. Group entries are written in brackets, `(group)`; with `nodefgroup` unset, a bare name that is not
the login name is also looked up as a group.

## 3. pam_time: /etc/security/time.conf
Add `account required pam_time.so` to the service's file.
`services;ttys;users;times`
```
sshd;*;contractor1|contractor2;Wk0800-1800
login;tty*;!root;!Al0000-2400        # `!` negates; users may be combined with `|` and `&`
```
Days `Mo Tu We Th Fr Sa Su`, `Wk` weekdays, `Wd` weekend, `Al` all; times are `HHMM-HHMM` (an end time earlier
than the start applies into the next day). pam_time provides only the account management type, so it is
evaluated when access is requested.

## 4. Simpler alternatives
- sshd only: `AllowGroups ops wheel` / `Match Address` blocks in sshd_config — easier to audit.
- sssd: `access_provider = simple` with `simple_allow_groups` (any matching deny rule beats an allow rule).

## Gotchas
- Missing final `- : ALL : ALL` = allow-by-default (rules only deny what they match).
- A rule that denies the account cron/systemd run as can break jobs that go through PAM account checks.
- Hostname origins depend on DNS at login; the `nodns` option (Linux-PAM 1.7.1 and later) stops tokens being
  resolved as host names, so use IP addresses.
- Test with a second session open; a wrong rule locks out admins too.

## Verify
- [ ] Login from a non-admin network as an ops user is refused and the log shows a pam_access denial.
- [ ] Allowed users/networks still log in; root only on console.

## Checked
Checked 2026-10-25 against the Linux-PAM source documentation (master branch, NEWS up to 1.7.x) and the authselect sssd profile README.
Confirmed: origin types and the LOCAL/localhost rule, bracketed group syntax and `nodefgroup`, first-match evaluation, `nodns` added in 1.7.1, the time.conf `services;ttys;users;times` grammar with Wk/Wd/Al day codes, `!`, `|` and `&` operators, authselect feature `with-pamaccess`, and sssd `simple_allow_groups`.
Removed as unconfirmed: the claim that pam_time cannot end running sessions, and the exact journal wording of denials.

Method: documentation only; no commands were run.
