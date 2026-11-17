---
id: repair-maintenance.aircraft-maintenance.scheduled-inspection-airworthiness.annual-inspection-ad-research-and-logbook-entry
name: annual-inspection-ad-research-and-logbook-entry
category: repair-maintenance
field: aircraft-maintenance
product: scheduled-inspection-airworthiness
tags: [aircraft-maintenance, scheduled-inspection-airworthiness, annual-inspection, 100-hour-inspection, part-43-appendix-d, airworthiness-directive, ad-compliance, drs, ad-list, logbook-entry, 43-11, return-to-service, ia, inspection-authorization, discrepancy-list, squawks, type-certificate-data-sheet, tcds, form-337, arc, part-ml, easa, 91-409]
level: practitioner
status: docs-checked
description: "Run a light-aircraft annual/100-hour inspection: records and AD research first, Part 43 App. D checklist, discrepancy handling, and a compliant 43.11 entry."
sources:
  - https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-14.xml?part=91&section=91.409
  - https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-14.xml?part=43&section=43.11
  - https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-14.xml?part=91&section=91.207
  - https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-14.xml?part=91&section=91.411
  - https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-14.xml?part=65&section=65.95
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Annual inspection, AD research and logbook entry

**Goal:** determine, and certify, that an aircraft conforms to its type design and is in
condition for safe operation, or give the owner a clear list of why not. US framing
(14 CFR Part 43/91): 91.409 requires an annual inspection within the preceding 12 calendar
months, and a 100-hour inspection for aircraft carrying persons for hire or used for paid
flight instruction. An inspection authorization (IA) holder may perform an annual (65.95).
Other regulators (for example EASA) have different paperwork and roles; check yours.

## 1. Records before wrenches (half the inspection is paperwork)
1. Gather: airframe, engine and propeller logbooks, equipment list and weight & balance,
   alteration paperwork (Form 337s/STCs), current AD compliance record, POH/AFM.
2. Pull the **Type Certificate Data Sheet (TCDS)** for airframe, engine and propeller from
   the FAA. Confirm the installed engine/prop models are approved.
3. **AD research:** search the FAA's AD listings by make/model for airframe, engine,
   propeller, and every appliance (magnetos, vacuum pumps, ELT, seat rails, carburettor,
   avionics). Note one-time vs recurring ADs, and the method of compliance chosen last time.
   Build an AD list table: AD number, subject, applicability (check serial ranges!),
   method, date/hours complied, next due.
4. Check life-limited parts and calendar items: the ELT must be inspected within 12 calendar
   months of the last inspection (91.207); static pressure system and altimeter tests fall
   under 91.411 (within 24 calendar months where it applies).
5. Look up manufacturer service bulletins; they are not an AD unless an AD mandates them.

## 2. The inspection itself
Use the manufacturer's inspection checklist if one exists; at minimum Part 43 Appendix D
scope: preparation (panels, cowling, cleaning), fuselage, cabin and cockpit, engine and
nacelle, landing gear, wing and centre section, empennage, propeller.
- Remove inspection panels, cowlings, fairings, seats/carpets as needed; you can't
  inspect what you can't see.
- Engine: cylinder compression, metal particles or foreign matter on screens and sump
  drain plugs, exhaust stacks for cracks, defects and improper attachment.
- Controls: full travel, safetying, correct direction of movement.
- Structure: corrosion, cracks at known hotspots (check type-club and SB lists), loose rivets.
- Placards and instruments marked per TCDS/POH; required equipment working.
- Run-up after reassembly and a leak check.

## 3. Discrepancies
- Write every finding as a clear, specific squawk ("L/H elevator outboard hinge bolt
  missing cotter pin", not "elevator needs work").
- Owner may have them corrected by anyone appropriately certificated; you may re-inspect
  only the items.
- If the aircraft is not airworthy, you do not approve. 43.11(b) requires giving the owner
  or lessee a signed and dated list of discrepancies, and the logbook entry states that a
  dated list has been provided.

## 4. The logbook entry (43.11)
Must include: type of inspection and brief description of its extent; date; aircraft total
time in service; signature, certificate number and kind of certificate; and either the
airworthy statement or the statement that a dated list of discrepancies and unairworthy
items has been provided. Example structure:

> *[Date], TT [xxxx.x] hrs. I certify that this aircraft has been inspected in accordance
> with an annual inspection and was determined to be in airworthy condition. AD compliance
> record attached. [Signature, certificate kind and no.]*

Update the AD record and W&B if equipment changed.

## Gotchas
- AD applicability by serial number catches people: an AD "not applicable" must be shown, not assumed.
- Recurring ADs are the most commonly overdue item: compute next-due in hours *and* date.
- An undocumented alteration makes the aircraft unairworthy until resolved.
- The entry wording above is a common form, not legal advice; verify against current
  regulations and your local FSDO/authority guidance.

## Verify
- [ ] TCDS, equipment list and W&B reviewed; installed engine/prop conform.
- [ ] AD list covers airframe, engine, prop and appliances with applicability shown.
- [ ] All Appendix D/manufacturer checklist areas inspected, ground run completed.
- [ ] Discrepancies written specifically; open items lead to a list given to owner.
- [ ] 43.11 entry has date, TT, extent, signature, certificate number and correct statement.

## Checked

Date checked: 2026-11-01. Jurisdiction: United States (14 CFR).
Confirmed in eCFR text: 91.409 (12 calendar months; 100 hours for hire/instruction), 43.11(a)-(b) entry contents and signed dated discrepancy list, 91.207 ELT inspection within 12 calendar months, 91.411 static/altimeter within 24 calendar months, 65.95 IA may perform an annual, Appendix D groups and the engine compression/screens/exhaust items.
Removed as unconfirmed: who may sign a 100-hour, EASA Part-ML claim, 91.413 transponder interval, Part 135 SB remark, magneto timing, oil filter cut-open, tensiometer, hoses/baffles/mounts items, 43.9 reference, radio/miscellaneous group, DRS and AC 39-7D references.

Method: documentation only; no commands were run.
