---
id: defence-public-safety.corrections.offender-management-systems.booking-records-and-sentence-calculation-checks
name: booking-records-and-sentence-calculation-checks
category: defence-public-safety
field: corrections
product: offender-management-systems
tags: [corrections, offender-management-systems, oms, jail-management-system, jms, offender-management-information-system, prison-records, custody-records, nomis, digital-prison-services, booking, intake, reception, booking-number, identity-verification, biometrics, fingerprints, mugshot, warrant-entry, commitment-order, detainer, hold, sentence-calculation, release-date, time-served, jail-credit, remand-credit, good-time, earned-time, consecutive-sentences, concurrent-sentences, release-checks, wrongful-release, release-in-error, over-detention, records-office, discharge, audit-trail, data-protection, cjis, data-quality, correctional-records-officer]
level: practitioner
status: draft
description: "Operating custody records systems: accurate booking, identity and warrant entry, sentence and release-date calculation checks, audit trails and avoiding wrongful release or over-detention."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Booking records and sentence-calculation checks

**Goal:** make the custody record an accurate, legally sound account of *who* is held, *on what
authority*, and *until when* — so nobody is released in error and nobody is held a day longer
than the law allows.

Offender-management / jail-management systems (OMS/JMS) differ by vendor and agency (for
example NOMIS and the newer Digital Prison Services in England & Wales; many commercial and
in-house JMS/OMS products in US jails and state systems). The screens differ; the controls below
don't. Lawful detention depends on the documents, not the system — the system only records them.

## 1. Booking / reception
- **Identity first:** confirm the person against the committal paperwork and, where available,
  biometrics (fingerprint check, photograph). Search existing records to link to a prior booking
  instead of creating a duplicate person record — duplicates split warnings and history.
- Record aliases, dates of birth used, and identifying marks as aliases/attributes, not as new people.
- Enter **every legal authority to detain**: each warrant, remand order, sentence, detainer or
  immigration hold, with court, case number, dates and offence codes exactly as on the document.
  Scan/attach the source document where the system supports it.
- Capture alerts that drive safety elsewhere: medical and self-harm flags, separation/keep-apart,
  risk to staff, sexual-safety screening outcomes (these feed
  `defence-public-safety.corrections.inmate-classification.risk-needs-classification-and-housing-review`).
- Property and money are recorded in front of the person and signed for.

## 2. Sentence calculation
The calculation applies the jurisdiction's sentencing law: start date, credit for time on
remand/pre-sentence custody, consecutive vs concurrent terms, early-release or good-time/earned-
time provisions, licence/supervision periods, and any recall or additional days.
- **Treat the system's calculated date as a draft until checked.** System rules are configured by
  people and can be wrong or out of date after a change in the law.
- **Two-person check:** a second trained calculator independently calculates (manually or with an
  approved worksheet) and the two results must match before the date is confirmed.
- Recalculate on every new order: further sentences, appeals, remand credit updates, recalls,
  awarded or restored days.
- Keep the working: which documents, which rules, which credits. A future reviewer must be able
  to reproduce the date.
- Known failure: software rule errors can mis-set dates for whole populations at once (e.g. the
  publicly reported Washington State DOC error discovered in 2015 that released prisoners early
  over many years). Report any suspected systemic error up the chain immediately.

## 3. Release and discharge checks
Before any release, check — against source documents, not just the screen:
1. Correct person (photo/biometric match).
2. Correct release date and no outstanding authority: other warrants, detainers, holds, unpaid
   fines in default, immigration holds, recall.
3. Release conditions/licence prepared; victim-notification duties completed where they apply.
4. Supervisor sign-off as policy requires.
Release in error and over-detention are both serious incidents — over-detention is unlawful
detention and gives rise to liability.

## 4. Data handling and audit
- Records are personal and often special-category data: access only what your role needs; never
  look up people out of curiosity (audit trails log every view; in US systems CJIS policy governs
  criminal-justice information).
- Corrections to a record are made by the authorised route with a reason, never by overwriting
  history.
- Don't keep side spreadsheets of release dates — they drift from the system of record.

## Gotchas
- Two people with the same name and DOB exist; one matching field is not identity.
- Court results often arrive late or are ambiguous ("concurrent" omitted); query the court rather
  than assume.
- Remand credit is the commonest source of over-detention errors; recheck when a case ends.
- A system migration is the riskiest time for dates and alerts — validate migrated records.

## Verify
- [ ] Person linked to existing record; no duplicate created.
- [ ] Every warrant/order entered and matched to its source document.
- [ ] Release date independently checked by a second person, with the working retained.
- [ ] Pre-release checklist done against source documents; no outstanding holds.
- [ ] Access and amendments within role, with reasons recorded.

*Uncertainty:* sentence-calculation rules are entirely jurisdiction-specific and change often; this
file covers the controls around calculation, not the law itself. System names and the cited
public example should be confirmed if relied on.
