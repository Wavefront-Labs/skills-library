---
id: computing-software.devops-ci-cd.backstage.techdocs-ci-github-actions
name: techdocs-ci-github-actions
category: computing-software
field: devops-ci-cd
product: backstage
tags: [techdocs-ci, github-actions-publish, external-build, backstage]
level: practitioner
status: docs-checked
description: "Publish TechDocs from a CI workflow, with an example using GitHub Actions and AWS S3."
sources:
  - https://backstage.io/docs/features/techdocs/configuring-ci-cd
  - https://backstage.io/docs/features/techdocs/cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

For the recommended deployment, CI generates and publishes docs on each change to the default branch. The steps are:

1. Prepare: clone the repository and install `@techdocs/cli` and `mkdocs-techdocs-core`.
2. Generate: build the site.
3. Publish: upload it to your bucket.

```yaml
name: Publish TechDocs Site
on:
  push:
    branches: [main]
    paths:
      - 'docs/**'
      - 'mkdocs.yml'
jobs:
  publish-techdocs-site:
    runs-on: ubuntu-latest
    env:
      TECHDOCS_S3_BUCKET_NAME: ${{ secrets.TECHDOCS_S3_BUCKET_NAME }}
      ENTITY_NAMESPACE: default
      ENTITY_KIND: Component
      ENTITY_NAME: artist-web
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - uses: actions/setup-python@v4
      - run: npm install -g @techdocs/cli
      - run: pip install "mkdocs-techdocs-core==1.*"
      - run: techdocs-cli generate --no-docker --verbose
      - run: techdocs-cli publish --publisher-type awsS3 --storage-name $TECHDOCS_S3_BUCKET_NAME --entity $ENTITY_NAMESPACE/$ENTITY_KIND/$ENTITY_NAME
```

Provide the cloud credentials as CI secrets. `generate` computes a content hash (etag) of the site, so adding `--skip-if-unchanged` to `publish` skips the upload when nothing changed. Set the `ENTITY_*` values from the entity in the repository's `catalog-info.yaml`: the CLI stores files under `namespace/kind/name/` in the bucket and the values are case-sensitive.

## Checked

2026-11-03. Confirmed on the Configuring CI/CD page: the prepare, generate and publish steps, `mkdocs-techdocs-core==1.*`, `techdocs-cli generate --no-docker`, the `publish` flags, the `ENTITY_NAMESPACE`/`ENTITY_KIND`/`ENTITY_NAME` variables, the content-hash (etag) tip and `--skip-if-unchanged`. On the TechDocs CLI page: `--entity` is `namespace/kind/name`, case-sensitive, and the bucket layout is `namespace/kind/name/<files>`. Changed: action versions to those the page uses (checkout v3, setup-node v3, setup-python v4). Removed: claims about organisation secrets and path filters keeping runs cheap, and the statement about what the reader shows after a mismatch, which the pages do not make. The trigger block is an illustration, not from the page.

Method: documentation only; no commands were run.
