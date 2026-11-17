---
id: computing-software.systems-network-administration.kopia.kopia-concepts-repository-snapshot-policy
name: kopia-concepts-repository-snapshot-policy
category: computing-software
field: systems-network-administration
product: kopia
tags: [concepts, repository, snapshot, policy, incremental, deduplication]
level: intro
status: docs-checked
description: "Core Kopia concepts: repository, snapshot, policy, content-addressed incremental backups, and the basic CLI workflow from create to restore."
sources: ["https://kopia.io/docs/getting-started/", "https://kopia.io/docs/faqs/", "https://kopia.io/docs/repositories/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
- A **snapshot** is a point-in-time backup of files and directories.
- A **repository** is the encrypted storage location holding snapshots (cloud, network or local).
- A **policy** is a set of rules for how snapshots are made and kept: compression, retention, scheduling, ignore rules.

Kopia ships as a CLI and as KopiaUI (a GUI). Provision and pay for the storage yourself first; Kopia does not do that.

## Basic CLI flow

```console
kopia repository create filesystem --path /path/to/repository
kopia repository connect filesystem --path /path/to/repository
kopia snapshot create /path/to/source
kopia snapshot list /path/to/source
```

Creation asks for a repository password. If you forget it there is absolutely no way to restore your files, so store it in a password manager. `repository create` and `repository connect` have one subcommand per storage type.

After the first snapshot prints a root ID beginning with `k`, running the command again rescans the files and uploads only changed content. All snapshots are incremental and deduplicated: only content not already in the repository is uploaded, which also applies to identical files in different places. Deduplication is automatic and needs no setting. A second run with no changes finishes almost instantly and yields the same root ID.

## Inspecting

`kopia snapshot list` shows history; identical consecutive snapshots are collapsed. `kopia diff ID1 ID2` compares two snapshots, `kopia ls -l ID` lists a snapshot directory, `kopia show OBJECT_ID` prints a file's content, and `kopia content show -j ID` shows a directory object as pretty-printed JSON.

## Checked

2026-11-03. Confirmed against the fetched Kopia docs pages: Getting Started (incremental snapshots, identical snapshot collapsing, kopia diff, ls -l, show, content show -j, forgotten-password warning) and Repositories (provision and pay for storage yourself).
Method: documentation only; no commands were run.
