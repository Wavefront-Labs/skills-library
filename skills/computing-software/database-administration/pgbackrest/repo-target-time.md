---
id: computing-software.database-administration.pgbackrest.repo-target-time
name: repo-target-time
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, repo-target-time, versioned-storage, object-lock, recovery]
level: sme
status: docs-checked
description: "Read a versioned object-store repository as it was at an earlier time to recover from deletion or malware."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: recover from a deleted or corrupted repository.

`repo-target-time` makes commands read a repository on versioned storage as it existed at a point in time. It is supported on S3, GCS and Azure, where versioning is generally not enabled by default. Consider also enabling object locking on S3 and soft delete on GCS or Azure.

Rules:

- `--repo` must be given with `--repo-target-time`; usually target a single repository.
- Comparison against the storage timestamp is less than or equal to the value, and milliseconds are truncated.

Guide example: after the stanza was deleted from the S3 repository, `info` showed `status: error (missing stanza path)`. The time of deletion was found by listing versions of `backup.info` with the AWS CLI, and `info` then showed the repository just before the DELETE marker:

```
pgbackrest --stanza=demo --repo=3 --repo-target-time="2026-10-15 07:08:49+00" info
pgbackrest --stanza=demo --repo=3 --delta --repo-target-time="2026-10-15 07:08:49+00" restore
```

If the needed backup is listed, restore with the same target time. The generated `restore_command` then includes `--repo` and `--repo-target-time`, so WAL replay also reads the repository as of that time.

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Target Time for Repository). Nothing needed removing. 

Method: documentation only; no commands were run.
