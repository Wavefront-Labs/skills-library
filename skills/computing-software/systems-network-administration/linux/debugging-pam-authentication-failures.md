---
id: computing-software.systems-network-administration.linux.debugging-pam-authentication-failures
name: debugging-pam-authentication-failures
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pam, pam-debugging, pam-stack, authentication-failure, pamtester, sssd, faillock]
level: advanced
status: docs-checked
description: "Find why a login or sudo fails in PAM: reading secure/auth.log, module debug options, pamtester, faillock/expiry/access checks, and safe editing with a root session open."
sources:
  - https://github.com/linux-pam/linux-pam/blob/master/doc/man/pam.conf-syntax.xml
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_unix/pam_unix.8.xml
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_faillock/pam_faillock.8.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/passwd.1.xml
  - https://github.com/SSSD/sssd/blob/master/src/man/sss_cache.8.xml
  - https://github.com/authselect/authselect/blob/master/src/man/authselect.8.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debugging PAM failures

## 1. Read the log for the service
```bash
journalctl -t sshd -t sudo -t login -t su --since -15min
```
Or read the authentication log your syslog configuration writes. Messages are prefixed with the module name and
service (module(service:type)), so they show which module in which stack phase failed.

## 2. Know which file runs
Service name → `/etc/pam.d/<service>` (sshd, sudo, login, su, system-auth/password-auth on RHEL via include,
common-auth/common-account on Debian). Stack order: auth → account → password → session; control flags decide flow.

## 3. Check the usual suspects
```bash
faillock --user alice                 # locked by failures? faillock --user alice --reset
chage -l alice                        # expired password/account
passwd -S alice                       # second field: L locked, NP no password, P usable
grep -v '^#' /etc/security/access.conf
getent passwd alice ; id alice        # resolvable? (SSSD/LDAP)
sss_cache -E ; journalctl -u sssd     # directory users: invalidate all cached entries
```
## 4. Turn on debug
Several modules accept a `debug` argument (for example `pam_unix.so debug`, `pam_access.so debug`,
`pam_pwhistory.so debug`); not all do (pam_faillock has no debug option). Output goes to syslog. Remove afterwards.
## 5. Test without logging in
Open a second login session as the affected user; keep the root session until it succeeds.

## Safety
- Keep a root shell open while editing PAM; test with a second session.
- On RHEL use authselect (`authselect current`, `authselect check`) — manual edits to managed files are overwritten.

## Verify
- [ ] The log shows the failing module; after the fix pamtester and a fresh login both succeed.

## Checked
Checked 2026-10-25 against Linux-PAM master docs, shadow passwd(1), SSSD sss_cache(8) and authselect(8).
Confirmed: `debug` option on pam_unix, pam_access and pam_pwhistory, absence of `debug` in pam_faillock, `faillock --user --reset`, `passwd -S` status codes, `sss_cache -E`, and authselect current/check.
Corrected: pam_faillock has no debug argument. Removed as unconfirmed: exact message texts, distribution log paths, `pam_sss.so debug`, the restorecon step and the pamtester tool.

Method: documentation only; no commands were run.
