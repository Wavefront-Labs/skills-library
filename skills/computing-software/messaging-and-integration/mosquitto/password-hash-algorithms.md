---
id: computing-software.messaging-and-integration.mosquitto.password-hash-algorithms
name: password-hash-algorithms
category: computing-software
field: messaging-and-integration
product: mosquitto
tags: [password-hash, argon2id, sha512-pbkdf2, upgrade]
level: practitioner
status: docs-checked
description: "Choose the hash used by mosquitto_passwd (-H) and convert plain-text password files with -U, noting the risk of re-running it."
sources:
  - https://mosquitto.org/man/mosquitto_passwd-1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right password hash and convert legacy files safely.

The `-H hash` option selects the hash: `argon2id`, `sha512-pbkdf2`, or `sha512`. It defaults to `argon2id`. The `sha512` option exists for creating password files for use with Mosquitto 1.6 and earlier.

```
mosquitto_passwd -H sha512 /path/to/passwd ral
```

That command adds a user to an existing file using the sha512 hash for 1.6 compatibility.

`-U passwordfile` upgrades or converts a file containing plain-text passwords into one with hashed passwords. It modifies the file in place. Critically, it does not detect whether passwords are already hashed, so running it on a file that already holds hashed passwords generates new hashes based on the old hashes and renders the password file unusable.

Because of that behaviour, `-U` is for a plain-text file only.

Passwords in the file are stored in a format similar to crypt(3).

## Checked

2026-11-08. Confirmed against the mosquitto_passwd man page: -H values and argon2id default, sha512 for Mosquitto 1.6 and earlier, and the -U in-place conversion and its warning about already-hashed files. Removed a closing claim about plain-text lines in builds without TLS, which the page does not state.

Method: documentation only; no commands were run.
