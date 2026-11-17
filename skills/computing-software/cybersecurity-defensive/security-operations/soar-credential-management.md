---
id: computing-software.cybersecurity-defensive.security-operations.soar-credential-management
name: soar-credential-management
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [soar-credential-management, soar-automation, service-accounts, secrets-management, least-privilege, vault, privileged-access]
level: advanced
status: draft
description: "Manage credentials for security automation accounts: least privilege per action, vault integration, rotation, scoping destructive permissions and monitoring automation accounts."
sources: ["https://docs.splunk.com/Documentation/SOAR/current/Admin/Assets", "https://developer.hashicorp.com/vault/docs", "https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Credential handling for automation accounts

SOAR platforms hold keys to disable users, isolate hosts and block traffic everywhere. Compromise
of the SOAR = compromise of your defences.

## Principles
- **One identity per integration**, per environment. Never share an admin account across assets.
- **Least privilege per action**: separate read (enrichment) credentials from write (response)
  credentials; e.g. Entra app with `User.Read.All` for enrichment, another with
  `User.EnableDisableAccount.All` for response, gated by approval.
- Prefer workload identities without static secrets: Azure managed identity for Logic Apps,
  AWS IAM roles for Lambda/SOAR on EC2, OIDC federation.
- Scope destructive permissions narrowly: AD delegation to disable users only in user OUs (not
  admin OUs); EDR API key with isolate only.

## Storage
- Use the platform's encrypted credential store, or fetch from an external vault at runtime
  (HashiCorp Vault, CyberArk, Azure Key Vault integrations) with short TTL secrets.
- No secrets in playbook code, comments or exported content.

## Rotation
Rotate on schedule (90 days or vault-dynamic) and on staff changes with platform admin rights;
track expiry (Entra app secrets expire silently and break playbooks).

## Monitoring
- Baseline automation account behaviour (source IPs, actions); alert on use from anywhere but the
  SOAR host IPs or outside expected APIs.
- Audit SOAR admin actions (asset edits, playbook changes).
- Conditional access / IP restrictions for service principals where supported.

## Gotchas
- Broad API keys created during PoC often remain in production; re-issue at go-live.
- Approval prompts are ineffective if the same analyst can approve their own actions.

## Verify
Inventory: every asset credential mapped to owner, scope, expiry and last rotation; test that the
response credential cannot act on protected groups/hosts.
