---
id: computing-software.digital-forensics-incident-response.evidence-handling.laboratory-evidence-intake-and-case-numbering
name: laboratory-evidence-intake-and-case-numbering
category: computing-software
field: digital-forensics-incident-response
product: evidence-handling
tags: [evidence-intake, case-numbering, chain-of-custody, forensic-lab, iso-17025, dfir]
level: practitioner
status: draft
description: "Run forensic lab evidence intake: receiving and inspecting items, case and item numbering schemes, intake photos, condition notes, request scoping and storage assignment."
sources: ["https://www.swgde.org/documents/published-complete-listing", "https://www.iso.org/standard/66912.html", "https://www.ojp.gov/pdffiles1/nij/219941.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Laboratory evidence intake and case numbering

Intake is where custody passes to the lab. Errors here (wrong item numbers, unnoticed broken seals) undermine everything after. Labs working to ISO/IEC 17025 must have a documented procedure for receipt and identification of items.

## Numbering scheme
Use one scheme everywhere: `<year>-<case seq>` for the case and `<case>-<item>` for each item, with sub-items for derived evidence:
- `2026-0147` case
- `2026-0147-003` laptop
- `2026-0147-003.01` internal SSD removed from the laptop
- `2026-0147-003.01-IMG1` forensic image of that SSD
Never re-use or re-number; voided numbers are recorded as void.

## Intake procedure
1. **Verify paperwork**: chain-of-custody form, request/authorisation (what questions, what scope, legal authority), submitter identity.
2. **Inspect packaging** before opening: seal intact, seal numbers match the form, photograph all sides. Broken or mismatched seals are noted and the submitter informed before proceeding.
3. **Open and inventory**: photograph each item, record make/model/serial/IMEI/capacity, condition (damage, power state, battery), attached media. Faraday-bag mobile devices immediately.
4. **Assign numbers and label** items (tags, not writing on the device).
5. **Custody entry**: sign receipt on the chain-of-custody form with date/time; enter in the lab evidence management system.
6. **Scope review**: confirm the analysis request is answerable and within authority; clarify ambiguities in writing.
7. **Storage**: assign a secure location (evidence locker, shelf ID); temperature/static-safe for media; record it.

## Gotchas
- Items arriving powered on (phones, laptops in sleep): decide quickly on power and isolation; document the decision.
- Digital submissions (uploads, cloud exports) need the same intake: hash on receipt and compare to the sender's hash.
- Keep intake separate from examination where possible, so the examiner gets a clean, recorded hand-off.

## Verify
Every item in the store has a unique number, an intake photo, a matching custody record and a location, and all seal discrepancies were documented and reported.
