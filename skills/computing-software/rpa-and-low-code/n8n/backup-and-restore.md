---
id: computing-software.rpa-and-low-code.n8n.backup-and-restore
name: backup-and-restore
category: computing-software
field: rpa-and-low-code
product: n8n
tags: [n8n, backup, restore, encryption-key, export-workflow, user-folder]
level: practitioner
status: docs-checked
description: "Back up and restore self-hosted n8n: the .n8n folder, external database, CLI export --backup limits, import flags, decrypted exports and full-instance recovery order."
sources:
  - https://docs.n8n.io/deploy/host-n8n/keep-n8n-running/backup-and-restore
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: recover a full instance, not just workflows.

## A complete backup
1. The `.n8n` folder (`~/.n8n`, relocatable via `N8N_USER_FOLDER`, which uses its `.n8n` subfolder): holds the `config` file with the credential encryption key, the SQLite file if used, and filesystem-mode binary or execution data.
2. The external PostgreSQL database, with its own tooling. Still back up `.n8n` because credentials are encrypted with its key.
Also back up external binary or execution storage (S3, Azure Blob), custom filesystem paths, and `N8N_CUSTOM_EXTENSIONS` directories. With SQLite, stop n8n before copying. In Docker the folder is the `n8n_data` volume mounted on the node user home `.n8n` folder. Without the encryption key (`config` or `N8N_ENCRYPTION_KEY`) restored credentials cannot be decrypted. Take a full backup before every update.

## CLI export
```bash
n8n export:workflow --backup --output=backups/workflows/
n8n export:credentials --backup --output=backups/credentials/
```
`--backup` means `--all --pretty --separate`. Use different output directories: `import:credentials --separate` fails when the directory also holds workflow files. In Docker bind-mount a host directory because container paths outside the volume are lost. A CLI backup excludes users and roles, execution history, variables and instance settings (including the encryption key).

## Restore
```bash
n8n import:workflow --separate --input=backups/workflows/
n8n import:credentials --separate --input=backups/credentials/
```
Complete the owner setup first on a fresh instance; use `--userId` or `--projectId` for credential ownership. Items with the same IDs are overwritten. Imported workflows are deactivated; `--activeState=fromJson` restores active state but only in queue or multi-main mode. Credentials need the same encryption key, or export with `--decrypted` (plain text: delete afterwards).

Full instance: stop n8n, restore `.n8n` and custom-node directories, restore PostgreSQL, restore deployment environment variables (database, `N8N_ENCRYPTION_KEY`, storage), start n8n.

## Checked

2026-11-03. Read against the official n8n documentation pages:
- https://docs.n8n.io/deploy/host-n8n/keep-n8n-running/backup-and-restore

Confirmed: parameter names, defaults, limits, commands and behaviour in this skill match those pages. Nothing removed; every concrete claim matched the page.

Method: documentation only; no commands were run.
