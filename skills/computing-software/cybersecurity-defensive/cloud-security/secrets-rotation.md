---
id: computing-software.cybersecurity-defensive.cloud-security.secrets-rotation
name: secrets-rotation
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [cloud-data-protection, secrets-rotation, aws-secrets-manager, azure-key-vault, rotation-lambda, database-credentials, dynamic-secrets, hashicorp-vault]
level: practitioner
status: draft
description: "Rotate secrets automatically: Secrets Manager/Key Vault rotation, dual-credential patterns to avoid downtime, dynamic secrets, and finding unrotated long-lived credentials."
sources: ["AWS Secrets Manager User Guide - Rotate secrets (rotation strategies)", "Microsoft Learn - Azure Key Vault secret rotation", "HashiCorp Vault - Database secrets engine (dynamic credentials)", "OWASP Secrets Management Cheat Sheet"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secrets rotation

**Goal:** credentials change regularly and automatically, so leaked secrets expire, and rotation
never causes an outage.

## Patterns
| Pattern | How | Downtime risk |
|---|---|---|
| Single user | Change the password of the one account, update the secret | Brief failures while clients have the old value |
| Alternating users | Two DB users; rotation updates the inactive one and switches the secret | None (recommended) |
| Dynamic secrets | Vault/IAM generate short-lived credentials per client (TTL minutes-hours) | None; no long-lived secret at all |
| Workload identity | No secret: IAM roles, managed identities, OIDC federation | Best where supported |

## AWS Secrets Manager
- Managed rotation for RDS/Aurora/Redshift/DocumentDB (`--rotation-rules AutomaticallyAfterDays=30`), alternating-users strategy via the templates.
- Custom rotation Lambda for other secrets implements `createSecret`, `setSecret`, `testSecret`, `finishSecret` steps.
- Clients fetch the secret at runtime with caching (AWS SDK caching libraries), not at deploy time.

## Azure Key Vault
Event Grid `SecretNearExpiry` triggers a Function that rotates the credential and writes a new
version; storage account keys and SQL credentials have documented two-key rotation patterns.
Prefer managed identities to secrets altogether.

## Find what is not rotated
- Inventory: secrets with no rotation configured, IAM access keys older than 90 days
  (`aws iam generate-credential-report`), service principal secrets near or past expiry, PATs.
- Secret scanning in repos and CI logs for leaked values; leaked = rotate now.

## Gotchas
- Apps that cache the secret forever break after rotation; test rotation in staging and make clients refresh on auth failure.
- Rotating a secret that other teams copied into their own config breaks them; single source of truth.
- Rotation Lambda needs network access to the database (VPC) and to Secrets Manager (endpoint).

## Verify
- [ ] Rotation runs successfully on schedule (rotation status and CloudTrail `RotationSucceeded`).
- [ ] Forced rotation in staging causes no application errors.
