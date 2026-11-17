---
id: education-training.school-and-training-program-administration.student-information-systems.keeping-sis-records-attendance-and-state-reporting-clean
name: keeping-sis-records-attendance-and-state-reporting-clean
category: education-training
field: school-and-training-program-administration
product: student-information-systems
tags: [student-information-systems, sis, mis, school-mis, powerschool, infinite-campus, skyward, sims, arbor, synergy, aeries, student-records, attendance, attendance-codes, gradebook, grade-reporting, report-cards, transcripts, state-reporting, census, school-census, data-validation, data-quality, ferpa, gdpr, role-based-access, end-of-year-rollover, data-steward]
level: practitioner
status: draft
description: "Run a student information system so the data is right: one owner per data domain, controlled code sets, daily attendance checks, validation before every state return, and a safe year-end rollover."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keeping SIS records, attendance and state reporting clean

**Goal:** the SIS (PowerSchool, Infinite Campus, Skyward, Synergy in the US; SIMS,
Arbor and others in the UK; equivalents elsewhere) is the single source of truth that
funding, compliance, report cards and transcripts depend on. Most problems are not
software bugs but inconsistent data entry. Screen and menu names differ by product and
by district configuration — this skill is the operating discipline.

## 1. Assign ownership
- One **data owner** per domain: demographics & enrolment (registrar/office), attendance
  (attendance clerk), schedules (scheduler), grades (teachers, verified by registrar),
  special programmes (SEN/SPED, EL/EAL, free meals — programme coordinators).
- A **data steward** who owns the code sets, validation reports and state/national returns.
- Write a one-page data-entry guide per domain: which field, which format, which code.

## 2. Control code sets and fields
- Attendance codes, entry/exit (withdrawal) codes, ethnicity/language codes and programme
  codes usually must map to state/national definitions. Never invent a local code without
  mapping it to the reportable one.
- Lock or hide fields people shouldn't edit. Free-text where a pick-list exists produces
  junk ("Mum", "mother", "MOTHER").
- **Legal names, dates of birth and unique student IDs** are matched against state/
  national databases — typos create duplicate students and lost funding.

## 3. Attendance, daily
- Teachers take period/session attendance by a fixed time; the clerk runs the
  "attendance not taken" report daily and chases.
- Unverified absences get a contact attempt the same day (safeguarding as well as
  compliance). Code changes after the fact need a documented reason.
- Know your jurisdiction's definitions: what counts as present, tardy vs absent, half-day,
  excused vs unexcused, chronic absence thresholds (commonly 10% of sessions).

## 4. Grades and reporting periods
- Publish gradebook setup rules (categories, weighting) before term; verify setups before
  grading periods open.
- Before report cards/transcripts: run missing-grade and incomplete reports, have
  teachers fix, then **store/lock grades** (terminology varies) before printing.
- Transcript changes after storing go through a request with approval and audit trail.

## 5. State/national reporting
- Calendar every return (enrolment counts, attendance, discipline, special programmes,
  end-of-year). Typical cycle: extract → run the agency's validation → fix errors
  **in the SIS** (never only in the extract) → resubmit → keep the error logs.
- Compare counts with last submission and last year; a 15% swing usually means a
  mapping or filter error, not a real change.
- Sign-off by the person accountable, with the validated file archived.

## 6. Access and privacy
- Role-based access: least privilege; remove leavers' accounts on their last day.
- Student records are protected by law (e.g. FERPA in the US, UK GDPR) — no bulk exports
  to personal drives or unapproved apps; check vendor data-processing agreements before
  connecting third-party tools.
- Review audit logs for unusual access.

## 7. End-of-year rollover
Back up first. Then: finalise grades and attendance, run final returns, promote/retain
students, process graduates and leavers with exit codes, build next year's calendar and
schedule, and test the rollover in a sandbox if the vendor provides one. Rollover
mistakes are painful to unwind.

## Gotchas
- Duplicate student records from re-enrolment under a slightly different name.
- Withdrawn students left "active" inflate counts and breach audit rules.
- Uncertain: field names, validation tools and deadlines are vendor- and agency-specific.

## Verify
- [ ] Every domain has a named owner and an entry guide.
- [ ] "Attendance not taken" report is clear daily.
- [ ] Grades stored/locked before report cards.
- [ ] Each return validated, compared with prior counts and archived.
- [ ] Access list matches current staff roles.
