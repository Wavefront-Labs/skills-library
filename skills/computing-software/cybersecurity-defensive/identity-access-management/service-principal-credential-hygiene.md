---
id: computing-software.cybersecurity-defensive.identity-access-management.service-principal-credential-hygiene
name: service-principal-credential-hygiene
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [entra-id, service-principal-credentials, app-registrations, client-secrets, managed-identity, app-instance-property-lock, graph-permissions]
level: advanced
status: docs-checked
description: "Control Entra app and service principal credentials: find secrets and certs, prefer managed identities and federation, restrict who adds credentials, detect abuse."
sources: ["https://learn.microsoft.com/en-us/entra/identity-platform/security-best-practices-for-app-registration", "https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/application-management-certs-faq", "https://learn.microsoft.com/en-us/entra/identity-platform/howto-configure-app-instance-property-locks"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Service principal credential hygiene

Attackers who reach Application Administrator, or own an app with powerful Graph permissions, add
their own secret to an existing service principal and get persistent, MFA-free access.

## Inventory
```powershell
Connect-MgGraph -Scopes Application.Read.All
Get-MgApplication -All -Property displayName,appId,passwordCredentials,keyCredentials |
  Select displayName, appId, @{n='Secrets';e={$_.passwordCredentials.Count}},
         @{n='NextExpiry';e={($_.passwordCredentials.endDateTime + $_.keyCredentials.endDateTime | Sort)[0]}}
Get-MgServicePrincipal -All -Property displayName,passwordCredentials,keyCredentials | ? { $_.passwordCredentials -or $_.keyCredentials }
```
Credentials can sit on the **service principal** object as well as on the app registration;
check both.

## Reduce credentials
1. **Managed identities** for Azure-hosted workloads (no secret at all).
2. **Workload identity federation** for GitHub Actions, Kubernetes, other clouds.
3. Certificates over client secrets where a credential is unavoidable; short validity,
   stored in Key Vault with rotation.
4. Remove unused credentials and unused apps (use the service principal sign-in activity reports).

## Restrict who can add credentials
- Owners of an app can add secrets: keep owners minimal (no regular users).
- Limit Application Administrator / Cloud Application Administrator role holders; use PIM.
- **App instance property lock** on multi-tenant apps prevents credentials being added to their
  service principals in customer tenants.

## Prioritise by permission
Apps with broad application permissions (directory write, role management, tenant-wide mail or file access) are Tier 0 equivalents. Review them first.

## Detect
Audit log activities that add service principal credentials or change application certificates and
secrets; alert when the actor is not your automation, or the target app is privileged.
Service principal sign-in logs: look for new IPs/ASNs for an app.

## Gotchas
- Secret expiry outages push teams to very long-lived secrets; give them federation or rotation automation instead.
- Microsoft first-party service principals in your tenant can also hold credentials; investigate
  unexpected ones.

## Verify
Monthly report: number of client secrets trending down, no credentials older than policy, every
privileged app has a named owner and only expected credentials.

## Checked

2026-10-28. Confirmed against the Entra app registration security best practices page (managed identities first, certificate in Key Vault if a credential is needed) and the app instance property lock page. Removed: Midnight Blizzard and SolarWinds attribution, 6-12 month validity, servicePrincipalSignInActivities and AADServicePrincipalSignInLogs names, named high-privilege Graph permission list, app management policy bullet (workload ID premium), audit activity display names, 99-year secret claim, portal visibility claim.

Method: documentation only; no commands were run.
