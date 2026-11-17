---
id: computing-software.it-support-helpdesk.device-provisioning.movers-role-change-access-review
name: movers-role-change-access-review
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, movers, joiners-movers-leavers, access-review, privilege-creep, rbac, entra-id-governance]
level: practitioner
status: draft
description: "Process role changes (movers) without privilege creep: trigger from HR, remove old access as well as adding new, time-boxed overlap, manager attestation and access reviews."
sources:
  - "https://learn.microsoft.com/en-us/entra/id-governance/access-reviews-overview"
  - "https://learn.microsoft.com/en-us/entra/id-governance/what-are-lifecycle-workflows"
  - "https://csrc.nist.gov/projects/role-based-access-control"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# movers-role-change-access-review

## The risk
Movers keep old access and gain new; after a few moves a user can approve their own
payments or see HR data. Auditors look for exactly this.

## Process
1. **Trigger** from HR (department/title/manager change) or an approved request, not
   from a hallway conversation.
2. **Inventory current access**: group memberships, app roles, shared mailboxes,
   SharePoint/Teams owners, privileged roles, distribution lists, file shares, licences.
   `Get-MgUserMemberOf -UserId <upn> -All` gives the Entra side.
3. **New access** from the target role's standard set (role-based groups), not "copy
   from colleague".
4. **Remove old access** that the new role does not need. Agree an overlap period for
   handover (e.g. 30 days) and schedule the removal with an end date.
5. **Attest**: new manager confirms the final access list; record it in the ticket.

## Automate what you can
- Dynamic groups on department/job title move people automatically when HR updates
  attributes.
- Entra ID Governance Lifecycle Workflows have a "mover" template to run tasks on
  attribute change.
- Periodic access reviews (quarterly for privileged/sensitive groups) catch what slipped.

## Gotchas
- Mailbox delegations and calendar permissions are granted per-user and missed by group
  reviews.
- Local admin and app-internal roles (finance system, CRM) need the app owner's action.
- Privileged role eligibility in PIM persists until removed.

## Verify
After the overlap period, the user's memberships match the new role's standard set plus
documented exceptions, and the manager's attestation is on file.
