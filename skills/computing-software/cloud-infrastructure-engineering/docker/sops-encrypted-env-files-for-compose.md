---
id: computing-software.cloud-infrastructure-engineering.docker.sops-encrypted-env-files-for-compose
name: sops-encrypted-env-files-for-compose
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, secrets, sops, age, env-file, compose-secrets, gitops]
level: advanced
status: docs-checked
description: "Keep Compose secrets in Git encrypted with SOPS and age or a cloud KMS, decrypt at deploy time into a process environment or a Compose secret file."
sources: ["https://github.com/getsops/sops", "https://github.com/getsops/sops/blob/v3.9.4/README.rst", "https://docs.docker.com/compose/how-tos/use-secrets/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SOPS-encrypted env files for Compose

SOPS is an editor of encrypted files for YAML, JSON, ENV, INI and BINARY formats. It encrypts
with AWS KMS, GCP KMS, Azure Key Vault, age and PGP, so encrypted files can live in Git.

## Set up keys
```bash
age-keygen -o ~/.config/sops/age/keys.txt          # default key file location on Linux
# .sops.yaml at repo root
creation_rules:
  - path_regex: deploy/prod\..*          # rules are evaluated in order, the first match wins
    kms: <kms-key-arn>
  - path_regex: deploy/.*\.env$
    age: <age-recipient-public-key>   # age1... from age-keygen output
```
```bash
sops encrypt -i deploy/prod.env      # encrypt in place; creation rule chosen by path
sops deploy/prod.env                 # edit decrypted in $EDITOR, re-encrypts on save
```
`SOPS_AGE_KEY_FILE` overrides the key file location; `SOPS_AGE_KEY` supplies the key directly.

## Deploy without plaintext files
```bash
# 1. decrypted values go only into the child process environment
sops exec-env deploy/prod.env 'docker compose -f compose.yaml up -d'
```
SOPS documents `exec-env` as making the decrypted contents available only to that process
and never written to disk.

```bash
# 2. file-based secrets: decrypt one value into a file and use a Compose secret
sops decrypt --extract '["DB_PASSWORD"]' deploy/prod.yaml > <secrets-dir>/db_password
docker compose up -d
```
```yaml
services:
  app:
    secrets: [db_password]
    environment: { DB_PASSWORD_FILE: /run/secrets/db_password }
secrets:
  db_password:
    file: <secrets-dir>/db_password
```
Compose mounts each secret as a file at `/run/secrets/<secret_name>` (Linux containers only).
The `_FILE` variable is a convention used by some images such as the mysql and postgres
Official Images. Put `<secrets-dir>` on a tmpfs or other non-persistent location and restrict
its permissions. `sops exec-file` can instead pass a decrypted file through a FIFO.

## Key changes
- `sops updatekeys <file>` applies the recipients now in `.sops.yaml` without rotating the
  data key (the SOPS team's recommended approach to changing recipients).
- `sops rotate -i <file>` generates a new data key and re-encrypts the values; rotate after
  removing keys.

## Gotchas
- Decrypting to a plaintext file in the project directory leaves plaintext that can be
  committed or copied into build contexts. Avoid it, or ignore that file in `.gitignore`
  and `.dockerignore`.
- Compose docs note that environment variables are often available to all processes and can
  be printed in logs when debugging; file secrets give per-service access control.

## Checked
2026-11-09. Confirmed in the SOPS README (v3.9.4): formats and backends, age key file path and
`SOPS_AGE_KEY_FILE` / `SOPS_AGE_KEY`, first-match creation rules, `encrypt -i`, `rotate -i`,
`updatekeys`, `exec-env`, `exec-file` FIFO, `--extract`. Confirmed in the Docker Compose secrets
page: `/run/secrets/<name>`, Linux only, `_FILE` convention. Removed: the claim that dotenv
files cannot hold multi-line values, that `/run` is tmpfs on most distros, `docker inspect`
exposure, `${VAR}` interpolation behaviour, `.env` auto-load, CI advice, a real-looking KMS ARN.
Method: documentation only; no commands were run.
