---
id: computing-software.it-support-helpdesk.servicenow.designing-catalog-items-and-variables
name: designing-catalog-items-and-variables
category: computing-software
field: it-support-helpdesk
product: servicenow
tags: [it-support-helpdesk, servicenow, service-catalog, service-request, catalog-item-design, catalog-variables, variable-sets, catalog-ui-policy, record-producer, reference-qualifier]
level: practitioner
status: gated
description: "Build ServiceNow catalog items users complete correctly: user-language names, variable types and sets, UI policies over client scripts, reference qualifiers, and record producers."
sources:
  - "https://www.servicenow.com/docs/"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://developer.servicenow.com/dev.do"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# designing-catalog-items-and-variables

Goal: a request form that captures everything fulfilment needs on the first
submit, in under two minutes for the user.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Before building
- Start from the **fulfilment team's** checklist: what do they ask users
  for today in follow-up emails? Those are your variables.
- Name items as users search: "Request new software", "I need access to a
  shared mailbox" — not "SW-REQ-01".
- One item per outcome; avoid mega-forms with 40 conditional fields.

## Variables
| Need | Type |
|---|---|
| Pick a user/CI/group | **Reference** with a reference qualifier (e.g. active users only, `active=true^u_type=employee`) |
| Fixed choices | Select box / Multiple choice (≤ 7 options), Lookup select for table-driven lists |
| Yes/No toggles | Checkbox / Yes-No |
| Free text | Single line / Multi-line — sparingly |
| Dates | Date (with validation for lead time) |
| Instructions | Rich text label / Macro (not a question) |
Reusable groups → **Variable sets** (e.g. "Requested for + location" used by
every item). Mark mandatory only what fulfilment truly requires.

## Dynamic behaviour
- **Catalog UI policies** (no code) to show/hide/make mandatory based on
  answers — prefer over Catalog Client Scripts.
- Client scripts (`onChange`, `g_form`) only for logic UI policies can't do
  (calculations, GlideAjax lookups).
- Show price/approvals/delivery time where relevant so users know what
  happens next.

## Record producers
For things that should create an incident/other record (e.g. "Report a
problem with your laptop" creating an incident with category pre-set) — a
**record producer** maps variables to fields with `producer.*` / script.

## Test
Submit as an end user (impersonate) on the portal and in mobile; check the
RITM variables read clearly for the fulfiller, approvals route, and tasks
generate.

## Gotchas
- Renaming variables after go-live breaks scripts/flows referencing them by
  name; add new ones instead.
- Reference variables to sys_user exposing all users may be a privacy
  concern — qualifiers and ACLs.

## Verify
Fulfilment follow-up questions ("what do you need exactly?") drop for that
item; abandoned carts low; first-submit completeness ≥ 95 %.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (axelos.com, developer.servicenow.com, servicenow.com); no readable alternative was found.

Method: documentation only; no commands were run.
