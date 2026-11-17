---
id: computing-software.devops-ci-cd.semaphore-ui.encryption-key-rotation
name: encryption-key-rotation
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [key-rotation, vault-rekey, vault-check, sighup, encryption, semaphore-ui]
level: advanced
status: docs-checked
description: "Rotate Semaphore encryption keys with zero downtime using SIGHUP, vault rekey and vault check."
sources:
  - https://semaphoreui.com/docs/admin-guide/security/encryption
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rotate encryption keys without downtime

Goal: move all secrets to a new key and retire the old one.

The active key encrypts new writes; every other key in the registry still decrypts old data.

1. Add a new key to the registry (a file in `keys_folder` or a `keys:` entry) and point `active.secret_key` (or `secret_key_file`) at it.
2. Apply it without restart: Semaphore polls the keys file every `encryption.keys_poll_interval` (default `15s`, `"0"` disables) or reload at once:

```bash
kill -HUP $(pidof semaphore)
```

3. Re-encrypt existing data:

```bash
semaphore vault rekey --config /path/to/config.yml
```

4. Confirm nothing uses the old key:

```bash
semaphore vault check --config /path/to/config.yml
```

5. When the old key shows `0 rows - retired, SAFE TO REMOVE`, delete it from the registry.

Other flags: `vault rekey --backup FILE.jsonl` snapshots ciphertexts, `--rollback FILE.jsonl` restores them, `--old-key <base64>` decrypts legacy un-prefixed data.

Check statuses: `active`, `retired, rekey pending`, `retired, SAFE TO REMOVE`, `legacy (no id)`, `MISSING KEY` (exit code 1).

Gotchas:
- Windows has no SIGHUP; rely on the poller or restart.
- A reload validates new keys first and keeps the running keys on any error.

Verify: `vault check` shows all rows on the new key id.

## Checked

2026-11-04: checked against the encryption security page. Every claim is stated there.

Method: documentation only; no commands were run.
