---
id: computing-software.devops-ci-cd.earthly.earthly-secrets-and-registry-commands
name: earthly-secrets-and-registry-commands
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, secrets, registry, cred-helper, ecr-login, gcloud, docker-login, project]
level: practitioner
status: docs-checked
description: "Store cloud secrets with earthly secrets set/get/ls/rm and registry credentials with earthly registry setup (none, ecr-login, gcloud); Docker login works out of the box."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/earthly-command/earthly-command.md
  - https://github.com/earthly/earthly/blob/main/docs/guides/auth.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# earthly secrets and registry commands

## Secrets store
```
earthly [options] secrets [--org <organization-name>, --project <project>] (set|get|ls|rm|migrate|permission)
```
(`earthly secret` is an alias.) `--org` is the organization the project belongs to; `--project` is where secrets are stored.
- `secrets set <path> <value>`, or `secrets set --file <local-path> <path>`, or `--stdin` to read from stdin.
- `secrets get [-n] <path>`: `-n` omits the trailing newline.
- `secrets ls [<path>]`, `secrets rm <path>`.
- `secrets migrate`: move existing secrets into the project-based structure; `--dry-run` prints what would happen.
- `secrets permission (ls|set|rm)`: user-level permissions.

## Registry credentials
```
earthly [options] registry [--org <org> --project <project>] (setup|list|remove)
```
Credentials are kept in the earthly-cloud secrets store under `std/registry/<host>/...` (also settable with `earthly secrets`). With `--org` and `--project` they attach to the project named by the `PROJECT` Earthfile command, which is used in CI; without them the personal store is used.

Username and password (`--cred-helper=none`):
```
earthly registry setup --username <username> --password <password> [<host>]
```
AWS ECR:
```
earthly registry setup --cred-helper ecr-login --aws-access-key-id <key> --aws-secret-access-key <secret> <host>
```
GCP:
```
earthly registry setup --cred-helper gcloud --gcp-service-account-key <key> <host>
```
Other options: `--password-stdin`, `--gcp-service-account-key-path <path>`, `--gcp-service-account-key-stdin`; `registry list`; `registry remove <host>` deletes stored credentials.

## Plain Docker credentials
Docker authentication works out of the box (for `FROM` of private images and `SAVE IMAGE --push`); just run `docker login --username <username>` first. Docker credential helpers also work.

## Gotcha
The first GCP example on the reference page writes `--gcp-key`, but the options list names only `--gcp-service-account-key` (plus its path and stdin variants); use the listed option names.

## Checked

2026-11-07. Read docs/guides/auth.md in full and the secrets and registry sections of earthly-command.md (about lines 876-1158), not the whole of that large page. Subcommands, flags, credential helper options and storage path match. Nothing removed.
Method: documentation only; no commands were run.
