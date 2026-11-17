---
id: computing-software.cybersecurity-defensive.authelia.totp-and-webauthn-storage-cli
name: totp-and-webauthn-storage-cli
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, totp, webauthn, storage-user, export, import, cli, credential-management]
level: advanced
status: docs-checked
description: "Manage registered second factors from the Authelia CLI: generate, import, export or delete TOTP configurations, and list, verify or delete WebAuthn credentials."
sources:
  - https://www.authelia.com/reference/cli/authelia/authelia_storage_user_totp_export_png/
  - https://www.authelia.com/reference/cli/authelia/authelia_storage_user_webauthn_list/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Administrators can manage second factors directly in the database.

TOTP, under `authelia storage user totp`: `generate`, `import`, `delete` and `export`. Exports come in three forms (`uri`, `csv`, `png`):

```bash
authelia storage user totp export png --directory /path/to/export \
  --config /path/to/configuration.yml
```

The plain `export` command writes an importable file chosen with `-f, --file` (default `authelia.export.totp.yml`; the extension picks TOML, JSON or YAML). The `png` export takes `--directory` and produces QR code images of each configuration's URI so it can be scanned onto a new device; `uri` and `csv` give text outputs. Treat all exports as secrets, since each holds the user's shared TOTP key. Delete the directory afterwards.

WebAuthn, under `authelia storage user webauthn`: `list`, `verify`, `delete`, `export` and `import`.

```bash
authelia storage user webauthn list
authelia storage user webauthn list john --config /path/to/configuration.yml
```

`list` takes an optional username.

All of these commands require the storage encryption key and the database details, from the configuration or from flags like `--encryption-key`, `--postgres.address` and `--postgres.password`. Without the right key, encrypted secrets cannot be read.

Only `totp export png`, `totp export`, and `webauthn list` were read in detail; the other subcommands are known only from the command index. Likely uses: re-enrolling a user who lost a device (delete their entry, they register again), migrating TOTP between instances (export then import), and auditing which users have security keys.

Check: after deleting a user's TOTP entry, log in as that user and confirm the portal asks them to register again.

## Checked

2026-11-08. Read in full: CLI pages for totp, totp export, totp export png, webauthn, webauthn list. Subcommand lists verified from the command index; other subcommand pages not read, and the draft says so.

Method: documentation only; no commands were run.
