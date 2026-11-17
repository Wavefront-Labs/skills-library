---
id: computing-software.cloud-infrastructure-engineering.azure.managed-identity-limits-cross-tenant-and-subscription-moves
name: managed-identity-limits-cross-tenant-and-subscription-moves
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, managed-identity, cross-tenant, federated-identity-credential, token-cache, subscription-move, mi-limits, mi-cross-tenant, mi-subscription-move]
level: practitioner
status: docs-checked
description: "Know what breaks managed identities: tenant transfers, resource moves, token caching limits, directory quota, and reaching another tenant via an app trusting a managed identity."
sources: ["https://learn.microsoft.com/entra/identity/managed-identities-azure-resources/managed-identities-faq", "https://learn.microsoft.com/entra/workload-id/workload-identity-federation-config-app-trust-managed-identity"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Managed identity limits, cross-tenant use and moves

**Goal:** plan migrations and multi-tenant designs knowing exactly where managed identities stop working.

## Moving things
| Action | Effect on managed identities |
|---|---|
| Move a **user-assigned** identity to another resource group or subscription | Not supported: create a new user-assigned identity there and grant it the permissions |
| Move a subscription to **another directory (tenant)** | Identities are not recreated automatically: re-create them manually and grant Azure role assignments again |
| Role assignments scoped to the old subscription or RG | Re-grant at the new scope after any move that changes scope |

Before a tenant move, export role assignments (`az role assignment list --all`) and identity usages so you can
rebuild. Deleted principals leave orphaned role assignments that show as unknown principals: clean them up.

## Caching limits
- Back-end services keep a token cache per resource URI for around 24 hours. Permission changes (including role
  removal) can take several hours to take effect, and a token cannot be forced to refresh before it expires.
  Design for this delay rather than expecting immediate revocation.
- Each managed identity has a service principal that counts toward the tenant's directory object quota; creation is
  blocked when it would push total directory usage to 98% or more of the quota.

## Cross-tenant access
The FAQ states managed identities do not directly support cross-directory access. The documented workaround is an
Entra app that trusts the managed identity:
1. Create an app registration that is **multitenant** and provision it into the other tenant.
2. Add a federated identity credential on that app: issuer `https://login.microsoftonline.com/<tenant-id>/v2.0`,
   subject = the managed identity's object (principal) ID (case-sensitive GUID), audience `api://AzureADTokenExchange`
   (US Government and China clouds use `...USGov` and `...China` variants). The app and the managed identity must be in
   the same tenant; wrong values are not rejected until the token exchange fails.
3. Grant the app's service principal access to the target resource.
4. In code get a token for that audience from the managed identity and use it as the client assertion for the app
   (for example .NET `ClientAssertionCredential`). No secrets are stored.

## Other limits
- Managed identities have no application object, so Microsoft Graph permissions are granted directly to the
  service principal.
- Some services support only system-assigned or only one user-assigned identity per feature - check per service.

## Verify
- [ ] Migration runbook includes identity re-creation and role re-grant steps; cross-tenant call works with no client secret.

## Checked
2026-10-27. Confirmed against Learn "Managed identities FAQ" and "Configure an app to trust a managed identity".
Fixed: the skill said same-tenant moves keep identities working (the FAQ says moving a user-assigned identity is not
supported), said a managed identity can only get tokens from its home tenant without noting the FAQ wording, and
described the token-cache limit as covering group changes. Removed: system-assigned disable/re-enable advice, the
4,000 role assignments per subscription figure, the PIM and Arc statements, and the unverified "one identity per
feature" specifics (kept as a pointer to per-service docs).
Method: documentation only; no commands were run.
