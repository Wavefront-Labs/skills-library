---
id: computing-software.cloud-infrastructure-engineering.openbao.kv-v2-secrets
name: kv-v2-secrets
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, kv-v2, versioning, soft-delete, destroy]
level: practitioner
status: docs-checked
description: "Use the OpenBao KV v2 engine: put, get, patch, delete, undelete, destroy, metadata limits and the data/ metadata/ policy paths."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/secrets/kv/kv-v2.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KV v2

## Commands

- `bao kv put` (`-cas` for check-and-set), `bao kv get` (`-version`)
- `bao kv patch`: tries HTTP PATCH, falls back to read-then-write; `-method` is `patch` or `rw` (read-then-write needs `read` and `update`)
- `bao kv delete` (soft; `-versions`), `bao kv undelete`, `bao kv destroy` (permanent)
- `bao kv metadata get|put|patch|delete`; `metadata delete` removes all versions

## Metadata settings

`max_versions` (`-max-versions`, older versions cleaned on next write), `delete_version_after` (new versions only), `custom_metadata` (`metadata put` overwrites it; `metadata patch` updates fields).

## Policy paths (separate ACLs)

- `secret/data/`: read/create/update/delete latest
- `secret/delete/`, `secret/undelete/`, `secret/destroy/`
- `secret/metadata/`: list, read, delete

## Gotchas

- Upgrading a v1 mount makes it inaccessible during conversion, then policies must switch to the prefixed paths.
- Non-string CLI values become strings; use a JSON file or the HTTP API to keep types.
- `allowed_parameters`, `denied_parameters`, `required_parameters` do not work in v2 policies.
- Writing to a soft-deleted key needs `cas` to match the current version.
- `destroy` and `metadata delete` are irreversible.

## Checked

2026-11-04. Confirmed against the KV version 2 page: put with -cas, get with -version, patch with -method patch or rw and its capabilities, delete, undelete, destroy, metadata commands and settings, data, delete, undelete, destroy and metadata policy paths, v1 upgrade behaviour, string conversion and the unsupported parameter constraints. Nothing removed.

Method: documentation only; no commands were run.
