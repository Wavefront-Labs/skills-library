---
id: computing-software.database-administration.pgbackrest.azure-repository
name: azure-repository
category: computing-software
field: database-administration
product: pgbackrest
tags: [pgbackrest, azure, object-store, repo-azure, blob-storage]
level: practitioner
status: docs-checked
description: "Configure an Azure Blob repository with shared key or SAS and avoid hierarchical namespace."
sources:
  - https://pgbackrest.org/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: store the repository in an Azure container.

The container must be created in advance; pgBackRest will not do it. The repository can be in the container root, though a subpath is usually best.

```
[global]
repo2-type=azure
repo2-path=/demo-repo
repo2-azure-account=<account>
repo2-azure-container=demo-container
repo2-azure-key=<key>
repo2-retention-full=4
```

Warning from the guide: do not enable hierarchical namespace, as it causes errors during expire.

Key types via `repo-azure-key-type`: `shared` (default), `sas` (set `repo2-azure-key` to the shared access signature token) or `auto` (Azure managed identities). `repo-azure-uri-style` is `host` (connect to account.endpoint, default) or `path` (connect to the endpoint host and prepend the account to URIs).

Commands then run exactly as for a local repository; the guide runs stanza-create (which creates the stanza on each configured repository) and backup with `--repo=2`.

File creation time in Azure is relatively slow, so backup and restore are faster with file bundling enabled. Tune uploads with `repo-storage-upload-chunk-size` (the default for Azure is 4MiB).

## Checked

2026-11-03: option names, defaults, ranges and behaviour confirmed against the pgBackRest Configuration Reference (pgbackrest.org/configuration.html) and the pgBackRest User Guide (pgbackrest.org/user-guide.html) (Azure-Compatible Object Store Support). Nothing needed removing. 

Method: documentation only; no commands were run.
