---
id: computing-software.cybersecurity-defensive.keycloak.password-policy-and-hashing
name: password-policy-and-hashing
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, password-policy, hashing, argon2, pbkdf2]
level: practitioner
status: docs-checked
description: "Set realm password policies in Keycloak: hashing algorithm and iterations, complexity, expiry, history, blacklist files, and bringing existing users onto new rules."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/server_admin/topics/authentication/password-policies.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# password policy and hashing
A new realm has no password policy, so simple passwords with no length or complexity limit are accepted. Add policies under *Authentication* > *Policies* tab: pick one in *Add policy*, enter a value, *Save*. The policy applies to new passwords; existing users are unaffected, so set it from realm creation, or use the "Update password" required action, or "Expire password" to make users change within N days.

Hashing (policy `HashAlgorithm`): `argon2` (default for non-FIPS), `pbkdf2-sha512` (default for FIPS), `pbkdf2-sha256`, `pbkdf2` (SHA1, deprecated). Argon2 is highly recommended: much lower CPU needs than PBKDF2 and more secure. Server default: `--spi-password-hashing--provider-default=<algorithm>`. Argon2 parallel hashing is limited by default to the cores available to the JVM; it has its own provider options. Changing the algorithm does not change stored hashes until the user logs in.

Hashing iterations: default -1 uses the algorithm default: argon2 5, pbkdf2-sha512 210,000, pbkdf2-sha256 600,000, pbkdf2 1,300,000. Usually do not change them: lower values are insecure, higher values cost CPU.

Other policy types: Digits, Lowercase characters, Uppercase characters, Special characters, Not username, Not email, Regular expression (Java patterns), Expire password (days), Not recently used (history), Not recently used (In Days), Password blacklist, Maximum Authentication Age.

Password blacklist: UTF-8 plain-text files with Unix line endings, one password per line, compared case-insensitively. The policy value is the file name (for example `100k_passwords.txt`), resolved against `${kc.home.dir}/data/password-blacklists/` unless changed by the `keycloak.password.blacklists.path` system property or `--spi-password-policy--password-blacklist--blacklists-path=/path/to/blacklistsFolder`. Files reload when modified (checked at most every 60 seconds; `--spi-password-policy--password-blacklist--check-interval-seconds=<seconds>`, 0 disables); update them atomically. It uses a Bloom filter, so false positives are possible (default probability 0.01%; `--spi-password-policy--password-blacklist--false-positive-probability=0.00001`). For large lists pre-compute the filter: `bin/kc.sh tools build-password-denylist /path/to/100k_passwords` (optional `--fpp 0.00001`) writes a `.bloom` file; put it in the folder and use its name in the policy.

Maximum Authentication Age: seconds a user can update a password without re-authenticating; 0 always requires re-authentication. The docs prefer configuring it on the Update Password required action, since the policy may be deprecated or removed.

## Checked
2026-11-03. Confirmed against server_admin/topics/authentication/password-policies.adoc. Removed: the "confirm the list for your version" hedge, the DoS-vector gotcha wording and the Verify step; added the blacklist and Maximum Authentication Age details.
Method: documentation only; no commands were run.
