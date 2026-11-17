---
id: computing-software.it-support-helpdesk.servicenow.cancelling-and-modifying-submitted-requests
name: cancelling-and-modifying-submitted-requests
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, request-cancellation, ritm, sctask, request-fulfilment, service-request, variable-editor]
level: practitioner
status: gated
description: "Cancel or change a submitted ServiceNow request safely: RITM vs REQ cancellation, stopping flows and open SCTASKs, editing variables, and reversing work already done."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/service-catalog-management/concept/c_RequestedItems.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/service-catalog-management/concept/c_ServiceCatalogRequestFulfillment.html"
  - "https://www.servicenow.com/docs/bundle/zurich-build-workflows/page/administer/flow-designer/concept/flows.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# cancelling-and-modifying-submitted-requests

Users change their minds, start dates move, managers order the wrong laptop. The risk is a
cancelled RITM whose flow keeps running and creates accounts or ships kit.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## One item vs the whole request
- **One item**: on the RITM set the state to Closed Incomplete (or your Cancelled stage)
  with a customer-visible reason. Other RITMs carry on.
- **Whole request**: cancel each RITM; the REQ closes when all children close. Setting the
  REQ `request_state` to closed_cancelled alone does not stop RITM flows on most instances.
- Requesters can cancel from the portal only while the REQ awaits approval (the base
  cancel action's condition). After approval it needs the desk.

## Stop the machinery
1. On the RITM, open the **Flow executions** related list (or the workflow context for
   legacy workflows) and cancel the running context. Closing the RITM doesn't always.
2. Close open SCTASKs as Closed Incomplete/Skipped with a work note so fulfillers don't act.
3. Check what already happened and reverse it: accounts created, licences assigned, PO
   raised, device shipped. Raise a task for each reversal; a note is not enough.
4. Set pending approvals to No Longer Required so approvers aren't chasing a dead request.

## Modify instead of cancel
- RITM variables are editable in the Variable Editor for roles your instance allows. A
  change after the flow has read the variable does nothing to steps already run.
- Material changes (different model, person or cost centre) need re-approval: cancel and
  resubmit, or use a "Change my request" item referencing the original RITM.
- Start date moves: update the variable *and* any flow wait timers or scheduled tasks.

## Gotchas
- Agree a close code such as "Cancelled by requester" so fulfilment reports can exclude
  cancellations instead of counting them as failures.
- Hardware Asset Management reservations stay "On order/Reserved" until released.

## Verify
RITM closed with a reason, no running flow context, no open SCTASKs or approvals, and every
downstream action (accounts, licences, orders) reversed and recorded.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
