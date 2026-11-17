---
id: computing-software.cybersecurity-defensive.system-hardening.linux-pam-hardening
name: linux-pam-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [linux-hardening, pam-hardening, pam-faillock, pam-pwquality, authselect, faillock-lockout, password-hashing-yescrypt]
level: practitioner
status: docs-checked
description: "Harden Linux authentication via PAM: faillock lockout, pwquality rules, password history, yescrypt/SHA-512 hashing, authselect profiles, and testing without locking yourself out."
sources: ["https://github.com/linux-pam/linux-pam/blob/master/modules/pam_faillock/faillock.conf.5.xml", "https://github.com/linux-pam/linux-pam/blob/master/modules/pam_faillock/faillock.8.xml", "https://github.com/linux-pam/linux-pam/blob/master/modules/pam_pwhistory/pwhistory.conf.5.xml", "https://github.com/libpwquality/libpwquality/blob/master/src/pwquality.conf", "https://github.com/linux-pam/linux-pam/blob/master/modules/pam_wheel/pam_wheel.8.xml", "https://github.com/linux-pam/linux-pam/blob/master/modules/pam_unix/pam_unix.8.xml", "https://github.com/linux-pam/linux-pam/blob/master/modules/pam_loginuid/pam_loginuid.8.xml", "https://github.com/linux-pam/linux-pam/blob/master/modules/pam_access/pam_access.8.xml", "https://github.com/openssh/openssh-portable/blob/master/sshd_config.5", "https://github.com/authselect/authselect/blob/master/src/man/authselect.8.adoc", "https://github.com/besser82/libxcrypt/blob/develop/doc/crypt.5"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux PAM hardening

## Rule zero: keep a root shell open
Before editing PAM, keep an existing root session open and test logins in a second session. A typo in
`/etc/pam.d/` can lock everyone out (console included).

## RHEL/Fedora: use authselect, not hand edits
```
authselect current
authselect select sssd with-faillock with-pwhistory --force     # or the 'local' profile; --force backs up the current configuration
authselect apply-changes
```
Hand edits to the files authselect generates are overwritten; custom profiles via `authselect create-profile`.
Debian/Ubuntu use a different mechanism (`pam-auth-update`), not covered by the authselect documentation.

## Lockout: pam_faillock (`/etc/security/faillock.conf`)
```
deny = 5
unlock_time = 900
fail_interval = 900
# even_deny_root              # option without a value; enables lockout of root too, so plan console recovery
audit
```
`deny` defaults to 3, `fail_interval` to 900 s and `unlock_time` to 600 s; `unlock_time = 0` means never unlock until `faillock --reset`. Records live in `/var/run/faillock` by default, which is usually cleared at reboot unless `dir` points elsewhere.
Inspect/reset: `faillock --user alice`, `faillock --user alice --reset`.

## Password quality: pam_pwquality (`/etc/security/pwquality.conf`)
```
minlen = 14
minclass = 0                 # minimum number of character classes; 0 disables the requirement
dictcheck = 1                # default is 1 (enabled)
maxrepeat = 3
enforce_for_root             # option without a value: also check root's password changes
```
History: `pam_pwhistory` with `remember = 24` in `/etc/security/pwhistory.conf` (default `remember` is 10; `enforce_for_root` applies the check to root).

## Hashing
`/etc/login.defs` `ENCRYPT_METHOD YESCRYPT` (or `SHA512` with `SHA_CRYPT_MIN_ROUNDS 65536`);
`pam_unix.so ... yescrypt` / `sha512 rounds=65536` (the `rounds=` option applies to SHA-256/512, blowfish, yescrypt and gost-yescrypt). A new hash is written the next time the user changes their password; check
`/etc/shadow` prefixes (`$y$` yescrypt, `$6$` SHA-512; `$1$` md5crypt should not be used for new hashes per crypt(5)).

## Other PAM controls
- `pam_wheel.so use_uid` in `/etc/pam.d/su` to restrict `su` to the wheel group.
- `pam_access` (rules in `/etc/security/access.conf`, then `/etc/security/access.d/*.conf`; the first matching pattern wins) to limit which users and groups log in from where.
- Centralised identity (SSSD/AD/FreeIPA) moves most policy to the directory; PAM still enforces local rules.

## Gotchas
- With `UsePAM yes`, sshd runs PAM account and session processing for all authentication types, including public-key logins (sshd_config(5)), so account modules such as `pam_access` still apply.
- Lockout applies to service accounts too: a misconfigured app retrying can lock out its own account.
- `pam_loginuid` (session module) sets the login UID for audit; use it only in entry-point services such as login, sshd and crond, not in sudo or su.
- Containers rarely use PAM; this is for hosts.

## Verify
With `deny = 5`, repeated bad passwords lock a test user (`faillock --user test` shows entries and `--reset` clears them), a password shorter than `minlen` is
rejected, and a new password hash in `/etc/shadow` starts with `$y$` when yescrypt is configured.

## Checked
Checked 2026-10-25 against Linux-PAM sources and manual pages (linux-pam/linux-pam: faillock.conf(5), faillock(8), pwhistory.conf(5), pam_wheel(8), pam_unix(8), pam_loginuid(8)), libpwquality's sample pwquality.conf, shadow login.defs(5), authselect(8) and its sssd profile README, and libxcrypt crypt(5). Confirmed option names and defaults for pam_faillock (deny 3, fail_interval 900, unlock_time 600, even_deny_root as a flag), pwquality (minlen, minclass, maxrepeat, dictcheck default 1, enforce_for_root as a flag), pwhistory (remember default 10), `pam_wheel use_uid`, yescrypt and sha512 `rounds=`, `ENCRYPT_METHOD` and `SHA_CRYPT_MIN_ROUNDS`, authselect `with-faillock`/`with-pwhistory` features, `--force` backup, `apply-changes`, `create-profile`, and hash prefixes. Wrong claim fixed: `even_deny_root = false` is not valid grammar (the option is a bare flag, so `false` would not disable it). Removed unconfirmed: NIST 800-63B/CIS minclass remarks, the pam_tally2 removal note, Debian pam-configs details and the RHEL 9 profile note. RHEL documentation and the CIS benchmark were not read.

Method: documentation only; no commands were run.
