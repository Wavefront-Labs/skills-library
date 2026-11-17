---
id: computing-software.database-administration.pgbackrest.repository-encryption
name: repository-encryption
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, encryption, repo-cipher-type, repo-cipher-pass, aes-256-cbc]
level: practitioner
status: docs-checked
description: "Enable client-side AES-256 repository encryption with repo-cipher-type and repo-cipher-pass."
sources:
  - https://pgbackrest.org/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt backups and WAL in the repository.

Set a cipher type and a passphrase:

```
[global]
repo1-cipher-type=aes-256-cbc
repo1-cipher-pass=<long random passphrase>
```

`repo-cipher-type` is `none` (default) or `aes-256-cbc`. Encryption is always performed client-side, even if the repository type, such as S3, offers its own encryption. `repo-cipher-pass` encrypts and decrypts repository files.

Rules:

- `info` shows `cipher: aes-256-cbc` (or `none`) per stanza.
- Run without `--stanza`, `info` reads encryption settings only from the global section, so per-stanza settings need `--stanza`.
- `repo-get` automatically decrypts the file it prints.
- The passphrase encrypts and decrypts every repository file, so the same value must be configured wherever the repository is read.

With multiple repositories, each can have its own cipher settings (`repo2-cipher-type`).

Because encryption is client-side, object-store features such as S3 server-side encryption (`repo-s3-kms-key-id`) are separate and do not replace this setting.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html), the pgBackRest Command Reference (pgbackrest.org/command.html) (repo-get) and the pgBackRest User Guide (pgbackrest.org/user-guide.html). Removed: the claim that encryption cannot be changed after stanza-create, which the fetched pages do not state. 

Method: documentation only; no commands were run.
