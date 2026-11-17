---
id: computing-software.systems-network-administration.backup-and-recovery.restic-rest-server-append-only
name: restic-rest-server-append-only
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [rest-server-append-only, append-only-backup, restic, immutable-backup, ransomware-resilience, rest-server]
level: advanced
status: docs-checked
description: "Make restic backups deletion-resistant with rest-server in append-only mode: setup, TLS and htpasswd, private repos, running forget/prune from a trusted host, and limits."
sources:
  - https://github.com/restic/rest-server
  - https://restic.readthedocs.io/en/stable/030_preparing_a_new_repo.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# restic with rest-server append-only

A compromised client holding the repo password can run `restic forget --prune` and destroy
its backups. **rest-server** in `--append-only` mode allows creating new backups but prevents deletion and modification of existing ones, so clients can add snapshots but not remove data.

## Server
```sh
rest-server --path /srv/restic --listen :8000 --append-only --private-repos \
  --tls --tls-cert /etc/rest-server/cert.pem --tls-key /etc/rest-server/key.pem \
  --htpasswd-file /etc/rest-server/.htpasswd --prometheus
htpasswd -B -c /etc/rest-server/.htpasswd web01
```
`--private-repos` grants a user access only when the repository URL starts with a subdirectory named like the user (`/web01/...`). `htpasswd` (Apache tools) is needed to create the file; only bcrypt (`-B`) and SHA are supported. Without `--no-auth`, rest-server refuses to start if it cannot open the `.htpasswd` file. `--prometheus` serves metrics at `/metrics`, authenticated for the `metrics` user unless `--prometheus-no-auth` is set.

## Client
```sh
export RESTIC_REPOSITORY=rest:https://web01:secret@backup.corp.example:8000/web01/
export RESTIC_PASSWORD_FILE=/root/.restic-pass
restic init
restic backup /etc /var/www
```

## Retention without giving clients delete rights
`forget` and `prune` need full read, write and delete access, which voids append-only protection, so run them from a separate, well-secured **trusted maintenance host**, for example with direct filesystem access or a second rest-server instance without `--append-only` reachable only from that host:
```sh
restic -r /srv/restic/web01 forget --keep-daily 14 --keep-weekly 8 --keep-monthly 12 --prune
```
Review snapshots before pruning: an attacker could have added junk snapshots so that
"keep-last" policies push out good ones; prefer time-based keep rules (`--keep-within`).

## Limits
- Append-only protects the stored data, not the repository password: an attacker can still
  read (exfiltrate) data. Keep the password secret and use per-host repos.
- Locks: `restic unlock` works even against a repository served append-only.
- Append-only is not a compliance-grade immutability guarantee; the restic manual recommends a separate, well-secured client for maintenance.

## Verify
From a client: `restic forget --keep-last 1 --prune` is denied; normal
backup succeeds; maintenance host prune works and `restic check` passes.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. rest-server README on master (last commit 2026-10-18, release v0.14.0). Confirmed: flags --path, --listen (default :8000), --append-only, --private-repos, --tls, --tls-cert, --tls-key, --htpasswd-file, --prometheus, --prometheus-no-auth, --no-auth behaviour, bcrypt/SHA htpasswd, per-user path rule, unlock under append-only, --keep-within advice (060_forget).

Method: documentation only; no commands were run.
