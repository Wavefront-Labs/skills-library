---
id: computing-software.systems-network-administration.rclone.rclone-crypt-password-change-and-verification
name: rclone-crypt-password-change-and-verification
category: computing-software
field: systems-network-administration
product: rclone
tags: [crypt, cryptcheck, password-change, re-encrypt, cryptdecode]
level: advanced
status: docs-checked
description: "Change a crypt password by re-encrypting data, and verify encrypted data with cryptcheck."
sources: ["https://rclone.org/crypt/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Changing the password

Encryption keys derive directly from the client-side password, so existing content cannot be re-keyed. Changing the password on an existing crypt remote just makes old content undecryptable. The documented options:

1. If a plaintext copy exists elsewhere, delete the encrypted files, change the password (or delete and recreate the crypt remote) and re-upload.
2. If there is space, create a new crypt remote pointing to a separate directory on the same backend, `rclone copy` from the old crypt remote to the new one (decrypting with the old password and encrypting with the new one on the fly), then delete the old directory and config. All data streams through your machine, so you use half the bandwidth and are charged twice if upload and download are metered.

## Verifying

The `rclone check` documentation points to the dedicated `rclone cryptcheck` command for crypt remotes, which is able to check the checksums of the encrypted files.

## Tracking renames on crypt

`--track-renames` with the default `hash` strategy is not supported on encrypted destinations, but `--track-renames-strategy modtime` or `leaf` works.

## Layout example

With standard name encryption the underlying listing shows scrambled names with directory structure preserved, for example `hagjclgavj2mbiqm6u6cnjjqcg` for a top-level file and an encrypted directory containing encrypted subpaths, while `rclone ls secret:subdir` shows `subsubdir/file4.txt`. Without name encryption the underlying names gain `.bin`.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
