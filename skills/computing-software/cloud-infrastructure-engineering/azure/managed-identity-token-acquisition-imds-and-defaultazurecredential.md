---
id: computing-software.cloud-infrastructure-engineering.azure.managed-identity-token-acquisition-imds-and-defaultazurecredential
name: managed-identity-token-acquisition-imds-and-defaultazurecredential
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-identity, imds, defaultazurecredential, token-acquisition, azure-identity]
level: practitioner
status: docs-checked
description: "Acquire tokens with a managed identity: raw IMDS and App Service endpoints, DefaultAzureCredential and ManagedIdentityCredential in SDKs, resource values and caching."
sources: ["https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/how-to-use-vm-token", "https://learn.microsoft.com/azure/app-service/overview-managed-identity#connect-to-azure-services-in-app-code", "https://learn.microsoft.com/dotnet/azure/sdk/authentication/credential-chains", "https://learn.microsoft.com/python/api/overview/azure/identity-readme"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Acquire tokens via IMDS and DefaultAzureCredential

**Goal:** application code gets Entra tokens from its managed identity with no secrets, the same code works on a laptop,
and token calls don't become a bottleneck.

## Raw endpoints (debugging, scripts)
VM / VMSS (Instance Metadata Service at link-local 169.254.169.254):
```bash
curl -s -H Metadata:true --noproxy "*" \
 "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://vault.azure.net" | jq -r .access_token
```
For a user-assigned identity add `client_id`, `object_id` or `msi_res_id`; one of them is required when the VM has
several user-assigned identities. The response carries `expires_in` and `expires_on`.

App Service / Functions (environment variables `IDENTITY_ENDPOINT` and `IDENTITY_HEADER`):
```bash
curl -s "$IDENTITY_ENDPOINT?resource=https://vault.azure.net&api-version=2019-08-01" -H "X-IDENTITY-HEADER: $IDENTITY_HEADER"
```
`client_id` selects a user-assigned identity here too. An app can have several user-assigned identities, and one identity
can be assigned to several resources.

## Resource values
The `resource` (v1) is the audience of the target service: ARM is `https://management.azure.com/` and Key Vault is
`https://vault.azure.net`. For other services take the value from that service's managed-identity documentation. SDKs
take a scope instead (resource plus `/.default`).

## SDK (preferred)
```python
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
cred = ManagedIdentityCredential(client_id=os.environ.get("AZURE_CLIENT_ID"))  # prod: explicit
# cred = DefaultAzureCredential()  # same code in dev and prod
from azure.keyvault.secrets import SecretClient
SecretClient("https://kv-orders-prd.vault.azure.net", cred).get_secret("db-password")
```
.NET: `ManagedIdentityId.FromUserAssignedClientId("<client-id>")` selects a user-assigned identity.
In .NET, set the `AZURE_TOKEN_CREDENTIALS` environment variable to `prod` (or `dev`) to exclude developer-tool (or
deployed-service) credentials from the `DefaultAzureCredential` chain; the sequential probing of many credentials adds
performance overhead. A single credential name as the value needs Azure.Identity 1.15.0 or later.

## Caching
- Azure SDK credentials cache tokens in memory by default: create the credential and client once and reuse them.
- Raw callers should cache a token until `expires_on` rather than calling per request.
- Back-end managed-identity services cache tokens per resource URI for around 24 hours, so role or group changes can
  take that long to show up, and a token can't be forced to refresh early.

## Gotchas
- Calls to 169.254.169.254 must not go through an HTTP proxy.
- AKS pods: use workload identity rather than node-level IMDS.

## Verify
- [ ] Raw curl returns a JWT; decode `oid`/`appid` and confirm it's the expected identity.
- [ ] App logs show token acquisition once per token lifetime, not per request.

## Checked
2026-10-27. Confirmed against Learn "Use a VM managed identity to acquire an access token", App Service "Connect to
Azure services in app code", .NET "Credential chains" and the azure-identity Python readme. Removed: IMDS throttling
figures (20 req/s, 5 concurrent), Arc challenge-file flow, SDK "refresh 5 minutes before expiry", the full
resource table (only ARM and Key Vault retained), the DefaultAzureCredential chain order, and the exact error text for
multiple identities.
Method: documentation only; no commands were run.
