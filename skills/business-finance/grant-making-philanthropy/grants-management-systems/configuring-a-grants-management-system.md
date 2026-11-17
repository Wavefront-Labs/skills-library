---
id: business-finance.grant-making-philanthropy.grants-management-systems.configuring-a-grants-management-system
name: configuring-a-grants-management-system
category: business-finance
field: grant-making-philanthropy
product: grants-management-systems
tags: [grants-management-systems, gms, grants-management-software, fluxx, smartsimple, submittable, blackbaud-grantmaking, salesforce-nonprofit, application-portal, application-form, review-workflow, workflow-states, reviewer-assignment, award-tracking, payment-schedule, reporting-requirements, grants-reporting, data-model, configuration, data-migration, foundation-operations, grants-manager, philanthropy]
level: practitioner
status: draft
description: "Set up and run a grants-management platform (Fluxx/SmartSimple/Submittable class): data model, application portal, workflow states, reviewer assignment, award payments, reports and clean data."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Configuring a grants-management system

**Goal:** a grants-management system (GMS) that mirrors your actual grant lifecycle,
gives applicants a painless portal, routes work to the right people, and produces
reliable data on who you fund. Written for the class of tools (Fluxx, SmartSimple,
Submittable, Blackbaud Grantmaking, Salesforce-based builds and similar): menu names
and features differ — *specific UI paths are not given because they vary by product and
version*; map the concepts to your platform's documentation.

## 1. Map the lifecycle before touching settings
Draw the stages on paper with owners: inquiry → eligibility quiz → LOI → invite →
full application → staff review → external review → due diligence → panel/board →
award → agreement signed → payments → reports due → close-out (and declined/withdrawn
branches). Each stage becomes a **workflow state**; each hand-off becomes a
**transition** with a role allowed to perform it. Keep it to the stages you really
use — every extra state is a place grants get stuck.

## 2. Data model: decide the records
Typical core objects: **Organisation**, **Contact**, **Request/Application**,
**Grant/Award**, **Payment**, **Report/Requirement**, **Review**. Decisions to make:
- One record per application that becomes the grant (simpler), or separate request and
  grant records (cleaner when one request yields several awards).
- **Controlled picklists** for programme, focus area, geography, grant type, population
  served — aligned with a recognised taxonomy if you want sector benchmarking
  (e.g. a philanthropy classification system). Free-text here destroys reporting.
- Unique organisation identifiers (charity/company number) to prevent duplicates.

## 3. Application portal
- Eligibility quiz up front that routes out ineligible applicants politely.
- Forms: save-and-return, word limits shown, character limits generous, file-type
  rules explicit, **pre-fill** organisation data from prior applications.
- Branching questions instead of one long form for all grant types.
- Test with 2–3 real applicants (including someone on a phone and someone using a
  screen reader) before launch. Publish the questions as a PDF so people can draft offline.

## 4. Review workflow
- Reviewer roles with access only to assigned applications; **conflict-of-interest
  declaration** step before access (see application-review-and-award.scoring-and-due-diligence).
- Scoring forms replicating the rubric, with required justification fields.
- Auto-assignment rules (by programme or region) plus manual override; due dates and reminders.
- Dashboards: applications by state, overdue reviews, score distributions per reviewer.

## 5. Awards, payments and requirements
On award, generate: the grant agreement (template merge fields), a **payment schedule**
(amounts, dates, conditions such as "report received"), and **requirements** (reports
due, with reminders to grantee and officer). Integrate or reconcile with the finance
system — the GMS tracks commitments; the ledger records payments. Reconcile monthly.

## 6. Reporting and data hygiene
- Build standard reports first: pipeline by state, approvals by programme/year,
  commitments ladder, payments due next quarter, overdue reports, grantee demographics
  (if collected, with consent and clear purpose).
- Assign a **data owner**; quarterly checks for duplicates, missing picklist values,
  orphan payments.
- Permission roles reviewed annually; leavers removed promptly.

## 7. Migration and launch
Migrate active grants (with open payments and requirements) first; historical grants
can be summary-level. Clean before migration, not after. Run a parallel period for
payments. Train staff with real scenarios, write a short internal manual of *your*
configuration choices.

## Gotchas
- Over-customising early locks you into expensive maintenance; prefer configuration
  over custom code.
- Email notifications from the platform land in spam unless the sending domain is
  authenticated — test applicant-facing emails.
- Personal data (applicant contacts, demographics) falls under privacy law; set retention rules.

## Verify
- [ ] Workflow states match the paper lifecycle; no grant can skip a required approval.
- [ ] Picklists are controlled; organisation duplicates prevented by ID.
- [ ] Portal tested by real applicants, including mobile and assistive tech.
- [ ] Reviewer COI step and access restrictions confirmed with a test account.
- [ ] Payments reconcile to the finance ledger monthly.
- [ ] Standard reports run without manual cleanup.
