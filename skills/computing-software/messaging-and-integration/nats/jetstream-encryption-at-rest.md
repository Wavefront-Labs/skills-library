---
id: computing-software.messaging-and-integration.nats.jetstream-encryption-at-rest
name: jetstream-encryption-at-rest
category: computing-software
field: messaging-and-integration
product: nats
tags: [encryption-at-rest, chachapoly, aes, jetstream-key, tpm, cipher]
level: practitioner
status: docs-checked
description: "Encrypt JetStream stores with cipher chachapoly or aes and a key from an env var; TPM on Windows; enabling and key-change behavior."
sources:
  - https://github.com/nats-io/nats.docs/blob/master/running-a-nats-service/nats_admin/jetstream_admin/encryption_at_rest.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt JetStream message blocks and metadata on disk.

Supported since server 2.3.0; the docs recommend filesystem-level encryption where available (optimized for throughput, no secret management in NATS). Server-side encryption covers message blocks (headers and payloads) and stream and consumer metadata files.

Ciphers: `chachapoly` (ChaCha20-Poly1305) or `aes` (AES-GCM). Config in the `jetstream` block:
```
jetstream : {
  cipher: chachapoly
  key: $JS_KEY
}
```
Provide the key from the environment so it is not persisted in a file, for example `JS_KEY="<secret>" nats-server -c js.conf`.

TPM on Windows (2.11.0+): `jetstream { store_dir: nats  max_file_store: 10G  tpm { keys_file: "keys"  encryption_password: "<password>" } }`. `keys_file` and `encryption_password` are required (if the file does not exist a key is created and sealed in the TPM); `srk_password` is optional; `pcr` defaults to 22 (choose 17 to 23; 0-16 reserved); `cipher` defaults to `chachapoly`.

Changing settings: enabling on a server with existing data is allowed but old blocks stay unencrypted; only new blocks are encrypted. To encrypt old data, back up the stream and restore it. If you restart with a different key or with encryption disabled, the server cannot decrypt existing blocks and logs errors when loading.

## Checked

2026-11-03. Read against the nats.docs repository (the pages listed in `sources`, plus the neighbouring concept, release-note and nsc/nk tool pages): configuration keys, flags, CLI commands, defaults, limits, subjects, header names and version gates were confirmed there.
Removed: the unsourced Verify step, plus statements that no page supports (see the PR notes for the per-skill list).
Method: documentation only; no commands were run.
