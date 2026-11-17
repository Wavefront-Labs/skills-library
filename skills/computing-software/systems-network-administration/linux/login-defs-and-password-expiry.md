---
id: computing-software.systems-network-administration.linux.login-defs-and-password-expiry
name: login-defs-and-password-expiry
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, users-groups, login-defs, password-expiry, pass-max-days, pass-min-days, pass-warn-age, chage, uid-min, encrypt-method, password-aging, rhcsa, lpic-1, sysadmin]
level: practitioner
status: gated
description: "Set site-wide account policy in /etc/login.defs (PASS_MAX_DAYS, UID ranges, ENCRYPT_METHOD, UMASK) and apply password expiry to existing users with chage."
sources:
  - https://github.com/shadow-maint/shadow/blob/master/man/login.defs.5.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/chage.1.xml
  - https://github.com/shadow-maint/shadow/blob/master/man/passwd.1.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# login.defs and password expiry

**Goal:** password aging and account defaults that match policy — and the step everyone forgets:
login.defs only affects accounts created **after** the change.

## 1. /etc/login.defs keys that matter
```
PASS_MAX_DAYS   365      # max days a password may be used (-1 or unset disables the limit)
PASS_MIN_DAYS   1        # min days between changes (gated: unconfirmed, source is paywalled or blocked)
PASS_WARN_AGE   7        # warning days before expiry
UID_MIN / UID_MAX / SYS_UID_MIN / SYS_UID_MAX   # ranges for useradd and useradd -r (values are distribution-specific)
GID_MIN / GID_MAX …
ENCRYPT_METHOD  YESCRYPT # BCRYPT, SHA256, SHA512 (default) or YESCRYPT; see the note below
UMASK           077      # file creation mask; HOME_MODE falls back to it
HOME_MODE       0700     # mode for new home directories
USERGROUPS_ENAB yes      # user private group; userdel removes an empty one
CREATE_HOME     yes
```
The current shadow manual does not document `PASS_MIN_DAYS`, so that key cannot be confirmed from documentation; check the login.defs shipped by your distribution.
Length and complexity belong in pam_pwquality. `ENCRYPT_METHOD` only affects the generation of group passwords:
user password hashing is done by PAM and follows the PAM configuration (for example the `pam_unix` hashing
option), so keep them consistent.

## 2. Apply aging to existing accounts
```bash
chage -l alice                           # current aging info
chage -M 365 -W 7 alice                  # max days and warning days
chage -I 30 alice                        # inactive days after expiry before the account is locked
chage -E 2026-12-31 contractor1          # account expiry date (YYYY-MM-DD or days since 1970-01-01)
chage -d 0 alice                         # last-change date 0: forces a change at next login
```
`passwd -x 365 -w 7 alice` sets the same maximum and warning values (`-x` is `--maxdays`). Loop over your own list of regular accounts to apply them to existing users. The minimum-days option `chage -m` (gated: unconfirmed, source is paywalled or blocked); the current shadow manual does not document it, so check `chage --help` on the host.

## 3. Check compliance
Run `chage -l <user>` for each regular account and compare the maximum, warning and inactive values with policy.

## Gotchas
- Service accounts with expiring passwords break later — use locked passwords + keys, or `chage -M -1`.
- Centrally managed users (sssd/IPA/AD) follow the directory's policy, not login.defs/chage.
- Changing the hashing configuration does not rehash existing passwords; they upgrade when users next change them.

## Verify
- [ ] `grep -E '^PASS_(MAX|MIN|WARN)' /etc/login.defs` matches policy.
- [ ] `chage -l` for a sample of existing users shows the same values (not just new ones).
- [ ] A test user created now gets them automatically.

## Checked
Checked 2026-10-25 against shadow-maint/shadow master and release 4.20.3 manual sources (login.defs(5), chage(1), passwd(1)).
Confirmed: PASS_MAX_DAYS (default -1), PASS_WARN_AGE, ENCRYPT_METHOD values and default and the note that user passwords are hashed by PAM, SHA_CRYPT_MIN_ROUNDS and YESCRYPT_COST_FACTOR, UMASK, HOME_MODE falling back to UMASK, USERGROUPS_ENAB, CREATE_HOME, chage `-M`, `-W`, `-I`, `-E`, `-d`, `-l`, and `passwd -x`.
Corrected: ENCRYPT_METHOD does not control user password hashing. Removed: the CIS and NIST statements, example UID/GID range values and the awk bulk and compliance scripts.
Gated: `PASS_MIN_DAYS` and `chage -m` carry the gated marker because neither appears in the current shadow manuals (the upstream history records the `-m` documentation as removed).

Method: documentation only; no commands were run.
