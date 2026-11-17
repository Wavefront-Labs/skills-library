---
id: computing-software.it-support-helpdesk.desktop-support.group-membership-and-access-requests
name: group-membership-and-access-requests
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, identity-support, group-membership, access-request, security-groups, add-adgroupmember, dynamic-groups, access-packages, kerberos-token, klist-purge, least-privilege]
level: practitioner
status: draft
description: "Process access requests through security groups: approval, AD vs Entra vs dynamic groups, mirroring risks, token refresh so access applies, and removing access on role change."
sources:
  - "https://learn.microsoft.com/en-us/powershell/module/activedirectory/add-adgroupmember"
  - "https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-membership"
  - "https://learn.microsoft.com/en-us/entra/id-governance/entitlement-management-access-package-create"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# group-membership-and-access-requests

Goal: access is granted through groups, approved by the data owner, takes
effect the first time, and is easy to remove later.

## Request handling
- Approval from the **resource owner** (not just the user's manager) for
  data access; capture approver in the ticket/RITM.
- Grant to a group, never directly to a folder/app ACL for a person.
- Avoid "same access as Bob" requests — mirroring copies years of
  accumulated access. Ask for the specific resources; if unavoidable, list
  Bob's groups and get each one approved.

## Doing it
```powershell
# on-prem AD
Add-ADGroupMember -Identity "FS-Finance-RW" -Members jdoe
Get-ADPrincipalGroupMembership jdoe | Select Name
# Entra cloud group
Connect-MgGraph -Scopes GroupMember.ReadWrite.All
New-MgGroupMember -GroupId <groupId> -DirectoryObjectId <userId>
```
- Groups synced from AD (Entra Connect) can only be changed in AD.
- **Dynamic groups** (rule on department/jobTitle) can't take manual
  members — fix the user attribute (usually from HR) instead.
- Entitlement management **access packages** let users request and get
  time-bound approved access themselves; route recurring requests there.

## Making it take effect
Group membership is in the logon token:
- File shares (Kerberos): user signs out and in, or `klist purge` then
  re-access; laptops off-network need VPN at sign-in.
- Entra/M365 (SharePoint, Teams): usually minutes, sometimes up to an hour;
  sign out of the browser session.
- Apps doing their own group sync (SaaS SCIM): next provisioning cycle (~40
  min for Entra provisioning).
`whoami /groups` on the client shows what the token actually contains.

## Movers and removal
Role change → remove old role groups at the same time as adding new ones
(mover process). Time-bound requests: set an expiry (access package or
ticket follow-up task).

## Gotchas
- Nested groups across domains/forests may not appear in tokens as
  expected; test.
- Token size bloat (hundreds of groups) causes Kerberos failures
  (`MaxTokenSize`) and HTTP 400 "header too long".

## Verify
`whoami /groups` (or the app) shows the new group after re-logon, the user
opens the resource, and the ticket records approver and group name.
