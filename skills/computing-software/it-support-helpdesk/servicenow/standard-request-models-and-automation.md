---
id: computing-software.it-support-helpdesk.servicenow.standard-request-models-and-automation
name: standard-request-models-and-automation
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-request, request-models, pre-approved-requests, request-automation, integration-hub, zero-touch-fulfilment, itil-4]
level: practitioner
status: draft
description: "Turn frequent service requests into standard request models: picking candidates from volume, defining steps and pre-approval, automating fulfilment, and measuring time saved."
sources:
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.servicenow.com/docs/"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# standard-request-models-and-automation

Goal: the top recurring requests are handled the same way every time, and
the most common are fulfilled with no human touch (ITIL 4 service request
management: request models, standardisation and automation).

## Find candidates
Pull 3–6 months of requests (and incidents that are really requests):
group by item/category, count, average handling time, number of manual
steps. Best candidates: **high volume, low risk, rule-based** — software
from the approved catalogue, shared mailbox/group access with owner
approval, licence assignment, distribution list membership, new starter
bundles.

## Define the model
For each: trigger, information required (variables), approval rule (or
pre-approved by policy), fulfilment steps with owners, expected lead time,
completion criteria, user communication. Write it down — this is the
"request model" that the catalog item and flow implement.

## Automation ladder
1. Standardised form + task template (removes back-and-forth).
2. Pre-approval for low-risk items (no approval step at all).
3. Partial automation: flow creates the account/assigns the licence; human
   verifies.
4. **Zero-touch**: flow calls Entra/AD/Intune/M365 via Integration Hub or
   API (add to group → app deploys), closes RITM, notifies user.
Keep a human-review fallback when an automated step errors (flow error
handler creates an SCTASK).

## Measure
Before/after: requests per month × minutes saved; lead time to fulfil;
percentage auto-fulfilled; error rate. Report it — it funds the next
automation.

## Gotchas
- Automating a bad process makes bad outcomes faster — clean the process
  first.
- Group-based access automation still needs owners to review membership
  periodically (access reviews).
- Service accounts used by automation need least privilege and monitoring.

## Verify
Top-10 request types each have a documented model; at least the top 3 have
automated fulfilment with measured lead time reduction.
