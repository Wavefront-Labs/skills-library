---
id: computing-software.cloud-infrastructure-engineering.openbao.static-key-seal
name: static-key-seal
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, static-seal, current-key, previous-key, key-rotation]
level: advanced
status: docs-checked
description: "OpenBao static key auto-unseal: 32-byte AES-256-GCM keys, env:// and file:// sources, key IDs and n-1 to n rotation."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/configuration/seal/static.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Static key seal

Keys are AES-256-GCM-96: exactly 32 bytes, given as base64 or hex directly, or via `env://` or `file://`. Other algorithms are not supported.

## Parameters (`seal "static"`)

- `current_key_id` (required): permanent identifier; change it whenever `current_key` changes
- `current_key` (required)
- `previous_key_id`, `previous_key`: optional pair; `previous_key_id` is required if `previous_key` is set
- `disabled`: `true` only when migrating from an auto seal, else `false`

No dedicated environment variables; use `env://` on the key parameters.

## Rotation (n-1 to n)

Set `current_key` to the new key and `previous_key` to the key currently encrypting storage. Each ID must always match its key; the docs suggest computing IDs from the key automatically.

## Generating a sample key

The docs use `openssl rand` to write 32 bytes to the target file path.

## Warnings

- Evaluate carefully before adopting. It is recommended only when an existing trust source (e.g. a third-party secrets manager) is already present and you want OpenBao to chain to it.
- Key material must be injected properly.

## Checked

2026-11-04. Read the OpenBao static seal page in full. Confirmed: 32-byte AES-256-GCM-96 key, base64, hex, `env://` and `file://` forms, all five parameters and their rules, the `n-1` to `n` rotation, the key ID matching rule, the `openssl rand` sample key command and the recommendation warning. Removed: nothing.
Method: documentation only; no commands were run.
