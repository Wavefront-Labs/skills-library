---
id: computing-software.it-support-helpdesk.user-support-communication.escalating-to-vendors-and-managing-vendor-cases
name: escalating-to-vendors-and-managing-vendor-cases
category: computing-software
field: it-support-helpdesk
product: user-support-communication
tags: [it-support-helpdesk, user-support-communication, escalation, vendor-escalation, vendor-case, support-severity, microsoft-support, entitlement, duty-manager-escalation, underpinning-contract]
level: practitioner
status: draft
description: "Open and drive vendor support cases: entitlement and severity, a case package that skips the script, chase cadence, duty-manager escalation, and mirroring status in tickets."
sources:
  - "https://learn.microsoft.com/en-us/microsoft-365/admin/get-help-support"
  - "https://www.axelos.com/certifications/itil-service-management"
  - "https://www.thinkhdi.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# escalating-to-vendors-and-managing-vendor-cases

Goal: vendor cases move at the speed your contract pays for, and your
internal ticket always shows where the case stands.

## Before opening
- **Entitlement**: which contract/support plan, contract ID, authorised
  contacts (many vendors only accept cases from named contacts), hardware
  serial/warranty.
- **Severity** using the vendor's definitions (Microsoft: A critical /
  B / C; others Sev1–4). Overstating severity damages credibility; Sev A/1
  usually requires 24×7 availability from you.
- Check vendor service health/status page and known issues first.

## Case package
Same as an internal escalation package plus: exact versions/builds, tenant
or account ID, timestamps with timezone, correlation/request IDs from error
pages, logs the vendor will ask for anyway (collect them before calling:
e.g. Microsoft Support and Recovery Assistant output, HAR file for web
apps, system logs). State what you've already done so you skip the
first-line script.

## Driving the case
- Record vendor case number, contacts and next steps in your ticket (work
  notes), and set the ticket to Pending vendor with a follow-up date.
- Agree next update time with the engineer; chase when it passes.
- Hardware: ensure the on-site appointment has building access info and
  the user's availability.

## Escalating within the vendor
When progress stalls (missed updates, wrong engineer, impact grows):
ask for the **duty manager / escalation manager**, give case number,
business impact, what's been missed; or use your account manager/TAM
(Premier/Unified customers). Raise severity only if impact actually
increased.

## Closing
Get the root cause or bug ID in writing; record in ticket/problem; close the
vendor case only after confirming the fix; feed vendor performance into
contract reviews.

## Gotchas
- Sharing logs: redact or use the vendor's secure upload; data protection
  terms apply.
- Cases opened from personal accounts are lost when people leave — use
  shared/team contacts.

## Verify
Every pending-vendor ticket has a case number, last vendor update date and
next follow-up date.
