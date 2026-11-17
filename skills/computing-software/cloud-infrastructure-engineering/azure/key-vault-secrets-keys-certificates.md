---
id: computing-software.cloud-infrastructure-engineering.azure.key-vault-secrets-keys-certificates
name: key-vault-secrets-keys-certificates
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, key-vault, keyvault, key-vault-secrets, key-vault-keys, key-vault-certificates, rbac-permission-model, access-policies, soft-delete, purge-protection, key-rotation, certificate-rotation, auto-rotation, key-vault-references, private-endpoint, key-vault-firewall, secrets-management, tls-certificates, managed-certificate, event-grid-near-expiry, premium-hsm]
level: practitioner
status: docs-checked
description: "Run Key Vault: RBAC model, soft-delete + purge protection, private endpoint, key auto-rotation, certificate auto-renewal, Key Vault references and near-expiry alerts."
sources: ["https://learn.microsoft.com/azure/key-vault/general/soft-delete-overview", "https://learn.microsoft.com/azure/key-vault/general/service-limits", "https://learn.microsoft.com/azure/key-vault/general/network-security", "https://learn.microsoft.com/azure/key-vault/keys/how-to-configure-key-rotation", "https://learn.microsoft.com/azure/key-vault/certificates/about-certificates", "https://learn.microsoft.com/azure/key-vault/general/event-grid-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key Vault — secrets, keys and certificates that rotate themselves

**Goal:** one vault per app per environment, RBAC not access policies, nothing reachable
from the internet, and every object with an expiry you get told about.

## 1. Create it right the first time
```bash
az keyvault create -n kv-app-prod -g rg-app-prod -l uksouth \
  --enable-rbac-authorization true --enable-purge-protection true \
  --retention-days 90 --public-network-access Disabled --sku standard
```
- **RBAC permission model** (`--enable-rbac-authorization`) — data-plane roles:
  *Key Vault Secrets User* (read), *Secrets Officer*, *Crypto User*, *Certificates Officer*,
  *Key Vault Administrator*. Assign at vault or even per-secret scope. Legacy *access
  policies* are all-or-nothing per principal and unmanageable at scale.
- **Soft delete** keeps deleted objects recoverable for 7 to 90 days (default 90), set at vault
  creation and not changeable later; **purge protection** blocks permanent deletion for that
  period — required for CMK scenarios.
- Networking: private endpoint plus the matching private DNS zone; keep
  *Allow trusted Microsoft services* on if ARM deployments / App Service / Disk Encryption
  need it (see the network-security page).
- Vault per application and environment; the per-vault throttling limits (service-limits
  page) and blast radius both argue against a shared "company vault".

## 2. Secrets
- Set `--expires` on every secret (`az keyvault secret set --expires 2027-01-01T00:00:00Z`);
  secrets don't auto-rotate — your rotation function/pipeline does, triggered by the
  **Event Grid** secret near-expiry event (fires 30 days before expiry). Template: Microsoft's
  *rotation tutorial* with a Function that creates the new credential and sets a new version.
- Consumers read by **unversioned URI** so rotation needs no redeploy:
  App Service / Functions app setting
  `@Microsoft.KeyVault(VaultName=kv-app-prod;SecretName=db-password)` — the app's managed
  identity needs *Secrets User*.
- Use the content type field for hints and tags for owner/rotation.

## 3. Keys
- Types: RSA, EC, and HSM-backed (`RSA-HSM`, Premium SKU; Managed HSM for a single-tenant
  FIPS 140-3 Level 3 HSM — see customer-managed-keys skill).
- **Auto-rotation policy**: `az keyvault key rotation-policy update -n cmk --vault-name kv-app-prod --value policy.json`
  with `"lifetimeActions":[{"trigger":{"timeBeforeExpiry":"P30D"},"action":{"type":"Rotate"}}]`
  and `"expiryTime":"P2Y"`. Services using versionless key URIs (Storage, Disk Encryption Sets with auto-key-rotation) pick up the new version.
- To create a key with a release policy, `--exportable` must be true and the caller needs the `export` permission.

## 4. Certificates
- `az keyvault certificate create -n tls-www --vault-name kv-app-prod -p "$(az keyvault certificate get-default-policy)"`
  — edit the policy: subject/SANs, validity, **issuer** (self-signed, integrated DigiCert/GlobalSign, or a non-integrated CA via manual CSR), lifetime action auto-renew or email contacts.
- Integrated issuers renew automatically; for others, the vault generates the CSR
  (`az keyvault certificate pending show`) and you merge the signed cert (`certificate pending merge`).
- Consumers: App Service, Application Gateway v2 (user-assigned identity) and AKS (Secrets
  Store CSI driver) read vault certificates; check each service's docs for renewal sync timing and the identity roles it needs.
- Managed certificates (App Service free cert, Front Door managed) are simpler when the
  service supports them — no vault needed.

## 5. Observe
- Diagnostic setting → audit logs to Log Analytics. Alert on 403 spikes and on secret reads
  from unexpected identities.
- Expiry: Event Grid system topic on the vault → secret near-expiry events → Logic App/Teams. Belt-and-braces: Azure Policy
  built-ins *Key Vault secrets should have an expiration date* / *... within the specified number of days*.
- `az keyvault secret backup` exports a secret for restore into another vault; check the CLI page for restore limits.

## Gotchas
- RBAC assignments can take time to apply on the data plane; "Forbidden" right after assignment is normal.
- With public access disabled, `az keyvault secret show` from your laptop fails — use a jump box, Bastion, or temporary firewall rule, not "enable public access".
- Purge protection + a failed IaC run leaves a soft-deleted vault holding the name; `az keyvault recover` instead of fighting it.
- Versioned references in app settings silently pin to the old secret after rotation.
- Certificate `AutoRenew` needs the issuer credentials to stay valid; the email-contacts action goes to vault *Certificate contacts*, which nobody set.

## Verify
- [ ] `az keyvault show` → `enableRbacAuthorization: true`, `enablePurgeProtection: true`, `publicNetworkAccess: Disabled`.
- [ ] Policy compliance shows 100 % for secrets/keys/certs with expiry.
- [ ] Rotating a test secret updates the app within one restart without redeploy.
- [ ] A near-expiry event reaches the on-call channel for a test secret set to expire within the event window.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: Key Vault soft-delete overview (7 to 90 day retention, default 90, purge protection), service limits (per-vault throttling), Event Grid overview (secret near-expiry 30 days before), certificate issuers (DigiCert, GlobalSign, self-signed), key rotation and exportable/release-policy wording, and the az keyvault CLI pages.

Removed because not confirmed: the 10-minute RBAC lag, the 24-hour reference refresh, privatelink zone name, enabledForTemplateDeployment, event type names, log field names, AutoRenew percentage, certificate consumer sync times, content-type examples, FIPS 140-2 L2 wording (Premium and Managed HSM are described as FIPS 140-3 Level 3 validated), and the secret backup scope claim.

Method: documentation only; no commands were run.
