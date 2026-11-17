---
id: computing-software.database-administration.patroni.patroni-basebackup-options
name: patroni-basebackup-options
category: computing-software
field: database-administration
product: patroni
tags: [patroni, basebackup, pg-basebackup, waldir, replica]
level: practitioner
status: docs-checked
description: "Pass long options to pg_basebackup through the basebackup section as a map or list, and what not to override."
sources:
  - https://patroni.readthedocs.io/en/latest/replica_bootstrap.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune the default replica creation method safely.

The `basebackup` method works without configuration, but a section of long options (with `--`) may be given. Two equivalent shapes are accepted:

```
postgresql:
  basebackup:
    max-rate: '100M'
    checkpoint: 'fast'
```

```
postgresql:
  basebackup:
    - verbose
    - max-rate: '100M'
    - waldir: /path/to/external-waldir
```

The list form allows single keys for options without values, such as `--verbose`.

Cautions from the docs:
- There is no validation of names or values passed in the section.
- If you override the connection string or request tar-ed or compressed base backups, Patroni cannot make a replica out of it.
- If symlinks are used for the WAL folder, specify the correct `--waldir` so the symlink persists after replica build-up or re-initialization. This option is supported only since PostgreSQL 10.
- Release notes for 4.1.1 say server-side compression is allowed for basebackup since PostgreSQL 15 with plain format, while client-side compression is still rejected; options given as a dictionary are now validated like lists.

The origin of the backup is the leader unless replicas carry the `clonefrom` tag; with several such replicas one is chosen randomly.

## Checked

2026-11-03. Confirmed against the replica bootstrap page (basebackup options in both shapes, cautions about validation, tar and compression, waldir) and the 4.1.1 release note.

Method: documentation only; no commands were run.
