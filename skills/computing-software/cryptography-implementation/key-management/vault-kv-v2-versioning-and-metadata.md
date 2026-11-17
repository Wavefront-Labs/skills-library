---
id: computing-software.cryptography-implementation.key-management.vault-kv-v2-versioning-and-metadata
name: vault-kv-v2-versioning-and-metadata
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, vault-kv-v2, hashicorp-vault, secrets-versioning, check-and-set, secrets-managers]
level: practitioner
status: docs-checked
description: "Use Vault KV v2 versioned secrets: data versus metadata paths, max_versions, check-and-set writes, soft delete versus destroy, and ACL paths that trip people up."
sources: ["https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2", "https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vault KV v2 versioning and metadata

## Enable and use
Each write creates a new version. Versions can be soft-deleted (`delete`), restored (`undelete`) or destroyed
(`destroy`); the read response carries per-version `created_time`, `deletion_time`, `destroyed` and `version`. Writes
accept a `cas` option for check-and-set.

## API paths (the ACL trap)
The CLI hides a path prefix. Policies must use the real API paths:
- `secret/data/...` read/write values
- `secret/metadata/...` list and key metadata; listing needs `list` here even if everything else uses `/data/`
- `secret/delete/...`, `secret/undelete/...`, `secret/destroy/...`
KV v2 does not filter listed key names by policy, so keep sensitive information out of key names.

## Practices
- `cas_required` (default false) forces every write to supply `cas`, preventing lost updates from concurrent writers.
- `max_versions` defaults to keeping 10 versions (0 or unset); beyond the limit the oldest is permanently deleted.
  Old versions remain readable secrets, so keep it modest. `delete_version_after` sets a time before a version is deleted.
- Rotation: write new version, roll consumers, then destroy old versions once unused.
- `custom_metadata` on the key for inventory.

## Verify
- [ ] Policies name `data/` and `metadata/` paths; a least-privilege token reads only its keys.

## Checked

2026-11-01. Confirmed against the Vault KV v2 API page (`max_versions` default of 10, `cas_required`, `delete_version_after`,
`custom_metadata`, `cas`, data/metadata/delete/undelete/destroy paths, list on `metadata`, key-name warning). Removed: all
CLI commands and flags and the rotation-order advice (CLI page not fetched).
Method: documentation only; no commands were run.
