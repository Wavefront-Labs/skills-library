---
id: computing-software.database-administration.cockroachdb.encryption-at-rest
name: encryption-at-rest
category: computing-software
field: database-administration
product: cockroachdb
tags: [encryption-at-rest, enterprise-encryption, store-keys, key-rotation, aes]
level: advanced
status: docs-checked
description: "Enable CockroachDB encryption at rest per store with --enterprise-encryption: generate AES key files, rotation period, status check and changing keys."
sources:
  - https://www.cockroachlabs.com/docs/stable/encryption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: encrypt store data on disk and rotate keys safely.

Key files: the algorithm is chosen from the key file size. The file holds a 32-byte key ID plus the key, so sizes are 48 bytes (AES-128), 56 (AES-192) or 64 (AES-256). Generate with either:
```shell
cockroach gen encryption-key -s 128 /path/to/my/aes-128.key
openssl rand -out /path/to/my/aes-128.key 48
```

Enable at node start; the flag applies to one store, so repeat it for each store:
```shell
cockroach start --store=cockroach-data \
  --enterprise-encryption=path=cockroach-data,key=/path/to/my/aes-128.key,old-key=plain
```
Fields: `path` (required, store to encrypt), `key` (required, new key file or `plain`), `old-key` (required, current key file or `plain`), `rotation-period` (optional, automatic data-key rotation interval, default one week).

Change algorithm or key by restarting with the new file as `key` and the previous as `old-key`:
```shell
--enterprise-encryption=path=cockroach-data,key=/path/to/my/aes-256.key,old-key=/path/to/my/aes-128.key
```
Switching `key` to `plain` with the prior file as `old-key` decrypts.

Status: the node's stores report at `https://<node>:8080/#/reports/stores/local` (or node ID) lists encryption status; the percentage encrypted with the current data key drops toward zero after each data-key rotation and then recovers.

Gotchas: once specified for a store, the `--enterprise-encryption` flag must always be present, so the key files must be available at every restart.

Verify: the stores report shows encryption status for each store on the node, and after a data-key rotation the percentage climbs again as data is compacted.

## Checked
2026-11-03. Confirmed on the encryption page: key file sizes of 48, 56 and 64 bytes (32-byte key ID plus 16, 24 or 32 byte key), both generation commands, the `--enterprise-encryption` fields and default one-week `rotation-period`, per-store use, changing algorithm with `key` and `old-key`, `key=plain` to disable, and the stores report URL. Removed: the enterprise-feature and key-loss claims.
Method: documentation only; no commands were run.
