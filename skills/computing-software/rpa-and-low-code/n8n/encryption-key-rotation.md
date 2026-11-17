---
id: computing-software.rpa-and-low-code.n8n.encryption-key-rotation
name: encryption-key-rotation
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, encryption, key-rotation, credentials, data-encryption-key, downgrade]
level: advanced
status: docs-checked
description: "Rotate n8n data encryption keys safely: two-layer key model, N8N_ENV_FEAT_ENCRYPTION_KEY_ROTATION, UI and API rotation, and the no-downgrade rule."
sources:
  - https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/rotate-encryption-keys
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: replace the key that encrypts credentials without touching the master key. Self-hosted only (all editions), instance owner required. On by default from n8n 3.0; on 2.x opt in.

## Model
- Instance key `N8N_ENCRYPTION_KEY`: master key that never changes; it protects the data keys. Every main and worker must share the same value.
- Data encryption key: encrypts credential data, stored encrypted in the database. Rotation creates a new one for all future writes; old records stay readable and are re-encrypted when next updated.

## Enable on 2.x
Set `N8N_ENV_FEAT_ENCRYPTION_KEY_ROTATION=true` on all instances and restart; n8n generates the initial key. Confirm under **Settings > Data Encryption Keys**.

## Rotate
UI: **Settings > Data Encryption Keys > Rotate key**. API: `POST /encryption/keys`, requiring global scope `encryptionKey:manage`; responses carry metadata only (ID, algorithm, status, timestamps), never key material.

## Danger
Data written under the new format carries a key identifier and older n8n versions cannot read it. Do not downgrade. Turning the feature off is safe only from n8n 2.40.3; on earlier versions setting the variable to `false` makes all data written since enabling permanently inaccessible. There is no conversion tool; recovery means restoring a database backup.

Order of work: back up the database, try staging first (verify credentials still decrypt), then production. The same backup step applies before upgrading to 3.0.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/configure-n8n/security/rotate-encryption-keys

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
