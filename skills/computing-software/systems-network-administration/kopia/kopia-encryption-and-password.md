---
id: computing-software.systems-network-administration.kopia.kopia-encryption-and-password
name: kopia-encryption-and-password
category: computing-software
field: systems-network-administration
product: kopia
tags: [encryption, aes256-gcm, chacha20, change-password, scrypt, envelope-encryption]
level: practitioner
status: docs-checked
description: "How Kopia encrypts repositories, which algorithms exist, why they cannot change later, and how to change the repository password."
sources: ["https://kopia.io/docs/advanced/encryption/", "https://kopia.io/docs/faqs/", "https://kopia.io/docs/repositories/", "https://kopia.io/docs/upgrade/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Encryption is per repository and always on. Kopia uses envelope encryption: the repository passphrase is turned into a key by scrypt (N=65536, r=8, p=1 is the only supported function today), and that key decrypts a format blob holding the real content-encryption secrets. This decouples the passphrase from the data keys.

The format blob is JSON containing tool and version fields, a random `uniqueID`, `keyAlgo`, the `encryption` algorithm used for the block format and the encrypted block format itself.

## Algorithms

The default is `AES256-GCM-HMAC-SHA256`; `CHACHA20-POLY1305-HMAC-SHA256` is available. Pick one when the repository is created (in KopiaUI use Show Advanced Options). It cannot be changed afterward.

## Password

There is no recovery if you lose the password. To change it, use the CLI while connected: `kopia repository change-password`. You cannot reset a forgotten password if you are not still connected, because the current password is needed. GUI password change is not supported. Per the upgrade notes, after the v0.9 index upgrade password change is available only for newly created repositories.

The storage backend password (S3 secret, WebDAV password) is separate from the repository password and the repository password should not equal it.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Encryption (envelope encryption, scrypt 65536/8/1, format blob fields), FAQ (default AES256-GCM-HMAC-SHA256, CHACHA20 option, no change after creation, no recovery, change-password only while connected, CLI only), Repositories (Show Advanced Options) and Upgrade (password change only on newly created repositories).
Method: documentation only; no commands were run.
