---
id: computing-software.systems-network-administration.restic.copy-between-repos
name: copy-between-repos
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, copy, replication, from-repo, chunker-params, deduplication]
level: advanced
status: docs-checked
description: "Copy snapshots between restic repositories with restic copy, --from-repo credentials, filters, and shared chunker parameters for deduplication."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
  - https://restic.readthedocs.io/en/stable/075_scripting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Copying snapshots between repositories

`copy` reads from a source repository and writes to the one given by `-r`:

```
restic -r /srv/restic-repo2 copy --from-repo /srv/restic-repo
```

## Source credentials

- `--from-repo` or `RESTIC_FROM_REPOSITORY`
- `--from-repository-file` or `RESTIC_FROM_REPOSITORY_FILE`
- `--from-password-file` or `RESTIC_FROM_PASSWORD_FILE`
- `--from-password-command` or `RESTIC_FROM_PASSWORD_COMMAND`
- `RESTIC_FROM_PASSWORD`
- `--from-key-hint` or `RESTIC_FROM_KEY_HINT` (key ID to try first when opening the source)

## Behaviour

The command copies all snapshots from the source to the destination, which must already exist. Snapshots already
copied are skipped by later runs (shown only with `--verbose`). Snapshots are copied in batches, so "snapshot saved"
messages can appear some time after the content was copied. If copy is aborted it resumes when run again; up to 10
minutes of progress can be lost.

## Filtering

Limit what is copied with `--host`, `--path` and a comma-separated `--tag foo,bar` list, or name snapshot IDs
(including `latest`) to copy only those.

## Keep deduplication working

Copying does not re-chunk files, so deduplication can break between copied files and files already in the
destination, and files present in both may occupy up to twice their space there. Chunker parameters are generated
once when a repository is created and cannot be changed afterwards, so initialise the destination with the source's:

```
restic -r /srv/restic-repo2 init --from-repo /srv/restic-repo --copy-chunker-params
```

The page gives transferring snapshots from a local to a remote repository as an example use.

## Checked
Compared with the "Working with repositories" and "Scripting" pages: the copy command line, `--from-*` options and
`RESTIC_FROM_*` variables, skip and resume behaviour, filters, no re-chunking and the `init --copy-chunker-params`
step. Removed: the claim about a "different polynomial" mechanism, "supported way for off-site redundancy", the
`RESTIC_PASSWORD*` statement for the destination and the final `snapshots` check (none stated on the cited pages).
Method: docs-only read of cited pages, 2026-11-08
