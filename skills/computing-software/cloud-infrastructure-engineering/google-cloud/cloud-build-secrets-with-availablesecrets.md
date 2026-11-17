---
id: computing-software.cloud-infrastructure-engineering.google-cloud.cloud-build-secrets-with-availablesecrets
name: cloud-build-secrets-with-availablesecrets
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, cloud-build, cloud-build-secrets, availablesecrets, secret-manager, secretenv]
level: practitioner
status: docs-checked
description: "Use Secret Manager secrets in Cloud Build with availableSecrets and secretEnv, avoid leaking them in logs, and grant the build service account access."
sources: ["https://cloud.google.com/build/docs/securing-builds/use-secrets", "https://cloud.google.com/build/docs/build-config-file-schema#availablesecrets"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud Build secrets with availableSecrets

## 1. Config
```yaml
steps:
- name: gcr.io/cloud-builders/gcloud
  entrypoint: bash
  args: ['-c', 'curl -sf -H "Authorization: Bearer $$DEPLOY_KEY" https://deploy.example.com/hook']
  secretEnv: [DEPLOY_KEY]
availableSecrets:
  secretManager:
  - versionName: projects/$PROJECT_ID/secrets/deploy-key/versions/3
    env: DEPLOY_KEY
```
- Use `entrypoint: bash`, a `-c` first argument, and reference the secret in the command string as `$$VAR`; declare it in the step's `secretEnv`.
- Pin versions for reproducibility in release builds; `latest` for dev.

## 2. IAM
Grant the build's service account the Secret Manager Secret Accessor role (`roles/secretmanager.secretAccessor`) on each secret rather than the whole project.

## 3. Don't leak
- Never `echo $$SECRET` or run with `set -x`.
- Don't write secrets to files that are later uploaded as `artifacts`.

## Gotchas
- `availableSecrets.inline` holds values encrypted with a Cloud KMS key; prefer `availableSecrets.secretManager`.
- `versionName` is a full resource name (`projects/*/secrets/*/versions/*`), so a secret can live in another project; grant access there.

## Verify
- [ ] Build succeeds and build logs contain no secret values.

## Checked

2026-10-27. Confirmed in the use-secrets page and the cloudbuild v1 discovery schemas (Secrets `inline` and `secretManager`, SecretManagerSecret `env` and `versionName` format, Secret `kmsKeyName`): `entrypoint: bash`, `-c`, `$$`-prefixed environment variable in `args`, `secretEnv`, Secret Manager version names. Removed: the NPM token and Docker BuildKit `--secret` example, `--build-arg` and `docker history` claims, the `/workspace` path, the claim that logs redact nothing, default-SA wording. Read end to end.

Method: documentation only; no commands were run.
