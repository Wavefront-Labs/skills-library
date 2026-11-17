---
id: computing-software.it-support-helpdesk.servicenow.standard-change-catalog-and-pre-approval
name: standard-change-catalog-and-pre-approval
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, standard-change-catalog, standard-change, change-template, pre-approved-change, change-enablement, change-model]
level: practitioner
status: gated
description: "Get routine support changes pre-approved as ServiceNow standard changes: proposal, template fields, retiring risky templates, and when a task must stay a normal change."
sources:
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/change-management/concept/c_StandardChangeCatalogPlugin.html"
  - "https://www.servicenow.com/docs/bundle/zurich-it-service-management/page/product/change-management/task/propose-standard-change-template.html"
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practitioner-change-enablement"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# standard-change-catalog-and-pre-approval

ITIL 4: a standard change is low risk, well understood, fully documented and pre-authorised,
so it skips CAB. Moving repetitive support work (adding a printer queue, standard patch
deployment, firewall rule from a template) to standard changes is the biggest lever on
change throughput.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Getting a template approved
1. Collect evidence: 5-10 successful normal changes of the same type with no incidents
   caused, a written procedure and a tested backout.
2. Change > Standard Change > **Propose a New Standard Change**: name, category,
   description, template values (short description, implementation plan, backout plan,
   test plan, risk, impact, assignment group, CI class), and justification.
3. The proposal is a `std_change_proposal` record that goes to the change manager/
   template owners for approval. Approved = template published in the Standard Change
   Catalog (`std_change_record_producer`).
4. Template owner and review date recorded. Review at least yearly.

## Using one
Change > Create New > Standard Changes > pick the template. Read-only fields come from
the template; you add the specific CI, schedule and any variables. It goes straight to
Scheduled after you request it; no CAB approval step.

## Keeping it standard
- Any deviation from the documented steps makes it a normal change. If the job needs a
  different backout, it isn't standard.
- Template health: change management can auto-flag templates with failed changes or
  caused incidents (the base "Standard change template" metrics show success rate). Two
  failures in a quarter, suspend the template and review.
- Modify a template via **Propose Modification**, not by editing the record directly.
- Still subject to change freeze and blackout windows unless the template says otherwise.

## Good candidates for a support team
Patch Tuesday deployment rings, adding users to a print queue server, DNS record add for
an existing zone, certificate renewal of a known type, adding a standard app to a
software deployment group. Poor candidates: anything touching authentication, core
network, or first-of-a-kind work.

## Gotchas
- "Standard" used as a shortcut to avoid CAB for a risky task is how most change-induced
  outages start; audit a sample monthly.
- Templates pinned to a CI class won't let you pick a CI of another class.

## Verify
The template shows Active with owner and review date, recent standard changes from it
closed successful, and no incidents linked to them as Caused by change.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
