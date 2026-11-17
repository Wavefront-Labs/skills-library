---
id: computing-software.systems-network-administration.linux.pam-pwquality-password-complexity
name: pam-pwquality-password-complexity
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pam, pwquality, pam-pwquality, password-complexity, pwquality-conf, pam-pwhistory, password-reuse, authselect, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Enforce password length, complexity, dictionary checks and reuse limits with pam_pwquality and pam_pwhistory: pwquality.conf, root enforcement and PAM wiring per distro."
sources:
  - https://github.com/libpwquality/libpwquality/blob/master/doc/man/pwquality.conf.5.pod
  - https://github.com/libpwquality/libpwquality/blob/master/doc/man/pam_pwquality.8.pod
  - https://github.com/libpwquality/libpwquality/blob/master/doc/man/pwscore.1.pod
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_pwhistory/pwhistory.conf.5.xml
  - https://github.com/authselect/authselect/blob/master/profiles/sssd/system-auth
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# pam_pwquality: password complexity and reuse

**Goal:** reject weak or reused local passwords at `passwd` time, configured in one file and
consistent with your policy.

## 1. Settings: /etc/security/pwquality.conf (or pwquality.conf.d/*.conf)
```ini
minlen = 14            # credits shorten the effective minimum unless the credit settings are 0 or negative (default 8)
minclass = 3           # require 3 of 4 classes (digits, upper, lower, other)  — or use the credits below
dcredit = -1           # negative = at least one digit required
ucredit = -1
lcredit = -1
ocredit = -1
maxrepeat = 3          # no more than 3 identical consecutive characters
maxclassrepeat = 4
dictcheck = 1          # cracklib dictionary check
usercheck = 1          # reject passwords containing the username
difok = 5              # characters that must differ from the old password (default 1)
enforce_for_root       # root gets errors too (otherwise only warnings)
retry = 3
```
Test without changing anything: `echo 'Summer2026!' | pwscore`.

## 2. PAM wiring
- **RHEL/Fedora:** already in the `sssd`/`minimal` authselect profiles' `system-auth` and
  `password-auth`: `password requisite pam_pwquality.so local_users_only`. Don't hand-edit
  those files (authselect overwrites them) — change `pwquality.conf`.
- **Debian/Ubuntu:** place `password requisite pam_pwquality.so retry=3` in the password stack before `pam_unix.so`
  (packaging is distribution-specific; confirm in the distribution's documentation).

## 3. Reuse: pam_pwhistory
```ini
# /etc/security/pwhistory.conf
remember = 5
enforce_for_root
```
RHEL: `authselect enable-feature with-pwhistory`. Debian: add
`password required pam_pwhistory.so use_authtok remember=5` before pam_unix in common-password.
History is stored in `/etc/security/opasswd` by default.

## 4. Try it
```bash
passwd testuser       # as root: with enforce_for_root a failed check is an error, otherwise only a warning
su - testuser -c passwd
```

## Gotchas
- Module arguments on the PAM line override pwquality.conf — check both (`grep pwquality /etc/pam.d/*`).
- `local_users_only` skips the quality test for users not in /etc/passwd (the module still prompts).
- Credits: with `dcredit=1` (positive), a digit counts as an extra character toward minlen — makes "minlen" shorter than you think.

## Verify
- [ ] `passwd` rejects "password123", a dictionary word, and a password containing the username.
- [ ] Reusing one of the last 5 passwords is refused.

## Checked
Checked 2026-10-25 against libpwquality master docs (pwquality.conf(5), pam_pwquality(8), pwscore(1)), Linux-PAM pwhistory.conf(5) and the authselect sssd system-auth template.
Confirmed: option names and defaults (minlen 8, difok 1, dictcheck 1, usercheck, minclass, maxclassrepeat, credits), enforce_for_root and local_users_only semantics, that module arguments override the config file, pwscore returning a 0-100 score, and `pam_pwquality.so local_users_only` in the RHEL sssd template.
Removed as unconfirmed: the NIST 800-63B statement, Debian package wiring detail, bypass claims for chpasswd/usermod and exact error wording.

Method: documentation only; no commands were run.
