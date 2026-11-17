---
id: computing-software.web-development.strapi.data-transfer-command
name: data-transfer-command
category: computing-software
field: web-development
product: strapi
tags: [strapi, strapi-transfer, transfer-token, remote, sync, environments]
level: advanced
status: docs-checked
description: "Push or pull data between two Strapi instances with strapi transfer, transfer tokens, and the interactive-mode environment variables."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/server.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/configurations/environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# strapi transfer

Transfers data between 2 Strapi instances, mainly local to remote or between remotes.

```bash
strapi transfer --to http://example.com/admin --to-token my-transfer-token
```

## Rules from the page
- The destination instance should run with `start`, not `develop`.
- You can't pass both `--to` and `--from`.
- `--from` with `--to-token`, or `--to` with `--from-token`, is an error.
- With neither `--to` nor `--from`, the command is interactive: it asks pull or push, uses `STRAPI_TRANSFER_URL` for the remote URL (asks if unset) and `--from-token`/`--to-token` or `STRAPI_TRANSFER_TOKEN` for the token (asks if unset).
- `STRAPI_TRANSFER_URL` and `STRAPI_TRANSFER_TOKEN` are only read in interactive mode.

## Related config
- `transfer.remote.enabled` in `config/server` toggles the transfer feature (default `true`).
- `transfer.remote.assetIdleTimeoutMs` sets the stall timeout when pulling from a remote.
- `TRANSFER_TOKEN_SALT` is the salt for transfer tokens.

## Checked

Checked 2026-11-04 against the Strapi CLI page (`strapi transfer`), the Server configuration page (`transfer.remote.enabled` default `true`, `transfer.remote.assetIdleTimeoutMs`) and the Environment page (`TRANSFER_TOKEN_SALT`). Nothing removed.

Method: documentation only; no commands were run.
