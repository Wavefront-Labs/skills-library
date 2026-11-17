---
id: computing-software.devops-ci-cd.backstage.techdocs-cli-generate-publish
name: techdocs-cli-generate-publish
category: computing-software
field: devops-ci-cd
product: backstage
tags: [techdocs-cli, generate-site, publish-docs, backstage]
level: practitioner
status: docs-checked
description: "Use techdocs-cli to generate TechDocs sites, publish them to storage and preview them locally."
sources:
  - https://backstage.io/docs/features/techdocs/cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `techdocs-cli` builds and publishes sites outside the Backstage backend. Install it with `npm install -g @techdocs/cli` or run `npx @techdocs/cli`.

Commands:

- `generate` (alias `build`): generate a site with the selected engine, MkDocs by default.
- `publish`: upload a generated site to AWS S3, Google GCS or other external storage.
- `serve`: preview docs in a Backstage-like environment.
- `serve:raw`: serve with the configured engine alone (`serve:mkdocs` is deprecated).
- `migrate`: migrate objects with case-sensitive entity triplets to lowercase.

```bash
npx @techdocs/cli generate --no-docker --source-dir . --output-dir ./site
npx @techdocs/cli publish --publisher-type awsS3 \
  --storage-name <bucket> --entity <namespace>/<kind>/<name> \
  --directory ./site
```

- `--no-docker` runs MkDocs locally, so install `mkdocs-techdocs-core` first.
- `--entity` is `namespace/kind/name` (case-sensitive); files are stored at `namespace/kind/name/<files>` in the bucket. If the namespace is missing in `catalog-info.yaml`, use `default`.
- `--skip-if-unchanged` skips publishing when the local etag in `techdocs_metadata.json` matches the remote etag.

For local authoring, `techdocs-cli serve` uses a Docker image by default; you can override it with `--docker-image`, pass `--docker-option` flags, or use `--no-docker`.

## Checked

2026-11-03. Confirmed on the TechDocs CLI page: install with `npm install -g @techdocs/cli` or `npx`, commands generate (alias build), publish, serve, serve:raw (serve:mkdocs deprecated alias) and migrate, `--no-docker`, `--docker-image`, `--docker-option`, `--source-dir`/`--output-dir`, `publish` flags `--publisher-type`, `--storage-name`, `--entity`, `--directory`, `--skip-if-unchanged`, and the bucket layout. Removed: the version pinning advice, which the page does not give.

Method: documentation only; no commands were run.
