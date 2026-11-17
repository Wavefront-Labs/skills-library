---
id: computing-software.cloud-infrastructure-engineering.azure.managed-identity-troubleshooting-401-403-and-token-cache
name: managed-identity-troubleshooting-401-403-and-token-cache
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-identity, troubleshooting, rbac-propagation, token-cache, credentialunavailable]
level: practitioner
status: docs-checked
description: "Troubleshoot managed identity failures: CredentialUnavailable, wrong identity selected, 401 vs 403, RBAC propagation, cached tokens and firewall-vs-permission confusion."
sources: ["https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/managed-identities-faq", "https://learn.microsoft.com/azure/role-based-access-control/troubleshooting", "https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/identity/Azure.Identity/TROUBLESHOOTING.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshoot managed identity 401/403 and token caching

**Goal:** go from "the app gets 403" to the exact cause in minutes.

## Step 1 - classify the error
| Symptom | Layer | Likely cause |
|---|---|---|
| `CredentialUnavailableException` (every credential in the `DefaultAzureCredential` chain failed) | Token acquisition | Identity not enabled, code running off-Azure, IMDS blocked or unreachable |
| IMDS returns 400 | Token acquisition | The requested identity isn't assigned to the VM |
| IMDS returns 502/504 | Token acquisition | Gateway error on the metadata endpoint; retry |
| Several user-assigned identities, no ID given | Token acquisition | `client_id`, `object_id` or `msi_res_id` is required in that case |
| 401 from the service | Token validation | Wrong audience/scope, wrong tenant, expired token |
| 403 from the service | Authorization | Missing data-plane role, wrong scope, management role instead of data role, or a firewall/private-endpoint block (check the service's error text to tell RBAC from network) |

## Step 2 - prove which identity the app is using
Get a token from inside the app environment (Kudu console, `kubectl exec`, VM shell) and decode the payload:
```bash
tok=$(curl -s "$IDENTITY_ENDPOINT?resource=https://vault.azure.net&api-version=2019-08-01" -H "X-IDENTITY-HEADER: $IDENTITY_HEADER" | jq -r .access_token)
echo $tok | cut -d. -f2 | base64 -d 2>/dev/null | jq '{aud, oid, appid, tid}'
```
Compare `oid` with the principal you granted. (`IDENTITY_ENDPOINT` exists on App Service and Functions; on a VM use IMDS.)

## Step 3 - check the role assignment
```bash
az role assignment list --assignee <oid> --all --query "[].{role:roleDefinitionName,scope:scope}" -o table
```
Common misses: a management-plane role such as *Contributor* does not give data access to blobs or secrets; the
assignment is at a different resource; Key Vault is still in access-policy mode.

## Step 4 - propagation and caches
- Role assignment changes (adding or removing) can take up to 10 minutes to take effect because Azure Resource Manager
  caches. PowerShell's listing of role assignments uses its own cache (about 10 minutes to refresh).
- Back-end managed-identity services cache tokens per resource URI for around 24 hours, so group or role changes can take
  hours to show in a token, and a token can't be forced to refresh early. Restart or wait; SDKs also cache tokens in memory.
- Removal is equally delayed: for incident containment disable the identity or block the network rather than relying
  on role removal.

## Step 5 - SDK diagnostics
.NET: `using AzureEventSourceListener listener = AzureEventSourceListener.CreateConsoleLogger();` prints each credential
attempted and why it failed. Check the Azure.Identity troubleshooting guide for the exception message you see.

## Gotchas
- `DefaultAzureCredential` on a dev box may pick developer or environment credentials instead of the managed identity;
  exclude them or select one credential explicitly when testing.
- Managed identities do not support cross-directory access directly; see the limits skill for the app-trust workaround.

## Verify
- [ ] Decoded token `oid` equals the principal with the role assignment.
- [ ] After the fix, the request succeeds from inside the app environment, not just from your laptop.

## Checked
2026-10-27. Confirmed against the Azure.Identity .NET troubleshooting guide (CredentialUnavailableException, IMDS 400 and
502/504 causes, console event listener), Learn "Troubleshoot Azure RBAC" (10 minute propagation, 24 hour managed
identity cache) and the managed identities FAQ. Removed: exact Storage/Key Vault 403 error strings, "xms_mirid" claim,
the "under 5 minutes" data-plane figure, the Python logging snippet, the Azure SQL 18456 note and the `AZURE_CLIENT_SECRET`
dev-box claim (not found in fetched pages). The Learn managed-identity troubleshooting page cited earlier returns 404.
Method: documentation only; no commands were run.
