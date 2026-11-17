---
id: computing-software.it-support-helpdesk.servicenow.request-fulfilment-req-ritm-sctask
name: request-fulfilment-req-ritm-sctask
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-request, request-fulfilment, req, ritm, sctask, catalog-task, flow-designer, fulfilment-workflow, stages]
level: practitioner
status: gated
description: "Work and design ServiceNow request fulfilment: REQ vs RITM vs SCTASK, stages, sequencing tasks in Flow Designer, when to close what, and fixing stuck requests."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://developer.servicenow.com/dev.do"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# request-fulfilment-req-ritm-sctask

Goal: requests move through approval and fulfilment without sitting
invisible in someone's queue.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## The three records
- **REQ (sc_request)** — the order/cart; one per submission; holds overall
  approval state. Users see this number.
- **RITM (sc_req_item)** — one per item in the cart; holds the variables,
  stage and the flow/workflow context. This is what the request is "about".
- **SCTASK (sc_task)** — work assigned to fulfilment groups (create account,
  ship laptop, install software). Agents work these.
Closing all SCTASKs typically lets the flow close the RITM, which closes the
REQ.

## Typical flow (Flow Designer)
1. Trigger: Service Catalog (item submitted).
2. **Ask for approval** (manager / data owner; see approvals skill).
3. Approved → **Create catalog task** for group A (wait for completion), then
   group B — sequential where dependent, parallel where not.
4. Update RITM **stage** (Approval → Fulfilment → Delivery → Completed) so
   users see progress in the portal.
5. Automation steps where possible (Integration Hub: create AD account, add
   to group, Intune app assignment).
6. Close RITM with outcome; notify requester.

## Agent practice
- Work the SCTASK, put fulfilment notes there; customer-visible updates go
  on the RITM (the user sees RITM comments).
- Don't close an SCTASK as complete when it was actually cancelled —
  use Closed Incomplete/Skipped so the flow branches correctly.
- Missing information: ask on the RITM, set SCTASK pending with a reason.

## Stuck requests
- RITM in fulfilment with no open SCTASKs → flow errored or waiting; open
  the **Flow execution** (Flow Designer → Executions) or workflow context,
  read the error, fix and restart/re-trigger per admin process.
- Approval pending for weeks → approver left/absent: reassign approval
  (delegate) per policy.
- Reports: RITMs open > N days by stage, SCTASKs unassigned.

## Gotchas
- Editing variables after submission doesn't re-run earlier flow logic.
- Cancelling the REQ doesn't always cancel open SCTASKs — check the flow
  handles cancellation.

## Verify
Sample request: stages visible to user, every SCTASK has an owner, RITM and
REQ closed automatically when tasks complete, end-to-end time matches the
item's promised delivery time.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, developer.servicenow.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
