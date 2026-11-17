---
id: computing-software.email-administration.dovecot.password-scheme-selection-and-encoding
name: password-scheme-selection-and-encoding
category: computing-software
field: email-administration
product: dovecot
tags: [password-scheme, doveadm-pw, argon2, bcrypt, weak-schemes, passdb-default-password-scheme]
level: practitioner
status: docs-checked
description: "Choose a Dovecot password scheme, generate hashes with doveadm pw, override per password with a prefix, and know which weak schemes are disabled."
sources:
  - https://doc.dovecot.org/main/core/config/auth/schemes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A password scheme is the format in which a password is stored in the passdb. Choosing something other than PLAIN stops someone who reads the database from reusing passwords elsewhere. Pick the strongest scheme your system supports.

Strongest first: ARGON2ID and ARGON2I (need a recent libsodium, and a lot of virtual memory, so raise `service auth { vsz_limit }` to about 2G), then bcrypt (`BLF-CRYPT`, hashes start with `$2y$`, bundled with Dovecot), then `SHA512-CRYPT` (`$6$`) and `SHA256-CRYPT` (`$5$`). MD5-based schemes (except DIGEST-MD5 and CRAM-MD5), LANMAN and NTLM are weak and disabled unless you set `auth_allow_weak_schemes = yes`.

Generate hashes with `doveadm pw`. The default scheme is CRYPT in bcrypt format; select another with `-s`, for example `doveadm pw -s SHA512-CRYPT`. Use `-p` for scripted input, and `-r` to tune the cost of Argon2 or bcrypt. Run `doveadm -O pw` when no config exists yet.

Set the default for a passdb with `passdb_default_password_scheme`. Override it for a single password with a prefix such as `{PLAIN}pass`. Append `.hex` or `.b64` to change the encoding, for example `{PLAIN.b64}`, which helps when a character like a colon is illegal in a passwd-file.

Exceptions: the passwd passdb always uses CRYPT, and with BSD auth Dovecot never sees the password. You cannot convert hashes in bulk; change them as users log in.

## Checked
2026-11-09. Read the Dovecot Password Schemes page (main documentation) in full. Confirmed: scheme ordering and hash
prefixes, libsodium and the `vsz_limit = 2G` recommendation, bcrypt bundled, weak-scheme list and
`auth_allow_weak_schemes`, `doveadm pw` options (-s, -p, -r, -O), default CRYPT in bcrypt format,
`passdb_default_password_scheme`, per-password prefixes and `.hex`/`.b64` suffixes, the passwd/PAM/BSD exceptions,
and the no-bulk-conversion note. Nothing removed.
Method: documentation only; no commands were run.
