---
id: law-government.immigration-law.immigration-case-management-software.forms-assembly-deadlines-and-intake-workflows
name: forms-assembly-deadlines-and-intake-workflows
category: law-government
field: immigration-law
product: immigration-case-management-software
tags: [immigration-law, immigration-case-management-software, docketwise, inszoom, mitratech, cerenade, efile, legal-practice-management, smart-forms, questionnaire, client-intake, client-portal, form-edition, uscis-forms, e-filing, receipt-notice, case-status, deadline-tracking, docketing, expiration-tracking, i-94, filing-packet, conflict-check, data-privacy]
level: practitioner
status: draft
description: "Use immigration case-management platforms (Docketwise, INSZoom and similar) well: intake questionnaires, form auto-fill, edition control, deadline and expiry tracking, packet assembly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Forms assembly, deadlines and intake workflows

**Goal:** get accurate data into immigration forms once, reuse it safely across filings,
and never miss a deadline or status expiry. Written for platforms such as Docketwise and
INSZoom (corporate-immigration heavy) and their competitors. Menus and feature names
differ between products and releases — this skill describes the workflow, not exact
clicks; confirm specifics in the vendor's current help centre.

## 1. Set up the matter correctly
- Run a **conflict check** before opening the matter (especially employer + employee
  representations — joint representation needs informed consent).
- Create the contact records once: beneficiary, petitioner/employer, family members.
  These records are the single source that populates every form, so duplicates are the
  root of most data errors. Merge duplicates rather than creating new ones.
- Attach the matter type (e.g. family petition + adjustment, H-1B extension) so the
  platform's templates load the right forms, checklists and task lists.

## 2. Intake via questionnaire
- Send the client the platform's **smart questionnaire** through the client portal
  rather than a PDF; answers map directly to form fields.
- Review answers before they flow to forms: clients misread questions about prior
  arrests, travel and status violations. Follow up in a meeting on every "yes" and
  every blank.
- Collect address and employment history with no gaps (many forms require five years
  or more); the platform will flag empty date ranges in some products, but don't rely on it.
- Request documents with a checklist and track receipt; store them in the matter, not
  email.

## 3. Form assembly
- **Edition control**: agencies reject outdated form editions. After any agency update,
  confirm the platform has pushed the new edition and that in-progress drafts migrated
  correctly — re-check fields that moved.
- Auto-filled data still needs a field-by-field attorney review against source documents
  (passport, I-94 record, prior approvals). Name spelling and date formats are common
  failure points.
- Use the platform's validation/"missing fields" report, then print a review copy for the
  client to check and sign. Keep the signed copy.
- For agency **e-filing** integrations, verify which forms the integration supports
  today; others still require paper or the agency's own online account.

## 4. Deadlines and expirations
- Docket every hard date with the source document attached: RFE and NOID response
  dates, appeal deadlines, hearing dates, biometrics appointments.
- Track **status and document expiries** for every beneficiary: visa status end (I-94),
  passport, work permit, travel document, H-1B maximum period, PERM recruitment windows.
  Set reminders at intervals long enough to prepare a filing (e.g. 6 months / 90 / 60 / 30
  days — choose per matter type).
- Import receipt notice numbers and enable **case-status syncing** where offered, but
  confirm important changes on the agency site directly.
- Corporate clients: use dashboards/reports for HR showing upcoming expirations by
  employee.

## 5. Packet preparation
- Generate the cover letter and exhibit index from the platform templates, then edit.
- Assemble in the order the filing instructions require; include fee and payment form;
  scan the final, signed packet into the matter before sending.
- Record tracking numbers and the date sent.

## Gotchas
- A client-entered portal answer can silently overwrite attorney-verified data in some
  setups — check sync direction and lock reviewed fields if the tool allows.
- Data protection: immigration files contain sensitive personal data. Use role-based
  permissions, MFA and the vendor's data-residency options; never send passports by
  ordinary email.
- Exports: confirm you can export complete matters (forms, documents, notes) before you
  depend on a vendor.

## Verify
- [ ] One contact record per person; no duplicates feeding forms.
- [ ] Every form on the current edition and attorney-reviewed against source documents.
- [ ] All deadlines and expiries docketed with reminders and source attached.
- [ ] Signed review copy and final filed packet stored in the matter.
- [ ] Access controls and MFA enabled for all users.
