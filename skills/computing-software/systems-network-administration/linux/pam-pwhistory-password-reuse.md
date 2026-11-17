---
id: computing-software.systems-network-administration.linux.pam-pwhistory-password-reuse
name: pam-pwhistory-password-reuse
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pam, pwhistory, password-history, pam-pwhistory, opasswd, password-policy, cis-benchmark]
level: practitioner
status: docs-checked
description: "Prevent password reuse with pam_pwhistory: remember= count, pwhistory.conf, correct stack position with authselect or pam-auth-update, enforce_for_root and /etc/security/opasswd."
sources:
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_pwhistory/pam_pwhistory.8.xml
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_pwhistory/pwhistory.conf.5.xml
  - https://github.com/linux-pam/linux-pam/blob/master/modules/pam_unix/pam_unix.8.xml
  - https://github.com/authselect/authselect/blob/master/profiles/sssd/system-auth
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pam_pwhistory

## Configure (the config file is the preferred method)
`/etc/security/pwhistory.conf`:
```
remember = 24          # default is 10
enforce_for_root
retry = 3              # default is 1
# file = /etc/security/opasswd   (default)
```
## Stack placement
The module goes in the **password** stack, after pwquality and before pam_unix:
```
password    requisite     pam_pwquality.so
password    required      pam_pwhistory.so use_authtok
password    sufficient    pam_unix.so yescrypt shadow use_authtok
```
- RHEL: `authselect enable-feature with-pwhistory` (a feature of the sssd profile; it adds pam_pwhistory with
  `use_authtok` ahead of pam_unix) — don't hand-edit authselect-managed files; otherwise create a custom
  profile (`authselect create-profile`).
- Debian/Ubuntu: insert the same line in the password stack of `common-password` before pam_unix.
- pam_unix also has `remember=n` (it also keeps history in /etc/security/opasswd) — use one mechanism, not both.

## Storage
`/etc/security/opasswd` is the default history file (the `file=` option or `file` in pwhistory.conf changes it).
Only password changes that go through the PAM password stack are recorded.

## Gotchas
- `use_authtok` needs a previous module (pwquality) to have prompted; otherwise you'll get no prompt/odd errors.

## Verify
- [ ] Changing a test user's password back to a recent one is refused; the history file gains an entry after each successful change.

## Checked
Checked 2026-10-25 against Linux-PAM master docs and the authselect sssd system-auth template.
Confirmed: pwhistory.conf is the preferred configuration method, option names and defaults (remember 10, retry 1, enforce_for_root, file default /etc/security/opasswd), `use_authtok`, pam_unix `remember=n`, and the authselect `with-pwhistory` feature.
Removed as unconfirmed: the opasswd file mode, the claim that chpasswd and usermod bypass history, the SSSD/LDAP exemption, the exact error text and the Debian pam-configs path.

Method: documentation only; no commands were run.
