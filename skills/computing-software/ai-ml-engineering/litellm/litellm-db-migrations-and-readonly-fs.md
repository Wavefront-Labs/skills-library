---
id: computing-software.ai-ml-engineering.litellm.litellm-db-migrations-and-readonly-fs
name: litellm-db-migrations-and-readonly-fs
category: computing-software
field: ai-ml-engineering
product: litellm
tags: [litellm, disable-schema-update, prisma-migrate-deploy, read-only-filesystem]
level: advanced
status: docs-checked
description: "Control database migrations (DISABLE_SCHEMA_UPDATE, Helm PreSync hook) and run on a read-only root filesystem."
sources:
  - https://docs.litellm.ai/docs/proxy/prod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Migrations: LiteLLM runs `prisma migrate deploy` on startup by default, so no configuration is needed across versions. To stop a pod from running migrations set `DISABLE_SCHEMA_UPDATE=true`.

Helm PreSync hook (beta): one service manages migrations during `helm upgrade` or `helm install`. The hook always sets `DISABLE_SCHEMA_UPDATE=false`. Set the LiteLLM pods to skip:

```
env:
  - name: DISABLE_SCHEMA_UPDATE
    value: "true"
```

`USE_PRISMA_MIGRATE="True"` was removed when migrate deploy became the default; setting it is not needed.

`migrate deploy` does not warn if an already applied migration is missing from history, does not detect drift, and does not reset the database or use a shadow database.

Read-only filesystem: LiteLLM supports `readOnlyRootFilesystem: true`. A `Permission denied` error means it needs writable directories:

- `LITELLM_MIGRATION_DIR`: migrations (default: package directory)
- `LITELLM_UI_PATH`: Admin UI (default /var/lib/litellm/ui in Docker)
- `LITELLM_ASSETS_PATH`: UI assets and logos (default /var/lib/litellm/assets)
- `PRISMA_BINARY_CACHE_DIR` and `XDG_CACHE_HOME`: caches

Recommended: an initContainer copies the pre-built UI from the image into emptyDir volumes, with `LITELLM_NON_ROOT=true`, `runAsNonRoot: true`, `runAsUser: 101` and `capabilities: drop: [ALL]`.

API-only alternative: set `LITELLM_NON_ROOT=true` and `LITELLM_MIGRATION_DIR` to a writable path; the proxy logs a UI warning but the API works. With a custom `server_root_path`, pre-process the UI files in your Dockerfile.

## Checked

2026-11-03. Confirmed on the LiteLLM production page (docs.litellm.ai/docs/proxy/prod): prisma migrate deploy on startup, DISABLE_SCHEMA_UPDATE, the Helm PreSync hook, USE_PRISMA_MIGRATE removal, the migrate deploy limits, readOnlyRootFilesystem, the writable-directory variables and defaults, and the initContainer example with LITELLM_NON_ROOT, runAsUser 101 and drop ALL.

Method: documentation only; no commands were run.
