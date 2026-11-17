---
id: computing-software.it-support-helpdesk.servicenow.request-approvals-and-delegation
name: request-approvals-and-delegation
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-request, request-approvals, approval-rules, delegation, sysapproval-approver, email-approval, separation-of-duties, data-owner-approval]
level: practitioner
status: draft
description: "Set up and support request approvals: manager vs data-owner vs group approvals, approve-by-email and mobile, delegates during absence, reminders, and audit evidence."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://support.atlassian.com/jira-service-management-cloud/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# request-approvals-and-delegation

Goal: the right person approves quickly, the record proves it, and absences
don't stall requests.

## Who should approve
| Request | Approver |
|---|---|
| Cost (hardware, licences) | line manager / budget holder |
| Data access (shares, mailboxes, apps) | **data/resource owner** (not just manager) |
| Privileged access | owner + security; time-bound |
| Standard pre-approved items (mouse, standard software) | none — pre-approved by policy |
Avoid approval chains longer than needed; every extra approver adds days.
Separation of duties: requester can't approve their own request (ServiceNow
blocks self-approval only if configured).

## Mechanics (ServiceNow)
- Flow Designer **Ask for approval** action: approvers by user, group (any
  one / all / % of group), manager of requested-for, or reference to a field
  (e.g. owner on the CI/business application record).
- Approvals live in **sysapproval_approver**; approvers act in the portal
  ("My approvals"), mobile app, Agent Workspace, or **approve by email**
  (reply with "approve"/"reject" — requires the inbound email action).
- Reminders: scheduled flow to remind after N days; escalate to approver's
  manager after N more.

## Delegation
Users set **delegates** (portal profile → Delegates / `sys_user_delegate`)
with start/end dates and "Approvals" ticked — delegate receives and can act
on approvals during absence. Service desk can set it on request for
someone on sudden leave (with manager approval).

## Supporting "where's my request?"
1. Open the RITM → Approvers related list: who, state, when requested.
2. Approver gone/left: reassign via approval record (admin/approval_admin)
   per policy, note reason.
3. Rejected: comment carries the reason; requester can resubmit with
   changes.

## Audit
Approval record holds approver, timestamp, comments — this is the evidence
auditors sample for access requests. Email approvals must be traceable to
the approver's authenticated mailbox.

## Gotchas
- Group approvals where "anyone" approves can let the requester's teammate
  rubber-stamp — choose owners deliberately.
- Approvals by chat/verbal "yes" must be recorded on the request by the
  approver, not pasted by an agent.

## Verify
Sample access requests: each has the correct owner approval recorded before
fulfilment started; median approval time within target.
