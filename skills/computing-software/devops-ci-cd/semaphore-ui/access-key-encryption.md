---
id: computing-software.devops-ci-cd.semaphore-ui.access-key-encryption
name: access-key-encryption
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [encryption, access-key-encryption, secrets, key-store, security, semaphore-ui]
level: practitioner
status: docs-checked
description: "Protect stored credentials with access_key_encryption and the encryption.keys_file registry (AES-256-GCM)."
sources:
  - https://semaphoreui.com/docs/admin-guide/security/encryption
  - https://semaphoreui.com/docs/admin-guide/security/database
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Encrypt stored secrets

Goal: make sure Key Store secrets in the database are encrypted.

Simple form: set `access_key_encryption` (or `SEMAPHORE_ACCESS_KEY_ENCRYPTION`) to a key generated with:

```bash
head -c32 /dev/urandom | base64
```

With no key configured, secrets are stored as plain base64.

Key registry (AES-256-GCM, protects Access Key secrets and the JWT signing key):

```yaml
encryption:
  keys_file: /etc/semaphore/encryption-keys.yml
```

```yaml
keys:
  key1: { value: "REPLACE_WITH_openssl_rand_-base64_32" }
  key2: { file: /run/secrets/secret_key }
active:
  secret_key: key1
  option_key: key2
```

Generate registry keys with `openssl rand -base64 32`; each must be base64 of 16, 24 or 32 bytes. The file is parsed as YAML or JSON regardless of extension. Prefer `file:` entries or a `keys_folder` (every regular file is one key, named by filename, ideal for mounted Kubernetes secrets) over inline values. If no option key is set, the secrets key is used.

Key ids are fingerprints (`base64url(sha256(key))[:8]`) stored with each ciphertext, so labels can be renamed freely and a missing key fails loudly.

Backward compatible: an existing `access_key_encryption` becomes the active secrets key; old data without a key id still decrypts.

Gotcha: losing the key means losing every stored credential, so back it up separately from the database.

Verify: `semaphore vault check --config /path/to/config.yml` lists rows per key id.

## Checked

2026-11-04: checked against the Semaphore encryption and database security pages. Removed the unconfirmed 32-byte key wording; registry keys are base64 of 16, 24 or 32 bytes. The old source URL was incomplete and is replaced.

Method: documentation only; no commands were run.
