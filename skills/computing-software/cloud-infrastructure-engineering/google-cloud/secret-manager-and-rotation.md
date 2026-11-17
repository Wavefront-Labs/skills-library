---
id: computing-software.cloud-infrastructure-engineering.google-cloud.secret-manager-and-rotation
name: secret-manager-and-rotation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, secret-manager, secrets, secret-rotation, secret-versions, secret-replication, cmek-secrets, secret-iam, secret-accessor, rotation-schedule, pubsub-rotation-notification, cloud-run-secrets, gke-secret-manager-csi, external-secrets-operator, regional-secrets, secret-expiry, secret-annotations, delayed-destruction]
level: practitioner
status: docs-checked
description: "Use Secret Manager well: version lifecycle, per-secret IAM, replication and CMEK, rotation with Pub/Sub, delayed destruction, and mounting secrets in Cloud Run, GKE and Terraform."
sources: ["https://cloud.google.com/secret-manager/docs/overview", "https://cloud.google.com/secret-manager/docs/best-practices", "https://cloud.google.com/secret-manager/docs/secret-rotation", "https://cloud.google.com/secret-manager/docs/destroy-secret-version", "https://cloud.google.com/secret-manager/docs/event-notifications", "https://cloud.google.com/secret-manager/quotas", "https://cloud.google.com/run/docs/configuring/services/secrets", "https://cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Secret Manager and rotation

**Goal:** no credential lives in code, env files, or Terraform state in plaintext; every
read is audited; and a leaked value can be rotated without a deploy.

## 1. Create and version
```bash
gcloud secrets create db-password --replication-policy=user-managed --locations=europe-west1,europe-west4 \
  --kms-key-name=projects/prj-p-kms/locations/europe-west1/keyRings/payments/cryptoKeys/secrets \
  --labels=app=orders --set-annotations=owner=payments-team \
  --version-destroy-ttl=7d                      # delayed destruction: a destroy request disables the version and schedules destruction
printf '%s' "$PASSWORD" | gcloud secrets versions add db-password --data-file=-
gcloud secrets versions access latest --secret=db-password
```
- Secrets are containers; **versions** hold bytes (≤64 KiB). `latest` is an alias — pin versions in prod configs (`projects/P/secrets/db-password/versions/3`) and roll forward deliberately, or accept that `latest` changes under you.
- Replication: `automatic` (Google picks regions) vs `user-managed` for residency. **Regional secrets** (`--location`) are a separate regional option.
- Version states: `ENABLED` → `DISABLED` (access fails until re-enabled) → `DESTROYED` (contents discarded, permanent, cannot be restored). With delayed destruction on the secret, a destroy request instead disables the version and schedules destruction, and an admin can restore it during the delay. Disable first, destroy later.

## 2. IAM (the whole point)
- `roles/secretmanager.secretAccessor` on the **secret** (not the project) to the workload SA; `secretVersionManager` for the rotation job; `admin` for humans only in non-prod.
- Every `AccessSecretVersion` is a Data Access audit log entry (enable `DATA_READ` for `secretmanager.googleapis.com`, see `cloud-audit-logs`); alert on access from unexpected principals.

## 3. Consume
| Runtime | How |
|---|---|
| **Cloud Run / Functions** | `--set-secrets=DB_PASSWORD=db-password:latest` (env) or `--set-secrets=/etc/secrets/db=db-password:3` (file mount); a mounted volume fetches the value from Secret Manager on read, and Google recommends pinning a version rather than `latest` |
| **GKE** | Secret Manager **CSI component** (`--enable-secret-manager` add-on) + `SecretProviderClass` → files in the pod, using Workload Identity Federation for GKE |
| **Compute Engine** | at boot: `gcloud secrets versions access` with the VM service account; never bake into images |
| **Cloud Build** | `availableSecrets.secretManager` (`versionName`, `env`) in `cloudbuild.yaml` plus `secretEnv` on the step |
| **Terraform** | the `google_secret_manager_secret_version` resource has write-only `secret_data_wo` / `secret_data_wo_version` arguments that are not stored in state; avoid a literal `secret_data` |
| Apps | client libraries with ADC; cache values rather than reading per request (access quotas are per secret: see the quotas page) |

## 4. Rotation
Secret Manager triggers a `SECRET_ROTATE` message to the topics at the secret's next rotation time; it does not change the value itself:
```bash
gcloud pubsub topics create secret-rotation
gcloud secrets update db-password --next-rotation-time=2026-11-01T00:00:00Z --rotation-period=2592000s \
  --add-topics=projects/P/topics/secret-rotation
```
Grant the Secret Manager service agent (`service-<PN>@gcp-sa-secretmanager.iam.gserviceaccount.com`) `pubsub.publisher`. A Cloud Run function subscribes, generates a new credential at the source (Cloud SQL user, API provider), adds a version, then disables the previous one after consumers pick it up. Notifications are also sent for events such as `SECRET_VERSION_ADD` and `SECRET_VERSION_DESTROY` — use them to trigger redeploys.
Zero-downtime pattern: dual credentials (two DB users A/B) so the new version is valid before the old is revoked.

## Gotchas
- `printf` not `echo` when adding versions — a trailing newline becomes part of the password and nobody finds it for a week.
- Secret payload limit is 64 KiB; large JSON configs do not fit — store a reference or split.
- Automatic replication lets Google choose regions — set `user-managed` when residency matters.

## Verify
- [ ] `gcloud secrets get-iam-policy db-password` lists only workload SAs with `secretAccessor`; project-level `secretmanager.*` roles absent in prod.
- [ ] Accessing a version appears in the Data Access log with the caller within a minute.
- [ ] Rotation topic receives a message at `next-rotation-time` (test with a 1-hour period on a sandbox secret).
- [ ] On a secret with delayed destruction, `gcloud secrets versions destroy` leaves the version disabled and scheduled for destruction, and an admin can restore it during the delay.

## Checked
2026-10-28. Confirmed on the Secret Manager destroy, disable, access, event-notification, rotation, IAM, quotas, audit-logging and GKE add-on pages, the Cloud Run secrets page, the Cloud Build use-secrets page and the google_secret_manager_secret_version provider doc: 64 KiB limit, delayed destruction behaviour, DATA_READ for AccessSecretVersion, roles, `--enable-secret-manager`, SecretProviderClass, SECRET_ROTATE and SECRET_VERSION_ADD/DESTROY events, publisher grant to the service agent, Cloud Build `availableSecrets`, write-only Terraform arguments. gcloud commands and flags passed check_commands. Removed: External Secrets Operator, CMEK replica note, org-constraint claim, env-var revision claim, deletion semantics, `--etag`/`--ttl` purposes, metrics-free quota figure.
Method: documentation only; no commands were run.
