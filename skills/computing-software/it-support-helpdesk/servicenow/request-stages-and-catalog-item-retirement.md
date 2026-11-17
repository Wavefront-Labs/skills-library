---
id: computing-software.it-support-helpdesk.servicenow.request-stages-and-catalog-item-retirement
name: request-stages-and-catalog-item-retirement
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, request-stages, catalog-item-retirement, request-fulfilment, delivery-targets, service-catalog]
level: practitioner
status: gated
description: "Configure request item stages and delivery targets so users see progress, and review then retire stale catalog items without breaking open requests or reports."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/service-catalog-management/concept/c_ServiceCatalogManagement.html"
  - "https://www.servicenow.com/docs/bundle/zurich-build-workflows/page/administer/flow-designer/concept/flow-designer.html"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-foundation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# request-stages-and-catalog-item-retirement

## Stages: what the user sees
Request items (RITMs) have a `stage` field separate from `state`. Stages are the
user-friendly progress bar on the portal ("Approval", "Fulfilment", "Delivery").
- In Flow Designer, set stages with the flow's **Stage** settings (define the stage set on
  the flow properties, then mark which actions start each stage). In legacy workflows,
  stages are set on activities.
- Keep 3-5 stages that mean something to users; "Waiting for Approval", "Ordered",
  "Being Built", "Ready for Collection", "Completed".
- Add **expected duration** per stage so the portal shows a due date; it becomes the
  delivery target on the RITM (`due_date`).

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Delivery targets
- Catalog item **Delivery time** sets the default target; flows can override per stage.
- Report RITMs past `due_date` that are still open; that list is your fulfilment SLA
  risk if you don't run task SLAs on catalog items.
- If suppliers are involved (hardware), set realistic times: a 2-day target on a laptop
  with 10-day supplier lead time just trains users to call.

## Catalog item review cadence
Every 6-12 months, per catalog owner:
1. Report items with zero or low requests in 12 months (`sc_req_item` grouped by
   `cat_item`).
2. Check items whose fulfilment group no longer exists or whose flow errors.
3. Check content: prices, models, approvals, wording.

## Retiring an item safely
1. Confirm no open RITMs (or let them finish; retiring doesn't cancel them).
2. Set **Active** false (hides it from the catalog and search) rather than deleting;
   deleting breaks historical reports and RITM references.
3. Optionally set an **Available until** date ahead of time and announce it.
4. Redirect: add a KB article or point the replacement item's meta keywords at the old
   name so searches still land somewhere.
5. Remove it from order guides and portal widgets that reference it directly.

## Pitfalls
- Stage values from one flow shown on an item using another flow show blank progress.
- Deleting variables used by old RITMs makes those records unreadable.

## Verify
A test request shows the progress bar moving through each stage with a due date; retired
items are absent from search, and last year's reports still show them.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
