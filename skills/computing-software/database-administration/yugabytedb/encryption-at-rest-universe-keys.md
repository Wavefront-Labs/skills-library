---
id: computing-software.database-administration.yugabytedb.encryption-at-rest-universe-keys
name: encryption-at-rest-universe-keys
category: computing-software
field: database-administration
product: yugabytedb
tags: [encryption-at-rest, universe-key, key-rotation, add-universe-key-to-all-masters, is-encryption-enabled, openssl-rand, snapshots]
level: advanced
status: docs-checked
description: "Turn on and rotate encryption at rest with yb-admin universe keys, check status, and keep every key because snapshot restores to new clusters need them."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/encryption-at-rest.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/admin/yb-admin.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Encryption at rest with universe keys

Enable with a self-generated key:
1. Generate it with a key size of 32, 40 or 48 bytes: `openssl rand -out /path/to/universe_key 32`
2. Push it to all masters:
```
yb-admin --master_addresses $MASTERS add_universe_key_to_all_masters <key_id> /path/to/universe_key
yb-admin --master_addresses $MASTERS all_masters_have_universe_key_in_memory <key_id>
yb-admin --master_addresses $MASTERS rotate_universe_key_in_memory <key_id>
yb-admin --master_addresses $MASTERS is_encryption_enabled
```
The key lives only in master memory; the plaintext key is never persisted to disk. Larger keys are more secure with slightly worse performance.

Rotate by generating a new key file at a different path, adding it with `add_universe_key_to_all_masters` under a key id that differs from every previous one, and running `rotate_universe_key_in_memory <new_key_id>`; confirm with `is_encryption_enabled`, which should print `Encryption status: ENABLED with key id <new_key_id>`.

Disable: the Encryption at rest page shows `yb-admin --master_addresses $MASTERS disable_encryption`, but the yb-admin reference documents `disable_encryption_in_memory` (these two official pages disagree on the command name), so try the one your release's `yb-admin --help` lists. Verify with `is_encryption_enabled` (expect `Encryption status: DISABLED`). Disabling stops encryption of new data; data already on disk stays encrypted until compaction rewrites it, and the cluster still needs the keys to read it.

Caveats:
- Only new data is encrypted at first. Existing files are re-encrypted as compaction rewrites them.
- Keep all keys, including rotated ones, in secure storage. To restore a distributed snapshot of an encrypted cluster onto another cluster, copy every key used.
- Disk-level encryption software must be running before YugabyteDB starts.

## Checked

2026-11-04. Confirmed against the Encryption at rest page (key lengths 32, 40 or 48 with `openssl rand -out`, add_universe_key_to_all_masters, all_masters_have_universe_key_in_memory, rotate_universe_key_in_memory, is_encryption_enabled output, rotation, background encryption on flush and compaction, keep rotated keys, third-party disk encryption must be running before YugabyteDB starts) and the yb-admin reference. Conflict: the encryption page shows `disable_encryption` while the yb-admin reference lists `disable_encryption_in_memory`; the skill says so.

Method: documentation only; no commands were run.
