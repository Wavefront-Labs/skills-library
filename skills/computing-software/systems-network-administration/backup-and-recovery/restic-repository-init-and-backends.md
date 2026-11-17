---
id: computing-software.systems-network-administration.backup-and-recovery.restic-repository-init-and-backends
name: restic-repository-init-and-backends
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic, restic-init, restic-backends, rest-server, append-only, s3, sftp, backup]
level: practitioner
status: docs-checked
description: "Create restic repositories on local disk, SFTP, rest-server (append-only), S3, B2, Azure or rclone backends, with environment-based credentials and a first backup."
sources:
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
  - https://restic.readthedocs.io/en/stable/040_backup.html
  - https://github.com/restic/rest-server
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic repository init and backends

**Goal:** an encrypted, deduplicated repository on the right storage, ready for scheduled backups.

## Credentials via environment
```bash
export RESTIC_REPOSITORY='s3:https://s3.eu-west-1.amazonaws.com/acme-backups/web01'
export RESTIC_PASSWORD_FILE=/etc/restic/password       # chmod 600, escrow a copy
export AWS_ACCESS_KEY_ID=... AWS_SECRET_ACCESS_KEY=...
restic init
```
New repositories use format version 2 (compression; needs restic 0.14.0 or newer), the current default; `init --repository-version` selects another version.

## Backends
| Backend | Repository string |
|---|---|
| Local | `/srv/restic-repo` |
| SFTP | `sftp:backup@nas.example:/srv/restic/web01` |
| REST server | `rest:https://user:pass@backup.example:8000/web01/` |
| S3 / compatible | `s3:https://s3.example.com/bucket/prefix` |
| Backblaze B2 | `b2:bucket:prefix` (the manual recommends B2's S3-compatible API instead) |
| Azure Blob | `azure:container:/prefix` (`AZURE_ACCOUNT_NAME`, `AZURE_ACCOUNT_KEY`) |
| Google Cloud Storage | `gs:bucket:/prefix` |
| rclone (anything rclone supports) | `rclone:remote:path` |

## Ransomware-resistant option: rest-server append-only
```bash
rest-server --path /srv/restic --append-only --private-repos --tls
```
Clients can add snapshots but cannot delete or overwrite data; run `forget`/`prune` from a trusted admin host with full access (see the restic-rest-server-append-only skill). With `--tls`, the server looks for its private and public key in the data directory unless `--tls-cert` and `--tls-key` are given.

## First backup
```bash
restic backup /etc /srv/www --exclude-file=/etc/restic/excludes --one-file-system --tag nightly
restic snapshots
```

## Gotchas
- The password is the only key: lose it and the data is gone. Escrow it.
- Parallel access, including parallel writes, from several hosts is supported by the repository design; during `prune` the repository is locked and backups cannot complete, so schedule prune apart.

## Verify
`restic snapshots` lists the first snapshot, and `restic check` passes.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: repository string forms for local, sftp, rest, s3, b2, azure, gs, rclone (030), AZURE_ACCOUNT_NAME/KEY, RESTIC_PASSWORD_FILE, repository v2 default, rest-server flags --path, --append-only, --private-repos, --tls (rest-server README), locking behaviour. Removed the unconfirmed S3 Object Lock claim.

Method: documentation only; no commands were run.
