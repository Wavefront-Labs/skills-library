---
id: computing-software.it-support-helpdesk.remote-support-tools.privileged-identity-management-for-support
name: privileged-identity-management-for-support
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, privileged-identity-management, pim, just-in-time-access, eligible-assignment, entra-roles, least-privilege]
level: practitioner
status: draft
description: "Use Entra Privileged Identity Management as a support engineer: eligible vs active roles, activating with justification, approval and duration, PIM for groups, and audit."
sources:
  - "https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-configure"
  - "https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/pim-how-to-activate-role"
  - "https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# privileged-identity-management-for-support

With PIM (Entra ID P2 / ID Governance), support engineers hold admin roles as **eligible**
and activate them only when needed, for a limited time, with justification. A stolen
engineer account then doesn't hold standing admin rights.

## Concepts
- **Eligible** assignment: you can activate the role. **Active**: you hold it now
  (permanently or time-bound).
- Role settings per role: max activation duration (e.g. 4 h), require MFA on activation,
  require justification, require ticket number, require approval (approver list),
  notification recipients.
- **PIM for Groups**: eligible membership of a group that grants access (e.g. a group
  assigned Intune roles, or local admin on devices via an Intune account protection
  policy), so non-Entra permissions get JIT too.

## Activating (engineer)
1. Entra admin center > Identity governance > Privileged Identity Management > **My roles**
   (or the My Access portal), Eligible assignments.
2. **Activate**: choose duration, enter justification and ticket number, complete MFA.
3. If approval required, wait for an approver (they get email/Teams); else active in
   seconds to a few minutes.
4. Sign out and in (or refresh tokens) in the admin portal so the new role applies; some
   portals cache roles for minutes.
5. **Deactivate** when done rather than waiting for expiry.

## Typical support roles to make eligible (not active)
Helpdesk Administrator (password resets for non-admins), Authentication Administrator
(MFA method reset for non-admins), Intune Administrator / Cloud Device Administrator,
Exchange Recipient Administrator, User Administrator. Global Administrator: emergency only.

## Audit
PIM > Resource audit / My audit: who activated what, when, why, approval. Security
reviews ask for this; keep justifications meaningful ("INC0012345 MFA reset for user X").
Access reviews (PIM > Access reviews) periodically confirm engineers still need eligibility.

## Gotchas
- Activation for 8 hours "to save time" defeats the purpose; ask for the realistic time.
- Approval-required roles need approvers available out of hours, or on-call work stalls.
- Break-glass accounts are excluded from PIM and CA by design; never use them for routine work.

## Verify
Your account shows no active privileged roles outside activations; an activation appears in
the audit log with ticket number; the role ends at expiry or deactivation.
