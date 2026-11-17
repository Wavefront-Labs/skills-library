---
id: computing-software.cloud-infrastructure-engineering.azure.app-registrations-and-service-principals
name: app-registrations-and-service-principals
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, app-registration, app-registrations, service-principal, service-principals, enterprise-applications, client-credentials, app-roles, api-permissions, admin-consent, delegated-permissions, application-permissions, client-secret-rotation, federated-credentials, single-tenant, multi-tenant, redirect-uris, app-governance, owners, app-instance-property-lock]
level: practitioner
status: docs-checked
description: "Create and govern Entra app registrations and service principals: tenancy, app roles, API permissions and admin consent, credential lifecycle, owners, stale apps."
sources: ["https://learn.microsoft.com/en-us/entra/identity-platform/app-objects-and-service-principals", "https://learn.microsoft.com/en-us/entra/identity-platform/howto-add-app-roles-in-apps", "https://learn.microsoft.com/en-us/entra/identity-platform/howto-configure-app-instance-property-locks", "https://learn.microsoft.com/en-us/entra/identity-platform/how-to-add-credentials", "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/configure-user-consent", "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/restore-application"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App registrations and service principals — identities for code, governed

**Goal:** every non-human identity has an owner, a least-privilege permission set, a
credential that expires, and an audit trail.

## 1. Objects
- **Application** (app registration) — the global definition; lives in the home tenant.
- **Service principal** (enterprise application) — the instance in *each* tenant that
  holds role assignments, consent and sign-in logs. Single-tenant apps get one SP; multi-tenant
  apps get an SP per consenting tenant.
- Prefer **managed identities** for anything running in Azure; use app registrations only
  for external code, multi-tenant apps, or when you need app roles/API exposure.

```bash
az ad app create --display-name billing-worker --sign-in-audience AzureADMyOrg
az ad sp create --id <appId>
# Secret (avoid): az ad app credential reset --id <appId> --years 1 --display-name ci-2026
# Better: certificate or federated credential (see workload identity federation skill)
az ad app federated-credential create --id <appId> --parameters fc.json
```

## 2. Permissions model
- **Delegated** permissions act *as a user* (needs user sign-in); **Application** permissions
  act as the app (client credentials). `Mail.Read` delegated vs application are very different
  blast radii.
- Request only what is needed; prefer the narrowest Graph permission that covers the call.
- **Admin consent**: application permissions always require it. Set the tenant's user
  consent to the built-in policy `microsoft-user-default-low` (verified publishers, permissions you
  classify as low impact) or disable user consent and route via **admin consent requests**.
- Expose your own API: delegated scopes and `App roles`. App roles and exposed scopes share a
  default limit of 700 permission definitions per application or service principal.
- Assign users, groups or app roles to the enterprise application to control who gets which role.

## 3. Credentials
- Certificates over secrets (Microsoft's recommended credential type); a client secret lifetime is
  at most 24 months, so choose shorter. Store in Key Vault; rotate with overlap (add new, swap,
  delete old). The secret Value is shown once, on creation.
- **App instance property lock** (enabled by default for new apps since June 2026): stops a consuming tenant adding
  credentials to a multi-tenant app's SP.
- Find expiring secrets by listing applications with their `passwordCredentials` and `keyCredentials`
  from Graph and alerting ahead of `endDateTime`.

## 4. Governance
- Keep at least two owners per app (team policy).
- Stale and over-privileged apps: review sign-in activity and granted permissions on a schedule
  and delete or trim after owner confirmation.
- Lifecycle: disable the SP before deleting; a soft-deleted enterprise application can be
  restored from the recycle bin within 30 days, then it is permanently deleted.
- Review redirect URIs regularly; keep them specific and out of production if they point at localhost.

## Gotchas
- Deleting the app registration deletes the SP everywhere; deleting an SP in a consuming tenant removes its role assignments there only.
- Secret value is shown once; the *secret ID* is not the secret.
- Role assignments to an SP use the SP object ID, not the app (client) ID — pass the object ID with `--assignee-object-id` and `--assignee-principal-type ServicePrincipal` when scripting.

## Verify
- [ ] No app registration has fewer than two owners.
- [ ] Every app permission shows *Granted for <tenant>* with a documented justification.
- [ ] No secret outlives your policy (never over 24 months); an alert fires for a test secret nearing expiry.
- [ ] Sign-in log for the SP shows the expected resource and no interactive entries.

## Checked
2026-10-28. Confirmed on Microsoft Learn: application vs service principal roles (app objects page), 700 permission-definition limit shared by app roles and scopes (add app roles page), property lock default since June 2026 (property locks page), 24-month client secret maximum, certificate recommended and secret Value shown once (add credentials page), `microsoft-user-default-low` consent policy (configure user consent page), 30-day soft-delete restore (restore application page). `az ad app`, `az ad sp` and `az role assignment` flags passed check_commands. Removed: stale-days thresholds, Recommendations/app governance claims, sign-in log table names, policy cmdlet name, redirect URI rules, specific Graph permission examples.
Method: documentation only; no commands were run.
