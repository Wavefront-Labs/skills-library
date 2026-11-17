---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.plan-of-action-and-implementing-the-fix
name: plan-of-action-and-implementing-the-fix
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, troubleshooting, plan-of-action, implement-solution, rollback-plan, change-approval, user-impact, comptia-a-plus, impact-assessment-before-change]
level: practitioner
status: draft
description: "CompTIA step 4: plan the fix with impact, rollback and approval in mind, schedule it with the user, follow vendor instructions, and implement or escalate per policy."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# plan-of-action-and-implementing-the-fix

Goal: once the cause is known, apply the fix safely — with the user's
agreement, a way back, and the right approvals (A+ 220-1201 5.1 step 4:
establish a plan of action to resolve the problem and implement the
solution; refer to vendor instructions for guidance).

## Plan
1. **Options**: workaround vs permanent fix; least invasive first (setting
   change before reinstall before reimage).
2. **Impact**: downtime for the user, data at risk, other users affected
   (shared machines, servers).
3. **Rollback**: how to undo — restore point, export registry key
   (`reg export`), previous driver kept, config backup, snapshot.
4. **Approvals/policy**: does it need a change record (server, shared
   service, many users)? Within your role's permissions? Security exception?
5. **Vendor guidance**: follow the vendor's documented procedure and
   firmware/driver versions; unsupported fixes void support.
6. **Schedule** with the user — "This needs a 20-minute restart; now or
   12:30?" Save work first.

## Implement
- Communicate start; perform steps as planned; record each in work notes
  (exact commands/settings).
- If a step fails unexpectedly, stop and reassess rather than improvising
  on a production system.
- Escalate when the fix needs access or authority you don't have.

## Examples of scale
| Fix | Needs |
|---|---|
| Clear Teams cache for one user | user agreement |
| Driver rollback on one laptop | restore point, user time |
| Change a GPO/Intune profile for a group | change record, pilot group |
| Firmware update on a fleet model | change, ring rollout, vendor notes |

## Gotchas
- Fixes applied "while I'm here" without the user knowing cause new
  tickets.
- Fleet-wide fixes from a single-ticket diagnosis need a pilot first.

## Verify
The ticket shows the plan (including rollback), approvals where required,
and steps as executed — then move to verification (step 5).
