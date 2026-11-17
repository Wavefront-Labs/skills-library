---
id: computing-software.cryptography-implementation.applied-cryptography.yescrypt-and-sha512crypt-in-shadow
name: yescrypt-and-sha512crypt-in-shadow
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, yescrypt, sha512crypt, crypt3, shadow, libxcrypt, password-hashing]
level: practitioner
status: draft
description: "Manage Unix crypt(3) password hashes: identify yescrypt, sha512crypt and bcrypt prefixes in /etc/shadow, set ENCRYPT_METHOD and rounds, and migrate on login."
sources: ["https://man.archlinux.org/man/crypt.5", "https://www.openwall.com/yescrypt/", "https://manpages.debian.org/bookworm/login/login.defs.5.en.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# yescrypt and sha512crypt in shadow files

## Identify by prefix
| Prefix | Scheme |
|---|---|
| `$y$` | yescrypt (default on Debian 11+, Ubuntu 22.04+, Fedora 35+) |
| `$gy$` | gost-yescrypt |
| `$6$` | sha512crypt (default rounds 5000) |
| `$5$` | sha256crypt |
| `$2b$` | bcrypt (libxcrypt) |
| `$1$` | md5crypt, weak |
| 13 chars no `$` | DES crypt, broken |

## Configure
- `/etc/login.defs`: `ENCRYPT_METHOD YESCRYPT` and `YESCRYPT_COST_FACTOR 5` (1-11), or
  `SHA_CRYPT_MIN_ROUNDS 656000` for sha512crypt.
- PAM: `password ... pam_unix.so yescrypt rounds=5` in `common-password` / `system-auth`.
- Generate a hash: `mkpasswd -m yescrypt` or `openssl passwd -6` (sha512crypt; OpenSSL has no yescrypt).

## Migrate
Hashes change only when a password is set. Force migration via password change at next login (`chage -d 0 user`)
or rely on natural rotation; find old ones with `awk -F: '$2 ~ /^\$(1|5|6)\$/ {print $1}' /etc/shadow`.

## Pitfalls
- Older systems (RHEL 8, Alpine musl) may not verify `$y$` hashes; copying shadow entries between distros breaks
  logins.
- Config management tools that template hashes (Ansible `password_hash`) need a library supporting yescrypt
  (passlib supports sha512_crypt; use `mkpasswd` output for yescrypt).

## Verify
- [ ] `getent shadow user` shows the expected prefix after a password change.
