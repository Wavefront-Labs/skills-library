---
id: computing-software.cybersecurity-defensive.identity-access-management.guest-access-governance
name: guest-access-governance
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [entra-id, guest-access-governance, b2b-collaboration, external-identities, access-reviews, cross-tenant-access, entitlement-management]
level: practitioner
status: docs-checked
description: "Govern guest and B2B access in Entra ID: invitation restrictions, cross-tenant access settings, guest permissions, MFA trust, access packages, reviews and stale guest cleanup."
sources: ["https://learn.microsoft.com/en-us/entra/external-id/external-collaboration-settings-configure", "https://learn.microsoft.com/en-us/entra/external-id/cross-tenant-access-overview", "https://learn.microsoft.com/en-us/entra/id-governance/manage-guest-access-with-access-reviews"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Guest and B2B access governance

**Goal:** external collaborators get the access they need for as long as they need it,
with MFA, and guests do not accumulate into thousands of forgotten accounts with access to
Teams, SharePoint and apps.

## External collaboration settings (Entra > External Identities)
- **Guest user access:** "Guest users have limited access to properties and memberships of
  directory objects" or the most restrictive option (cannot enumerate the directory).
- **Guest invite settings:** only users in specific admin roles or a designated inviter group
  can invite, or route invitations through entitlement management.
- **Collaboration restrictions:** allowlist or blocklist of partner domains.
- Email one-time passcode for guests without an Entra/Microsoft account.

## Cross-tenant access settings
Default and per-organisation inbound/outbound rules: which users/groups and apps B2B
collaboration covers; **trust settings** to accept partner MFA and compliant device claims
(so guests are not prompted twice), only for partners you trust. B2B direct connect for Teams
shared channels configured separately.

## Conditional access for guests
Policy targeting "Guest or external users": require MFA, block access to admin portals,
session controls (no downloads on unmanaged devices) for sensitive sites.

## Lifecycle
- **Entitlement management access packages** for partner access: catalogue resources
  (groups, Teams, SharePoint sites, apps), connected organisations, requests with sponsor
  approval, assignment expiry, automatic removal of the guest account when
  its last assignment ends.
- **Access reviews** for all guests quarterly: reviewers are sponsors or resource owners;
  block sign-in then remove from the tenant after denial.
- Inactive guests: find them with sign-in activity data and block, then remove, after a period you set
  (access reviews can block denied guests for 30 days, then remove them).
```powershell
Get-MgUser -Filter "userType eq 'Guest'" -All -Property displayName,mail,createdDateTime
```

## Gotchas
- SharePoint/OneDrive external sharing settings are separate; align them (existing guests
  only vs anyone links).
- Guests added to Microsoft 365 groups inherit everything the group can reach.
- Guest accounts from consumer domains (gmail.com) via OTP are harder to attribute; require
  sponsors.

## Verify
Guest count trends with business activity rather than climbing forever; every guest has a
sponsor or access package; a test guest from a blocked domain cannot be invited; guests are
prompted for MFA or trusted partner MFA is shown in sign-in logs.

## Checked

2026-10-28. Confirmed against the external collaboration settings, cross-tenant access overview and guest access review pages: guest access levels (limited by default, most restrictive option), invite restrictions, email one-time passcode fallback, trust settings (inbound MFA and device claims), B2B direct connect, 30-day block then remove for denied guests. Removed: signInActivity property, 90-day inactivity and 90-180 day assignment expiry figures, deny-on-no-response claim.

Method: documentation only; no commands were run.
