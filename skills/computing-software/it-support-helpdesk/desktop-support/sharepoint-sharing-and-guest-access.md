---
id: computing-software.it-support-helpdesk.desktop-support.sharepoint-sharing-and-guest-access
name: sharepoint-sharing-and-guest-access
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, sharepoint-sharing-access, guest-access, b2b-collaboration, external-sharing, sharepoint-permissions]
level: practitioner
status: draft
description: "Resolve SharePoint and OneDrive permission and sharing tickets, and B2B guest access problems: sharing levels, access requests, guest invitation and sign-in issues."
sources:
  - "https://learn.microsoft.com/en-us/sharepoint/turn-external-sharing-on-or-off"
  - "https://learn.microsoft.com/en-us/sharepoint/sharepoint-permissions-for-site-owners"
  - "https://learn.microsoft.com/en-us/entra/external-id/troubleshoot"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# sharepoint-sharing-and-guest-access

## SharePoint permissions model
- Sites have **Owners, Members, Visitors** groups (connected to the Microsoft 365 group
  for team sites). Add people via the group, not unique item permissions.
- Sharing links: "People in your organization", "Specific people", "Anyone" (if
  allowed), "People with existing access". Links create limited-access entries.
- Broken inheritance at folder/file level makes troubleshooting hard; check via Site
  settings > Site permissions > "Check Permissions" for the user.
- Access requests: owners get an email; configure who receives them in Site permissions
  > Access request settings.

## Common tickets
| Ticket | Check |
|---|---|
| "Access denied" on a link | Link type (specific people sent to another address?), user signed in with right account |
| Can see but not edit | Visitors group, or link was view-only |
| Owner left the company | Site admin adds a new owner via SharePoint admin center |
| Can't share externally | Tenant and site sharing level (most restrictive wins), domain allow/block lists, sensitivity label |

## External sharing levels
Tenant (SharePoint admin center > Policies > Sharing) sets the maximum: Anyone, New and
existing guests, Existing guests, Only people in organization. Each site can be equal or
more restrictive. OneDrive can't exceed SharePoint's setting.

## B2B guest access
- Guests are invited (sharing, Teams add, or Entra invitation) and redeem with their
  own identity (Entra account, Microsoft account, Google, or email one-time passcode).
- Problems:
  - Invitation never arrived: check spam; resend from Entra > Users (guest) >
    Resend invitation; or share the direct link with redemption.
  - Signs in to their own tenant and sees nothing: tell them to use the link or switch
    organization (Teams org switcher; `https://myapps.microsoft.com/?tenantid=<id>`).
  - Blocked by the resource tenant's **cross-tenant access settings** or Conditional
    Access (MFA required: guest must register MFA in your tenant unless inbound trust
    is configured).
  - Domain blocked in collaboration restrictions.
- Guest lifecycle: access reviews for guests; remove stale guests.

## Verify
The user opens the item with the intended rights (Check Permissions confirms it), and a
guest can redeem and reach the resource from a private browser window.
