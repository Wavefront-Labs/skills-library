---
id: computing-software.cloud-infrastructure-engineering.azure.key-vault-references-in-app-service-functions-and-container-apps
name: key-vault-references-in-app-service-functions-and-container-apps
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, key-vault, key-vault-reference, kv-reference, app-service, container-apps, azure-functions]
level: practitioner
status: docs-checked
description: "Use Key Vault references for app settings in App Service/Functions and secret references in Container Apps: syntax, identity, networking, rotation refresh and diagnostics."
sources: ["https://learn.microsoft.com/en-us/azure/app-service/app-service-key-vault-references", "https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets", "https://learn.microsoft.com/en-us/azure/azure-functions/manage-connections", "https://learn.microsoft.com/en-us/cli/azure/containerapp"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key Vault references

**Goal:** apps read secrets as normal environment variables while the values live (and rotate) in Key Vault.

## App Service / Functions
App setting value:
```
@Microsoft.KeyVault(SecretUri=https://kv-orders.vault.azure.net/secrets/DbPassword/)
@Microsoft.KeyVault(VaultName=kv-orders;SecretName=DbPassword)
```
- **Versionless** URIs are re-fetched automatically (within 24 hours) and on restart / config change; a version in
  the URI pins it.
- Identity: system-assigned by default; for user-assigned set `keyVaultReferenceIdentity`:
```bash
az webapp update -g rg -n app-orders --set keyVaultReferenceIdentity=<uami-resource-id>
```
- Grant **Key Vault Secrets User** on the vault (RBAC model) to that identity.
- Network-restricted vault: the vault must accept traffic from a virtual network the app uses; apps that reach private endpoints must route all traffic through the virtual network (`vnetRouteAllEnabled`; automatic on Flex Consumption).
- Status: portal > Application settings > Edit on the reference shows resolution status and errors; *Diagnose and solve
  problems* > "Key Vault Application Settings Diagnostics" (App Service: Availability and Performance > Web app down).
- Any configuration change restarts the app and refetches all references immediately; the platform otherwise refetches every 24 hours.

## Container Apps
```bash
az containerapp secret set -g rg -n ca-orders \
  --secrets "db-password=keyvaultref:https://kv-orders.vault.azure.net/secrets/DbPassword,identityref:<uami-resource-id>"
az containerapp update -g rg -n ca-orders --set-env-vars "DB_PASSWORD=secretref:db-password"
```
In ARM, a secret with `keyVaultUrl` takes `"identity": "system"` for the system-assigned identity or the resource ID of a user-assigned identity. A reference without a version uses the latest version and picks up new versions within 30 minutes; active revisions that reference the secret in an environment variable are restarted automatically to pick up the new value. Pin a version in the URI for full control.

## Gotchas
- `WEBSITE_CONTENTAZUREFILECONNECTIONSTRING` can use a reference, but App Service validates the content share when the setting changes and the validation fails for a reference; set `WEBSITE_SKIP_CONTENTSHARE_VALIDATION=1` and create the content share beforehand (an invalid connection string or share then causes HTTP 500 errors).
- Mark most Key Vault reference settings as slot settings so each slot keeps its own.
- A reference that does not resolve is passed to the app as the literal `@Microsoft.KeyVault(...)` string - apps then fail auth in odd ways.
- Prefer identity-based connections over secrets entirely when the target service supports Entra auth.

## Verify
- [ ] All references show resolved status; rotate a secret and confirm the app picks it up within the expected window.

## Checked
Checked 2026-10-24 against azure-docs app-service-key-vault-references and container-apps manage-secrets, plus the azure-docs-cli containerapp reference (--secrets, --set-env-vars exist; secretref: prefix documented). Confirmed: SecretUri and VaultName/SecretName reference forms, 24 hour refetch and restart-on-config-change, keyVaultReferenceIdentity via az webapp update, Key Vault Secrets User role, vnetRouteAllEnabled requirement, diagnostic detector name, literal string left when unresolved, Container Apps keyvaultref and identityref syntax and 30 minute versionless refresh. Found wrong and fixed: Container Apps running revisions restart automatically on a new secret version (no new revision needed); the content-share setting can be a reference with WEBSITE_SKIP_CONTENTSHARE_VALIDATION. Removed unconfirmed: identityref:system in the CLI form, the slot-identity statement.

Method: documentation only; no commands were run.
