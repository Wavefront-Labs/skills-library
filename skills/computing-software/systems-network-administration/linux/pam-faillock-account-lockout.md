---
id: computing-software.systems-network-administration.linux.pam-faillock-account-lockout
name: pam-faillock-account-lockout
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pam, faillock, pam-faillock, account-lockout, brute-force, faillock-conf, authselect, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Lock accounts after repeated failed logins with pam_faillock: faillock.conf (deny, unlock_time, root), enabling via authselect or common-auth, and inspecting/resetting lockouts."
sources:
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_faillock/pam_faillock.8.xml
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_faillock/faillock.conf.5.xml
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_faillock/faillock.8.xml
  - https://github.com/linux-pam/linux-pam/blob/master/NEWS
  - https://github.com/authselect/authselect/blob/master/profiles/sssd/system-auth
  - https://github.com/openssh/openssh-portable/blob/master/sshd_config.5
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pam_faillock: account lockout

**Goal:** slow down password guessing against local accounts without creating an easy
denial-of-service against admins.

## 1. Policy: /etc/security/faillock.conf
```ini
deny = 5               # failures before lock
fail_interval = 900    # counting window (s)
unlock_time = 600      # auto-unlock after 10 min (0 = admin must unlock — DoS risk)
even_deny_root         # also lock root …
root_unlock_time = 60  # … but briefly
audit                  # log usernames of unknown users
silent                 # print no informative messages; without it, existing and unknown users behave differently
dir = /var/run/faillock   # default tally directory; on tmpfs it is cleared at reboot (set dir elsewhere to persist)
```

## 2. Enable
**RHEL 8/9, Fedora:**
```bash
authselect current
authselect enable-feature with-faillock
authselect apply-changes
grep faillock /etc/pam.d/system-auth /etc/pam.d/password-auth
```
**Debian/Ubuntu** (`/etc/pam.d/common-auth`, order matters; adapted from the examples in pam_faillock(8)):
```
auth    required    pam_faillock.so preauth
auth    [success=1 default=ignore] pam_unix.so nullok
auth    [default=die] pam_faillock.so authfail
auth    sufficient  pam_faillock.so authsucc
```
and `account required pam_faillock.so` in `common-account`. Test from a second session
before closing your root shell — a broken auth stack locks everyone out.

## 3. Inspect and unlock
```bash
faillock                    # all users with failures
faillock --user alice       # list failures: time, source (tty/host), valid
faillock --user alice --reset
```

## 4. SSH specifics
- Key-based logins skip the PAM auth stack, so the pam_faillock auth calls do not run for them; with
  `UsePAM yes` sshd still runs PAM account and session modules for every authentication type.
- With `UsePAM yes`, password and keyboard-interactive attempts go through PAM and are counted.
- Pair with fail2ban or sshd `MaxAuthTries` to limit the source rather than locking the account.

## Gotchas
- `pam_tally2` is gone (removed in PAM 1.5) — old guides don't apply.
- `unlock_time=0` + an attacker who knows usernames = all admins locked out. Keep a console/break-glass path.
- Lockouts on tmpfs tally dir vanish at reboot — intended or not, know which.
- Centrally managed users: `local_users_only` tracks only users in /etc/passwd and ignores AD/IdM/LDAP users.

## Verify
- [ ] With `deny = 5`, more than five consecutive bad passwords for a test user lock it (the module denies once failures exceed `deny`); `faillock --user` lists entries.
- [ ] After `unlock_time` (or `--reset`) login succeeds.
- [ ] Root/admin access still possible via console or key-based SSH during lockout.

## Checked
Checked 2026-10-25 against Linux-PAM master docs and NEWS, the authselect sssd system-auth template and OpenSSH portable sshd_config(5).
Confirmed: faillock.conf option names and defaults (deny 3, fail_interval 900, dir /var/run/faillock, unlock_time 0 means never, even_deny_root, root_unlock_time implies even_deny_root, audit, silent, local_users_only), the preauth/authfail/authsucc arguments, `faillock --user --reset`, pam_tally2 removal in 1.5.0, authselect feature `with-faillock`, and the UsePAM account/session behaviour.
Removed as unconfirmed: the /var/lib/faillock path and the journal search for message text.

Method: documentation only; no commands were run.
