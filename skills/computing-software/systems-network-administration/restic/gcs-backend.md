---
id: computing-software.systems-network-administration.restic.gcs-backend
name: gcs-backend
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, google-cloud-storage, gcs, backend, service-account]
level: practitioner
status: docs-checked
description: "Use Google Cloud Storage as a restic backend with project ID, service account JSON, access tokens and the required bucket permissions."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Google Cloud Storage backend

URL form, bucket `foo` at the root:

```
restic -r gs:foo:/ init
```

## Credentials

```
export GOOGLE_PROJECT_ID=my-project
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
```

`GOOGLE_ACCESS_TOKEN` disables all other authentication mechanisms. The token needs at least the scope `https://www.googleapis.com/auth/devstorage.read_write` and is short-lived (usually one hour), so it does not suit a backup that runs longer. On an instance with default service account credentials, they should work without these variables.

## Permissions

The identity needs `storage.objects.create`, `storage.objects.delete`, `storage.objects.get` and `storage.objects.list`. Add `storage.buckets.create` only if `init` should create the bucket.

## Options

- `-o gs.connections=10` sets parallel connections; default 5.
- `-o gs.region=us` sets the bucket region used when the bucket is created; default `us`.

The four object permissions are included in the Storage Object Admin role; `storage.buckets.create` is in the Storage Admin role.

## Checked

2026-11-03. Confirmed in the restic docs page Preparing a new repository (Google Cloud Storage section) and Scripting: `gs:foo:/` form, `GOOGLE_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_ACCESS_TOKEN` behaviour and scope, the four object permissions and `storage.buckets.create`, the role names, `gs.connections` default 5, `gs.region` default `us`. Removed: the bucket-creation advice, the smoke-test paragraph and the several-repositories-per-bucket paragraph (not in the docs).

Method: documentation only; no commands were run.
