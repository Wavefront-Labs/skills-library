---
id: computing-software.it-support-helpdesk.servicenow.order-guides-for-multi-item-requests
name: order-guides-for-multi-item-requests
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, order-guide, service-catalog, rule-base, cascading-variables, new-hire-request, service-request]
level: practitioner
status: gated
description: "Build ServiceNow order guides: describe-needs variables, rule base conditions, cascading variables, and the one-REQ-many-RITM result for new-starter bundles."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/service-catalog-management/concept/c_OrderGuides.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/service-catalog-management/task/t_DefineAnOrderGuide.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/service-catalog-management/concept/c_CascadeVariablesOrderGuide.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# order-guides-for-multi-item-requests

An order guide (`sc_cat_item_guide`) asks a few questions once, then adds the right set of
catalog items to one order. Classic use: new starter (laptop + accounts + phone + access).

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Build (Service Catalog > Catalog Definitions > Order Guides)
1. Create the guide: name, catalogs, category. Two-step checkout lets users review the
   chosen items before submitting.
2. **Describe needs** variables on the guide: department, role, location, start date,
   "needs a phone?". Keep it under about 8 questions.
3. **Rule base** related list: each rule is a condition on guide variables that includes a
   catalog item, e.g. `role=Field engineer` includes Rugged laptop; `needs_phone=true`
   includes Mobile phone. Rules with no condition always include their item.
4. **Cascade variables**: tick Cascade variables on the guide and give the child items
   variables with the *same name* (`requested_for`, `start_date`). Values flow down; hide
   the duplicates on the child with a catalog UI policy.
5. For logic the rule base can't express, use the order guide script (`guide.add()`
   style item inclusion) rather than hundreds of rules.

## Result
One REQ, one RITM per included item, each with its own fulfilment flow and SCTASKs.
Report fulfilment at RITM level; the REQ closes when every RITM closes.

## Design rules
- Don't rebuild child item logic in the guide; each child item must still work alone.
- Mandatory child variables that are not cascaded block checkout. Cascade them, default
  them, or make them non-mandatory in the guide context.
- State lead times in the guide description (e.g. laptop 5 business days) and validate
  the start date with a catalog client script.
- Restrict who sees the guide with user criteria (e.g. people managers and HR).

## Gotchas
- Cascading matches by variable *name*; a typo fails silently and the child shows blank.
- Rule base edits don't affect requests already submitted.
- Service Portal renders guides with the SC Order Guide widget; test there, not only in
  the platform UI.

## Verify
Submit as a test manager with two different role answers; confirm the expected RITM set,
cascaded values on each RITM, and that each item's fulfilment flow started.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
