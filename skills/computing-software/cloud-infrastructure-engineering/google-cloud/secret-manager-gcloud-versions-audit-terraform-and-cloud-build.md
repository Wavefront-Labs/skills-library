---
id: computing-software.cloud-infrastructure-engineering.google-cloud.secret-manager-gcloud-versions-audit-terraform-and-cloud-build
name: secret-manager-gcloud-versions-audit-terraform-and-cloud-build
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, secret-manager, gcloud-secrets, secret-create-gcloud, secret-version-destroy, disable-version, secret-access-logging, secret-audit, secret-terraform, secrets-in-cloud-build]
level: practitioner
status: docs-checked
description: "Operate Secret Manager day to day: version secrets with gcloud, disable and destroy versions safely, audit access, keep values out of Terraform state, Cloud Build."
sources: ["https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets", "https://cloud.google.com/secret-manager/docs/destroy-secret-version", "https://cloud.google.com/secret-manager/docs/disable-secret-version", "https://cloud.google.com/secret-manager/docs/audit-logging", "https://cloud.google.com/build/docs/securing-builds/use-secrets", "https://raw.githubusercontent.com/hashicorp/terraform-provider-google/main/website/docs/r/secret_manager_secret_version.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret Manager: gcloud, versions, audit, Terraform and Cloud Build

## 1. Create and add versions
```bash
gcloud secrets create stripe-key --replication-policy=user-managed --locations=europe-west2,europe-west1 \
  --labels=owner=payments --version-destroy-ttl=7d
printf '%s' "$NEW_VALUE" | gcloud secrets versions add stripe-key --data-file=-   # no trailing newline, not in shell history
gcloud secrets versions access latest --secret=stripe-key          # debugging only
gcloud secrets versions list stripe-key
```
Grant access per secret, not per project:
`gcloud secrets add-iam-policy-binding stripe-key --member=serviceAccount:<SA> --role=roles/secretmanager.secretAccessor`.

## 2. Version lifecycle
| Action | Reversible | Use |
|---|---|---|
| `versions disable 3` | yes (`enable`) | after rotation, before destroy, to find hidden consumers |
| `versions destroy 3` | no (with delayed destruction on the secret, the version is disabled and scheduled, and an admin can restore it during the delay) | after the disable soak period |
Rotation flow: add v4 → consumers pinned to `latest` pick it up on restart/refresh → disable v3 →
watch errors → destroy v3. `--next-rotation-time`/`--rotation-period` with `--add-topics` only
sends `SECRET_ROTATE` to a Pub/Sub topic; your rotator function does the work.

## 3. Audit access
`AccessSecretVersion` is a **Data Access (DATA_READ)** log — enable Data Access audit logs for `secretmanager.googleapis.com`
on projects holding secrets. Query:
`protoPayload.serviceName="secretmanager.googleapis.com" protoPayload.methodName="google.cloud.secretmanager.v1.SecretManagerService.AccessSecretVersion"`.
Alert when a human principal reads production secrets.

## 4. Terraform without values in state
Create the secret container and IAM in Terraform; add versions outside (rotator, CI, manual). If
Terraform must set the value, use the write-only argument (`secret_data_wo` with
`secret_data_wo_version`) so it is not stored in state. The provider doc warns that other arguments, such as `secret_data`, are stored in state.

## 5. Cloud Build
```yaml
steps:
- name: node:20
  entrypoint: bash
  args: ['-c', 'npm config set //registry.npmjs.org/:_authToken=$$NPM_TOKEN && npm ci']
  secretEnv: [NPM_TOKEN]
availableSecrets:
  secretManager:
  - versionName: projects/$PROJECT_ID/secrets/npm-token/versions/latest
    env: NPM_TOKEN
```
`$$` escapes substitution; the build SA needs `secretAccessor` on that secret. Never `echo` secrets — build logs are readable by many.

## Gotchas
- Automatic replication stores copies in any region; use `user-managed` for residency.
- Pin secret versions rather than `latest` for predictable behaviour (Google's Cloud Run guidance).
- Destroying a version still referenced by a pinned deployment breaks it.

## Verify
- [ ] `gcloud secrets get-iam-policy stripe-key` lists only the consuming SAs.
- [ ] An access by a test user appears in Data Access logs.

## Checked
2026-10-28. Confirmed on the Secret Manager destroy-secret-version, disable-secret-version, audit-logging, event-notification and secret-rotation pages, the Cloud Build use-secrets page and the google_secret_manager_secret_version provider doc: delayed destruction, DATA_READ AccessSecretVersion, SECRET_ROTATE, `availableSecrets.secretManager` with `versionName`/`env`/`secretEnv`, `secret_data_wo` and `secret_data_wo_version`. gcloud commands and flags passed check_commands. Fixed: rotation flag is `--add-topics`. Removed: Terraform 1.11 gate, Cloud Run env-var timing claim, one-week soak period, cold-start claim, dead page link.
Method: documentation only; no commands were run.
