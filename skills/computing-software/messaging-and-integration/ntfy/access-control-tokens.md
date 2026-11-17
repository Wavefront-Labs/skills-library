---
id: computing-software.messaging-and-integration.ntfy.access-control-tokens
name: access-control-tokens
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, access-tokens, token, auth-tokens, provisioning]
level: advanced
status: docs-checked
description: "Create, expire and provision ntfy access tokens with ntfy token or auth-tokens config, and know that tokens grant full account access."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/config.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Access tokens

```
ntfy token list
ntfy token add phil
ntfy token add --expires=2d phil
ntfy token remove phil tk_th2sxr...
ntfy token generate
```

- 60 tokens per user maximum.
- Tokens must start with `tk_` and be 32 characters long.

## Provision from config

Format `<username>:<token>[:<label>]`:

```yaml
auth-tokens:
  - "phil:tk_3gd7d2yftt4b8ixyfe9mnmro88o76"
  - "backup-service:tk_f099we8uzj7xi5qshzajwp6jffvkz:Backup script"
```

## Use

`Authorization: Bearer tk_...` or `curl -u :tk_...` (see publish-authentication).

## Gotchas

- Tokens currently grant everything except changing the password and deleting the account; treat them like passwords.
- `auth-tokens` entries are created or updated when the server starts; entries removed from the config are deleted from the database. The `<username>` must be an existing provisioned user from `auth-users`.
- `ntfy token generate` creates a random token for use in `auth-tokens`.
- Each token can carry a label and an expiry (`--expires=2d`, `--label=backups`).

## Checked

2026-11-04. Confirmed against the ntfy config page (Access tokens, Tokens via the CLI and via the config): command list, 60 tokens per user, `tk_` prefix and 32-character length, `<username>:<token>[:<label>]` format, full-account-access warning, provisioning and deletion behaviour. Removed: the invented Verify step and the claim that generate does not store a token.
Method: documentation only; no commands were run.
