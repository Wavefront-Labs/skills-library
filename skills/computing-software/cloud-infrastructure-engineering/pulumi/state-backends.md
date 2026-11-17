---
id: computing-software.cloud-infrastructure-engineering.pulumi.state-backends
name: state-backends
category: computing-software
field: cloud-infrastructure-engineering
product: pulumi
tags: [cloud-infrastructure-engineering, pulumi, pulumi-login, s3-backend, self-managed-backend, state-backend]
level: practitioner
status: docs-checked
description: "Choose and log in to a Pulumi state backend: Pulumi Cloud or DIY (S3, Azure Blob, GCS, file, PostgreSQL), plus migrate and logout."
sources:
  - https://www.pulumi.com/docs/iac/concepts/state-and-backends/
  - https://www.pulumi.com/docs/iac/concepts/state-and-backends/using-a-diy-backend/
  - https://www.pulumi.com/docs/iac/cli/commands/pulumi_stack_migrate/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State backends

```bash
pulumi login                                  # Pulumi Cloud (default)
pulumi login s3://my-bucket?region=us-west-2  # AWS S3 (also &profile=...)
pulumi login 's3://my-bucket?endpoint=my.minio.local:8080&disableSSL=true&s3ForcePathStyle=true'  # MinIO
pulumi login azblob://my-container            # Azure Blob
pulumi login gs://my-bucket                   # Google Cloud Storage
pulumi login file://~/pulumi-state            # local directory
pulumi login --local                          # same as file://~ (state under ~/.pulumi)
pulumi login postgres://...                   # PostgreSQL backend
pulumi logout                                 # --all to log out of every backend
pulumi whoami -v                              # shows "Backend URL"
```

Select a backend without logging in: set `PULUMI_BACKEND_URL`, or put `backend: {url: ...}` in `Pulumi.yaml`.

Azure Blob credentials: `AZURE_STORAGE_ACCOUNT` plus `AZURE_STORAGE_KEY` or `AZURE_STORAGE_SAS_TOKEN`; otherwise the Azure default credential chain is used.

Migrate stacks between backends with `pulumi stack migrate` (CLI v3.254.0+; check `pulumi stack migrate --help`).

## Gotchas
- DIY backends use file-based locking and keep history; lock files live under `.pulumi/locks`.
- Stack names on a DIY backend use the constant organization `organization` (for example `organization/project/stack`).
- A backend created before Pulumi v3.61.0 uses a global namespace; upgrade it with `pulumi state upgrade`.
- Every user and CI job needs credentials for the bucket or database, set up outside Pulumi.

## Verify
`pulumi whoami -v` prints the `Backend URL` you are logged in to.

## Checked
2026-11-03. Confirmed against the Pulumi docs source (pulumi/docs, content/docs): the State and backends page and the "Using a DIY backend" page (URL forms and query parameters, `--local`, `PULUMI_BACKEND_URL`, `backend.url`, Azure credentials, locking and history, `organization`, `state upgrade`, `whoami -v`, logout) and the `pulumi stack migrate` reference. Removed: bucket versioning advice, passphrase-provider naming claims, the Pulumi Cloud access-token claim, export/import migration steps and "confirm" hedges.
Method: documentation only; no commands were run.
