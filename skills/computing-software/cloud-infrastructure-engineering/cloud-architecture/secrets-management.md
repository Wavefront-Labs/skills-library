---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.secrets-management
name: secrets-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, secrets-management, secrets-manager, key-vault, secret-manager, hashicorp-vault, dynamic-secrets, secret-rotation, secret-scanning, external-secrets-operator]
level: practitioner
status: docs-checked
description: "Architect secrets handling: prefer managed identity, a vault per app and environment, runtime retrieval, rotation, Vault dynamic credentials and External Secrets Operator."
sources: ["https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html", "https://learn.microsoft.com/azure/key-vault/general/best-practices", "https://developer.hashicorp.com/vault/docs/secrets", "https://external-secrets.io/latest/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secrets management architecture

## Order of preference
1. **No secret**: use managed identities for app and service connections to Key Vault and other
   services, which Microsoft recommends to eliminate hard-coded credentials.
2. **Dynamic secrets**: Vault secrets engines can connect to other services and generate dynamic
   credentials on demand; Vault leases are tied to the path where they were created.
3. **Stored secrets with automatic rotation**: AWS Secrets Manager can rotate database credentials,
   application credentials, OAuth tokens and API keys on a schedule, replacing long-term secrets
   with short-term ones. Rotation uses a Lambda function (managed rotation excepted). Azure Key Vault
   recommends autorotation of keys, secrets and certificates.
4. Remaining static secrets: stored in a vault, logged, rotated.

## Design
- **Separate vaults** (Microsoft): one Key Vault per application, region and environment, because a
  vault is a security boundary and sharing one increases blast radius; per tenant in multitenant SaaS.
- **Access control**: Key Vault uses Entra ID with separate control and data planes; use Azure RBAC,
  not legacy access policies; just-in-time (PIM) roles for administrators, with approvals and MFA.
- **Retrieve at runtime**: AWS replaces hard-coded credentials with a runtime call to Secrets Manager,
  so rotating a credential does not require redeploying clients. On Kubernetes, External Secrets Operator
  syncs secrets from AWS Secrets Manager, HashiCorp Vault, Google Secrets Manager, Azure Key Vault
  and others into Kubernetes Secrets through the ExternalSecret, SecretStore and ClusterSecretStore resources.
- **Use the right store**: AWS recommends IAM for AWS credentials, KMS for encryption keys, ACM for
  private keys and certificates; Microsoft says not to store certificates as secrets or use Key Vault as a
  configuration or customer-data store.
- **Protect the vault**: Key Vault soft delete (7 to 90 day retention) and purge protection; Private
  Link or firewall; TLS 1.2 or 1.3; audit logging; Defender for Key Vault; Event Grid notifications;
  native backup, with restores tested.
- **Two valid credentials during rotation**: AWS documents an alternating-users rotation tutorial.

## Leak response
Revoke or rotate first, then investigate usage in audit logs. Secret scanning tools are not covered by
the cited pages.

## Verify
- [ ] Inventory of static secrets with owner and last rotation date.
- [ ] Rotation tested end to end without downtime.
- [ ] Separate vaults per environment; no legacy access policies.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the AWS Secrets Manager introduction, the Azure Key Vault security page, the Vault secrets
engines page and the External Secrets Operator introduction. Removed as not on those pages: CSI Secrets
Store driver, ECS and Lambda injection, App Service references, caching TTL advice, gitleaks, GitHub push
protection, Terraform-state warnings, and IAM database authentication.
