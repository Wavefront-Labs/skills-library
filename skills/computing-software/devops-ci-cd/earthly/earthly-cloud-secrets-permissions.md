---
id: computing-software.devops-ci-cd.earthly.earthly-cloud-secrets-permissions
name: earthly-cloud-secrets-permissions
category: computing-software
field: devops-ci-cd
product: earthly
tags: [earthly, cloud-secrets, earthly-secret, earthly-org, earthly-project, permissions, earthly-token, registry]
level: practitioner
status: docs-checked
description: "Set up Earthly Cloud: account, org, project, EARTHLY_TOKEN for CI, cloud secrets (earthly secret, /user/), access levels, and registry login via earthly registry setup."
sources:
  - https://github.com/earthly/earthly/blob/main/docs/cloud/overview.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/cloud-secrets.md
  - https://github.com/earthly/earthly/blob/main/docs/cloud/managing-permissions.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Earthly Cloud secrets, orgs and permissions

## Account, org, project
```bash
earthly account register --email <email>
earthly account register --email <email> --token <token>   # token arrives by email
earthly org create <org-name>
earthly org select <org-name>
earthly org ls
earthly project create <project-name>
```
CI login: `earthly account create-token [--write] <token-name>`, then export it as `EARTHLY_TOKEN=...` in the CI.

## Secrets
Each project has an isolated secret store.
```bash
earthly secret --project <project-name> ls
earthly secret --project <project-name> set my_key 'hello world'
earthly secret --project <project-name> get my_key
```
Keys starting with `/user/` are private to the current user and never shared; org and project are not needed:
```bash
earthly secret set /user/my_private_key 'hello private world'
earthly secret get /user/my_private_key
```
Use them in an Earthfile after declaring the project under `VERSION`:
```Dockerfile
VERSION 0.8
PROJECT <org-name>/<project-name>
RUN --secret MY_KEY=my_key echo $MY_KEY
RUN --secret MY_KEY=/user/my_private_key echo $MY_KEY
```
Registry login stored in cloud secrets (host may be omitted for DockerHub):
```bash
earthly registry --org <org-name> --project <project-name> setup --username <registry-user-name> --password-stdin <host>
earthly registry --org <org-name> --project <project-name> setup --cred-helper ecr-login --aws-access-key-id <key> --aws-secret-access-key <secret> <host>
earthly registry --org <org-name> --project <project-name> setup --cred-helper gcloud --gcp-service-account-key <key> <host>
```
Migrating 0.6 secrets: `earthly secret --org <org-name> --project <project-name> migrate <source-org-name>`; change `+secrets/<org-name>/<secret-key>` references to `<secret-key>`; user secrets are not migrated.

## Access levels
Two boundaries: orgs (hold satellites and projects) and projects (hold secrets and build history/logs). Levels: `read`; `read+secrets` (view and use secrets); `write` (create and modify secrets, plus satellites and projects at org level); `admin` (manage users). An org level grants the same level on all its projects.
```bash
earthly org invite --permission <access-level> <email>
earthly org member update --permission <permission> <email>
earthly org member rm <email>
earthly project --project <project-name> member add --permission <access-level> <email>
earthly project --project <project-name> member update --permission <permission> <email>
earthly project --project <project-name> member rm <email>
```
Only users already in the org can be added to a project.

## Checked

2026-11-07. Read from a clone of the earthly/earthly repository's docs directory: cloud/overview.md, cloud/cloud-secrets.md, cloud/managing-permissions.md. Commands, flags, defaults, values and code snippets in this skill were matched to that page text. Changes: none; every claim matched the page text.

Method: documentation only; no commands were run.
