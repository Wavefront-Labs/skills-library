---
id: computing-software.it-support-helpdesk.servicenow.self-service-portal-taxonomy-and-forms
name: self-service-portal-taxonomy-and-forms
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, self-service-portal, self-service, portal-design, service-portal, employee-center, catalog-taxonomy, portal-search]
level: practitioner
status: draft
description: "Design a self-service portal users actually finish: task-based categories in user language, short catalog forms, search tuning, and measuring abandonment in ServiceNow portals."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.nngroup.com/articles/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# self-service-portal-taxonomy-and-forms
Goal: a user who needs something types or clicks to the right form in
under a minute and submits it without calling the desk.

## Taxonomy in the user's words
- Organise by what people want to do ("Get software", "New starter",
  "Report something broken", "Access to a shared folder"), not by IT team
  names ("Desktop Engineering", "IAM").
- 6-9 top categories; any item reachable within two clicks.
- Put the same item in several categories if users look in several places.
- Test with a card sort or tree test (5-10 users) before building.

## Forms people complete
- Ask only what fulfilment needs. Every variable must have an owner who
  uses it; remove the rest.
- Pre-fill from the user record (`gs.getUserID()` defaults: requested for,
  location, manager, department).
- Use reference fields and select boxes, not free text, for anything
  routed or approved on (application name, access level).
- **UI policies / catalog client scripts** to show follow-up questions
  only when relevant.
- Plain help text under each field with an example value.
- Keep mandatory fields minimal; long forms are abandoned.

## Search
- Most users search. Add **meta tags/keywords** on catalog items for the
  words users type ("VPN", "Teams phone", "Adobe").
- Review AI Search / portal search logs monthly: top searches with no
  click = missing content or bad naming.
- Promote knowledge articles and catalog items together in results.

## Measure and iterate
- Abandoned cart / form start vs submit (via portal analytics or Usage
  Analytics in Service Portal / Employee Center).
- Incidents opened via phone that had a portal item available → candidate
  for renaming or promotion.
- Requests with "Other" chosen frequently → missing item.

## Gotchas
- Building one generic "Request anything" form produces unroutable
  tickets; keep it as a fallback, not the main path.
- Category names copied from the org chart change at each reorg.
- Mobile layout: test the forms on a phone (Now Mobile / responsive).

## Verify
A tree test shows > 80% of users find the right item for common tasks, and
form completion rate is tracked monthly.
