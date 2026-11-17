---
id: computing-software.systems-network-administration.restic.b2-backend
name: b2-backend
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, backblaze, b2, backend, application-key]
level: practitioner
status: docs-checked
description: "Use the native Backblaze B2 backend with application keys, connection count and lifecycle rules, and know when the S3 API is preferred."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backblaze B2 backend

The restic docs recommend using B2 through its S3-compatible API (see the s3-compatible-storage skill) because the native backend has error-handling issues. If you use native B2:

```
export B2_ACCOUNT_ID=...
export B2_ACCOUNT_KEY=...
restic -r b2:bucketname:path/to/repo init
```

## Keys

As of restic 0.9.2, non-master application keys work, provided they have at least read and write access to the bucket. Earlier versions need a master application key. Treat the application key like a password: Backblaze shows it only once.

## Tuning

`-o b2.connections=10` raises parallel connections; the default is 5. Too many connections can degrade performance, so raise it gradually.

## Bucket notes

- Bucket names must be globally unique.


## Hidden files

The S3 backend only hides files that are no longer needed, and B2 keeps old versions by default. The docs suggest the B2 lifecycle rule `Keep only the last version of the file`, which deletes hidden versions after one day.

## Checked

2026-11-03. Confirmed in the restic docs page Preparing a new repository (Backblaze B2 section) and Scripting: S3-API recommendation and reason, `B2_ACCOUNT_ID`/`B2_ACCOUNT_KEY`, the 0.9.2 note on non-master keys, the `bucketname:path` URL form, unique bucket name, `b2.connections` default of 5, and the lifecycle rule. The warning that a too high connection count degrades performance is on the Tuning parameters page. Removed: the bucket-restricted-key advice and the smoke-test and path-per-repository paragraph (not in the docs).

Method: documentation only; no commands were run.
