---
id: computing-software.database-administration.pgbackrest.gcs-repository
name: gcs-repository
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, gcs, object-store, repo-gcs, service-account]
level: practitioner
status: docs-checked
description: "Configure a Google Cloud Storage repository and choose a key type."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store the repository in a GCS bucket.

Repository files can be in the bucket root with `repo-path=/`, though a prefix such as `/repo` is usually best so logs and other content can share the bucket.

```
[global]
repo5-type=gcs
repo5-path=/demo-repo
repo5-gcs-bucket=demo-bucket
repo5-gcs-key=/path/to/gcs-key.json
```

`repo-gcs-key-type` values:

- `service` (default): service account from a locally stored key file (`repo-gcs-key`); credentials reload when the token renews.
- `auto`: authorize using the instance service account; the guide notes setting this when running in GCE.
- `web-id`: Workload Identity Federation. `repo-gcs-key` must hold an external account credential file; `service_account_impersonation_url` is not supported, only `credential_source.file`, and a specified `credential_source.format` must be text.
- `token`: for local testing, for example with a fake GCS.

`repo-gcs-endpoint` defaults to storage.googleapis.com and can point to a local GCS server. `repo-gcs-user-project` is the project ID used to determine request billing.

File creation time in GCS is relatively slow, so file bundling improves backup and restore performance.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (GCS-Compatible Object Store Support). Removed: the claim that the bucket must exist beforehand. 

Method: documentation only; no commands were run.
