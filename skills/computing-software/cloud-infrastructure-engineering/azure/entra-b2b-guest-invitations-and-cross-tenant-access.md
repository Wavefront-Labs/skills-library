---
id: computing-software.cloud-infrastructure-engineering.azure.entra-b2b-guest-invitations-and-cross-tenant-access
name: entra-b2b-guest-invitations-and-cross-tenant-access
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, entra-id, guest-invitations, cross-tenant-access, b2b-collaboration, external-identities]
level: practitioner
status: draft
description: "Invite external guests with Entra B2B, set external collaboration restrictions, and configure cross-tenant access inbound/outbound and trust settings."
sources: ["https://learn.microsoft.com/en-us/entra/external-id/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Entra B2B guests and cross-tenant access

**Goal:** let named outside users into your tenant with controlled scope, and control which external tenants can collaborate.

## Invite a guest
- Portal: Users > New user > Invite external user. Graph: `POST /invitations` with `invitedUserEmailAddress`, `inviteRedirectUrl`, `sendInvitationMessage`.
```powershell
New-MgInvitation -InvitedUserEmailAddress guest@partner.example -InviteRedirectUrl "https://myapps.microsoft.com" -SendInvitationMessage:$true
```
- The guest appears as user type **Guest** and redeems the invitation at first sign-in. Give access via group membership (dynamic groups on `userType`) and app/role assignments, never directly to many resources.

## Who can invite (External collaboration settings)
External Identities > External collaboration settings > Guest invite settings: anyone including guests; member users and specific roles; admins and Guest Inviters only; no one. Also set guest user access restrictions (default: limited access to directory objects) and collaboration restrictions (allow/deny domain list).

## Cross-tenant access settings
External Identities > Cross-tenant access settings:
- **Default settings** apply to every external tenant; **Organizational settings** override per tenant (add by tenant ID or domain).
- Each has **Inbound** (their users into your tenant) and **Outbound** (your users to theirs), for B2B collaboration and B2B direct connect.
- **Trust settings**: accept their MFA, compliant-device and hybrid-joined-device claims so guests are not prompted twice; Conditional Access can then require MFA for guests.
- Start restrictive: block by default, allow specific partner tenants.

## Gotchas
- Trusting external MFA is a per-partner decision; do not enable it by default.
- Guest lifecycle: use access reviews and entitlement management to expire guests.
- Invitation redemption fails if the user signs in with a different identity than invited.

## Verify
Sign-in logs show cross-tenant sign-ins with the home tenant ID; the guest sees only the assigned apps.
