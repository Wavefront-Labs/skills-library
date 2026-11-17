---
id: computing-software.systems-network-administration.borg.borg-init-encryption-modes
name: borg-init-encryption-modes
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borgbackup, borg-init, encryption, repokey, keyfile, blake2, authenticated]
level: practitioner
status: docs-checked
description: "Create a Borg repository and choose an encryption mode (repokey, keyfile, authenticated, blake2 variants) with the options, quota and append-only flags of borg init."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/init.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg init and encryption modes

`borg init --encryption=MODE REPOSITORY` creates a repository. `-e/--encryption` is required, and the mode can only be set at creation: it cannot be changed per archive or later.

| Mode | Hash/MAC | Encryption | Key stored |
|---|---|---|---|
| `none` | SHA-256 | none | n/a (avoid; no authentication) |
| `authenticated` | HMAC-SHA256 | none | in repo |
| `authenticated-blake2` | BLAKE2b-256 | none | in repo |
| `repokey` | HMAC-SHA256 | AES-CTR-256, encrypt-then-MAC | in repo |
| `keyfile` | HMAC-SHA256 | AES-CTR-256 | local keys directory |
| `repokey-blake2` | BLAKE2b-256 | AES-CTR-256 | in repo |
| `keyfile-blake2` | BLAKE2b-256 | AES-CTR-256 | local keys directory |

The blake2 and authenticated modes need Borg 1.1+. The docs recommend `repokey` with a strong passphrase, or `repokey-blake2` if the CPU lacks hardware SHA-256. With `keyfile` modes, losing the local key means losing the repository, so keep an offsite copy made with `borg key export`; a copy on the backed-up machine is not enough.

Encryption happens on the client; a remote host never sees the passphrase or unencrypted key. Use long ASCII passphrases because keyboard layouts can change non-ASCII input.

Other options: `--append-only`, `--storage-quota 5G`, `--make-parent-dirs`.

```
borg init --encryption=repokey-blake2 /path/to/repo
borg init --encryption=keyfile user@hostname:backup
```

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/init): mode table, hash/MAC and cipher details, Borg 1.1+ requirement, passphrase and key-backup advice, options. Removed: nothing.

Method: documentation only; no commands were run.
