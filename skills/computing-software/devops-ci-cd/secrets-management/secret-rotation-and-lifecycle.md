---
id: computing-software.devops-ci-cd.secrets-management.secret-rotation-and-lifecycle
name: secret-rotation-and-lifecycle
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, secret-rotation, credential-rotation, key-rotation, secret-lifecycle, secret-inventory, overlapping-credentials, aws-secrets-manager, rotation-lambda, awspending, awscurrent, external-secrets-operator, stakater-reloader, cert-manager, tls-certificates, secret-age]
level: advanced
status: docs-checked
description: "Rotate secrets without outages: lifecycle records, AWS Secrets Manager rotation steps and stages, Kubernetes pickup of new values, cert-manager renewal."
sources: ["https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_lambda-functions.html", "https://kubernetes.io/docs/concepts/configuration/secret/", "https://cert-manager.io/docs/usage/certificate/", "https://github.com/stakater/Reloader", "https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secret rotation and lifecycle

**Goal:** every secret can be rotated on schedule, or quickly in an emergency, without downtime and without anyone having to remember where it is used.

(Where secrets should live and leak scanning are in `computing-software.devops-ci-cd.secrets-management.secrets-and-supply-chain-hygiene`; dynamic credentials avoid rotation, see `computing-software.devops-ci-cd.secrets-management.vault-dynamic-secrets-and-leases`.)

## 1. Policy (OWASP Secrets Management Cheat Sheet)
- Rotate regularly so stolen credentials work only for a short time. Automate rotation of static secrets, because manual rotation is error-prone; at least make sure the process is well supported.
- Create secrets to expire after a defined time where possible, either actively by the consuming system or via an expiry date in the secrets manager that triggers rotation.
- Keep a record per secret: when it was created, consumed, archived, rotated and deleted, who and what did so, and when manual rotation is due.
- User credentials are excluded from regular rotation; rotate them only on suspicion or evidence of compromise (per NIST, as the cheat sheet states).
- Encryption key rotation can trigger full or partial data re-encryption. Strategies include gradual rotation (new keys for writes, old keys kept for reads), rapid and scheduled rotation.
- Prefer dynamic secrets where possible: short lease, revoke when no longer needed. Restarting an application does not revoke stolen credentials.

## 2. Overlap, then retire
An outage happens when the old credential dies before every consumer has the new one, so create the new credential first, distribute it, verify consumers use it, then revoke the old one. The AWS staging labels below implement this by retaining the previous version as `AWSPREVIOUS`.

## 3. AWS Secrets Manager rotation (worked model)
Rotation by Lambda function uses staging labels to identify versions. Four steps:
1. `createSecret`: calls `get_secret_value` with the `ClientRequestToken`; if absent, creates the version, generates a value with `get_random_password`, and stores it with label `AWSPENDING` (this helps idempotency; use `ExcludeCharacters` for characters the target does not accept).
2. `setSecret`: changes the credential in the database or service to match `AWSPENDING`. The function is a privileged deputy, so before updating check that the `AWSCURRENT` credential is valid (abandon the rotation if not), that `AWSCURRENT` and `AWSPENDING` are for the same resource (same username, same hostname), and use query parameterisation.
3. `testSecret`: uses the `AWSPENDING` value to access the database or service (templates test with read access).
4. `finishSecret`: moves `AWSCURRENT` to the new version via `update_secret_version_stage`; the previous version gets `AWSPREVIOUS`. Do not remove `AWSPENDING` yourself with a separate call, because that can signal that rotation did not complete. If `AWSPENDING` remains attached to a different version than `AWSCURRENT`, a later rotation assumes one is still in progress and errors.

Other points: start from the AWS rotation templates; the function can only rotate the secret directly (it cannot call another Lambda); avoid logging sensitive values to CloudWatch; provisioned concurrency below 10 can cause throttling; in RDS MySQL alternating-users rotation the cloned user name is limited (16 characters by default; the "_clone" suffix takes six of a 32-character maximum). Use `describe-secret` and `VersionIdsToStages` to see stages while testing. Managed rotation (no Lambda) exists for many managed secret types. Per the OWASP sheet, ensure a custom rotation function's privileged role can only be assumed by that function.

## 4. Getting consumers to pick up new values (Kubernetes)
- Secrets mounted as volumes are updated by Kubernetes with an eventually-consistent approach; the delay can be as long as the kubelet sync period plus cache propagation delay. A `subPath` volume mount does not receive automatic updates.
- Updating a Secret does not by itself restart workloads (Reloader's description). Reloader is a controller that triggers rollouts of Deployments, StatefulSets and other workloads when referenced Secrets or ConfigMaps change.
- External Secrets Operator's `refreshInterval` periodically syncs the provider value into the Kubernetes Secret; ESO does not manage rotation itself.
- A sidecar such as Vault Agent can periodically refresh a secret into a shared in-memory (`emptyDir` `medium: Memory`) volume that the application reads (OWASP example pattern).

## 5. TLS certificates
cert-manager renews a `Certificate` automatically: by default at 2/3 of the issued certificate's lifetime, or at `spec.renewBefore` / `spec.renewBeforePercentage` before expiry. Minimum `spec.duration` is 1 hour and `spec.duration` must exceed `spec.renewBefore`; a `renewBefore` very close to `duration` can cause a renewal loop.

## Verify
- [ ] Each production secret has an owner, consumers and rotation method recorded.
- [ ] A scheduled rotation ran with zero authentication errors in consumers.
- [ ] Pods pick up a changed secret (volume refresh or Reloader rollout) within the documented time.
- [ ] `describe-secret` shows `AWSCURRENT` on the new version and `AWSPREVIOUS` on the old after rotation.

## Checked
Method: docs-checked 2026-11-09 against the AWS Lambda rotation functions page, the Kubernetes Secrets concept page (volume update and kubelet sections), the cert-manager Certificate usage page (renewal sections), the Stakater Reloader README (overview) and the OWASP Secrets Management Cheat Sheet (rotation, lifecycle and AWS example sections). The AWS top-level rotation page was read but is a stub; the alternating-users and strategies pages returned no content.
Removed as unconfirmed: suggested rotation intervals (30-90 days, yearly, 2/3 for all TLS), the MySQL 8 `RETAIN CURRENT PASSWORD` and PostgreSQL "no equivalent" claims, the alternating-users procedure detail, Azure Key Vault and GCP rotation remarks, the claim that environment variables never update, the pod-template hash annotation, connection-pool lifetime advice, JWKS and `kid` signing-key rotation, envelope encryption and `aws kms enable-key-rotation`, the 14-day expiry alert rule, and the quarterly emergency-rotation rehearsal.
