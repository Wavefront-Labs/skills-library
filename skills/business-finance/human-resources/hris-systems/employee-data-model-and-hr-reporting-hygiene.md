---
id: business-finance.human-resources.hris-systems.employee-data-model-and-hr-reporting-hygiene
name: employee-data-model-and-hr-reporting-hygiene
category: business-finance
field: human-resources
product: hris-systems
tags: [hris-systems, hris, hcm, workday, sap-successfactors, successfactors, bamboohr, oracle-hcm, employee-records, effective-dating, position-management, job-management, supervisory-organization, cost-centre, business-process, approval-workflow, employee-self-service, ess, manager-self-service, hr-reporting, headcount-report, data-quality, role-based-security, gdpr, hr-data-privacy, integrations, payroll-integration]
level: practitioner
status: draft
description: "Keep an HRIS (Workday, SuccessFactors, BambooHR class) trustworthy: core data model, effective dating, workflows, security roles, integrations and reports that tie to payroll."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Employee data model and HR reporting hygiene

**Goal:** an HR system where every worker's record is correct as of any date, changes
go through approved workflows, people see only what they should, and the headcount
report matches payroll and finance. Concepts apply across Workday, SAP SuccessFactors,
Oracle HCM, BambooHR and similar; object and menu names differ by product and aren't
verified per release here.

## 1. Core data model
- **Worker/person** (identity, personal data) ≠ **employment** (hire date, type,
  status) ≠ **job/position** (title, level, family, FLSA/overtime status, location,
  standard hours, FTE) ≠ **organisation** (supervisory org/manager line, cost centre,
  legal entity, company).
- **Position management** (each seat exists before someone fills it) vs **job
  management** (headcount is just people): position management supports budget
  control and vacancy reporting; decide once and configure consistently.
- **Compensation** attached to the employment/job record with plan, grade/band and
  effective date.
- Reference data (locations, job codes, cost centres) owned by one team with change
  control; finance owns cost centres, HR owns jobs.

## 2. Effective dating — the core skill
Every change carries an **effective date**, separate from the date it was entered.
- Hires, transfers, promotions and pay changes are entered with the date they take
  effect, even if keyed late — so reports "as of" any date are right.
- **Retro changes** across a payroll cutoff trigger retro pay; coordinate with payroll.
- **Future-dated** changes (a promotion next month) exist in the system now — reports
  must choose "as of today" vs "including future".
- Correcting an error ≠ recording a change: use the system's *correct* function for
  mistakes so history isn't polluted with fake events.

## 3. Business processes and self-service
- Each event (hire, termination, job change, leave) is a workflow with steps,
  approvers (manager, HR partner, comp, finance) and notifications.
- Self-service: employees update personal data (address, bank, emergency contacts);
  managers initiate changes. Sensitive changes (bank details) should trigger
  notification to the employee's old contact details — a fraud control.
- Termination workflows must trigger downstream actions: payroll final pay, system
  access removal, equipment return, benefits.

## 4. Security
- **Role-based** (HR partner for org X sees comp; manager sees direct and indirect
  reports; payroll sees bank details) — least privilege.
- Restrict sensitive fields (health, diversity, background checks) further.
- Review role assignments quarterly; remove access for leavers and movers.
- Apply privacy law (e.g. GDPR purpose limitation and retention) to HR data;
  log access to sensitive data.

## 5. Integrations
Typical outbound: payroll, benefits providers, identity/SSO, finance/ERP cost
allocation, learning systems. For each: owner, frequency, fields, error handling, and
a **reconciliation report** (records sent vs accepted). Silent integration failures
are the main source of payroll and access errors.

## 6. Reporting that people trust
- Define **headcount** precisely (active employees only? include leave? contractors?
  as of which date?) and publish the definition with every report.
- Monthly reconciliation: HRIS active headcount vs payroll paid employees vs FP&A plan.
  Explain every difference (unpaid leave, new hires paid next cycle, contractors).
- Data-quality dashboard: missing managers, workers without cost centre, positions
  without job code, duplicate persons, future terminations not processed.

## Gotchas
- Back-dated terminations after payroll ran = overpayments.
- Rehires creating **duplicate person records** — search before hiring.
- Bulk loads (EIBs/imports) bypassing validation — test in a sandbox tenant first.
- Org restructures done by renaming rather than effective-dated moves erase history.

## Verify
- [ ] Changes entered with correct effective dates; corrections use correct, not new events.
- [ ] Each event workflow has defined approvers and downstream triggers.
- [ ] Security roles reviewed quarterly; sensitive fields restricted.
- [ ] Integrations each have a reconciliation report checked every run.
- [ ] Headcount definition published; HRIS, payroll and finance headcount reconcile monthly.
