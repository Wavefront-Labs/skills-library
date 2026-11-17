---
id: computing-software.web-development.hugo.hugo-deploy-cloud-buckets
name: hugo-deploy-cloud-buckets
category: computing-software
field: web-development
product: hugo
tags: [hugo-deploy, s3, azure-blob, google-cloud-storage, deployment-targets]
level: practitioner
status: docs-checked
description: "Deploy with hugo deploy to S3, Azure Blob or Google Cloud Storage: target URLs, build and deploy flags, comparison rules and authentication."
sources:
  - https://raw.githubusercontent.com/gohugoio/hugoDocs/master/content/en/host-and-deploy/deploy-with-hugo.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Config: a `[deployment]` table with `[[deployment.targets]]` entries, each with a `name` you choose and a `url`.

- Amazon S3: `s3://my-bucket?region=us-west-1`
- Azure Blob Storage: `azblob://my-container?storage_account=my-account`
- Google Cloud Storage: `gs://my-bucket`

Build first from the project root: `hugo build` with `--cleanDestinationDir` (remove orphans from `public`), `--gc` and `--minify`.

`hugo deploy` flags:

- `--confirm`: list changes and prompt.
- `--dryRun`: list changes without applying.
- `--force`: upload every file, even unchanged.
- `--maxDeletes`: cap deletions (default 256; `-1` disables). If exceeded, uploads proceed but all deletions are skipped with a warning.
- `--target`: pick a target by name (default is the first).

Files are compared by size and MD5 checksum. Remote files absent from local `public` are deleted. `.DS_Store` and hidden directories like `.git` are skipped; `.well-known` is uploaded.

Authentication:

- S3: AWS CLI 2.32.0 or later, run `aws login`, attach the SignInLocalDevelopmentAccess managed policy.
- Azure: Azure CLI, `az login`, Storage Blob Data Contributor role on the account.
- Google: Google Cloud CLI, `gcloud auth application-default login`.
- CI or non-interactive: supply credentials through environment variables.

Matchers, headers, upload order and CDN invalidation are under the deployment configuration page (not fetched here).

## Checked

2026-11-04. Confirmed against the Hugo docs page Deploy with Hugo: the target URL formats, the build flags, the five deploy flags and the 256 default for `--maxDeletes`, size and MD5 comparison, the `.DS_Store`, hidden-directory and `.well-known` rules, and the AWS CLI 2.32.0, `aws login`, Azure and Google authentication steps. Nothing removed.

Method: documentation only; no commands were run.
