---
id: computing-software.database-administration.dragonfly.snapshots-to-s3
name: snapshots-to-s3
category: computing-software
field: database-administration
product: dragonfly
tags: [s3-snapshots, s3-bucket, cloud-backup, dragonfly]
level: practitioner
status: docs-checked
description: "Store and restore Dragonfly snapshots in an S3 bucket by pointing the dir flag at an s3 URL, with an optional path prefix."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/backups.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly can save backups to and restore from AWS S3 instead of local disk. Configure the `--dir` flag with the bucket URL:

```shell
./dragonfly --logtostderr --dir s3://acme-backups
```

Add an optional path prefix:

```shell
./dragonfly --logtostderr --dir s3://acme-backups/dragonfly/staging
```

As with disk backups, Dragonfly loads the latest snapshot from the bucket on startup and stores one on shutdown.

Warning from the docs: S3 cloud storage is a preview feature. Report problems as a GitHub issue.

An individual save can also target a cloud URI directly: `SAVE DF s3://bucket/folder my_dump`.

Credentials and region come from the environment, see the S3 credentials skill.

## Checked

2026-11-04. Confirmed against the Dragonfly Saving Backups and SAVE pages: `--dir` with an s3 URL, the path prefix example, load on startup and save on shutdown, preview warning, `SAVE DF s3://bucket/folder my_dump`. Removed the claim that scheduled snapshots write to S3 and the Operator `snapshot.dir` field, which the operator page does not list.

Method: documentation only; no commands were run.
