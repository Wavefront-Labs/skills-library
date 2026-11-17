---
id: health-medicine.pharmacy.dispensing-and-verification.prescription-clinical-and-final-accuracy-check
name: prescription-clinical-and-final-accuracy-check
category: health-medicine
field: pharmacy
product: dispensing-and-verification
tags: [dispensing-and-verification, pharmacy, pharmacist, dispensing, prescription-verification, clinical-check, final-check, accuracy-check, legal-check, drug-interactions, dose-check, renal-dosing, pediatric-dosing, allergy-check, duplicate-therapy, controlled-drugs, barcode-scanning, ndc, lasa, dispensing-errors, pharmacy-technician, act, rph, tall-man-lettering, counselling]
level: practitioner
status: draft
description: "Verify a prescription in three passes: legal/administrative validity, clinical appropriateness (dose, interactions, allergy, renal, duplication), and the final product-accuracy check."
sources: ["USP and state board of pharmacy dispensing rules (US)", "GPhC/RPS professional standards (UK)", "ISMP error-prone abbreviations list"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prescription verification: legal, clinical and final accuracy checks

> General professional reference. Legal requirements (prescription validity, controlled-drug rules, who may perform which check) differ by jurisdiction — follow your local law and SOPs. Dose ranges must be checked in a current reference.

**Goal:** catch the wrong drug, wrong dose, wrong patient and wrong product before it
leaves the pharmacy. Separate the checks so each has your full attention — most
dispensing errors happen when one glance tries to do all three.

## Pass 1 — Legal and administrative (is this a valid order for this patient?)
- Patient identity: two identifiers (name + DOB/address), matched to profile. Watch same-name patients.
- Prescriber: legitimate, within scope, signature/e-signature, registration/DEA/number as required.
- Prescription complete: drug, strength, form, dose, route, frequency, quantity, date;
  not expired; refills valid. Controlled drugs: schedule-specific requirements
  (quantity in words and figures where required, validity period, PDMP check in the US).
- Ambiguity → **clarify, don't interpret**. Error-prone notations: trailing zeros (5.0 mg),
  missing leading zeros (.5 mg), "U" for units, "QD"/"QOD", "MS"/"MSO4".

## Pass 2 — Clinical check (is it right for *this* patient?)
Work a fixed list, every time:
1. **Indication** — does the drug fit what the patient is being treated for? (Look up
   if not obvious — this catches LASA mix-ups like hydroxyzine/hydralazine.)
2. **Dose** — within range for age, weight (pediatric mg/kg and **max adult dose cap**),
   indication, and frequency. Watch daily vs weekly (methotrexate), mg vs mcg, and
   liquid concentrations.
3. **Renal/hepatic function** — CrCl or eGFR-based adjustment where needed; check recent labs.
4. **Allergies and intolerances** — true allergy vs side effect; cross-sensitivity.
5. **Interactions** — triage the software alerts: act on contraindicated/major ones
   (e.g. QT-prolonging combinations, serotonergic stacks, CYP3A4 inhibitors with
   statins/DOACs), don't override reflexively.
6. **Duplication** — same class from two prescribers; combination products containing an ingredient already taken (paracetamol/acetaminophen).
7. **Special populations** — pregnancy/lactation, older adults (Beers criteria), pediatrics.
8. **Continuity** — is this a change from the last fill? Unexplained change = call.
Document every intervention: problem, who you contacted, outcome.

## Pass 3 — Final accuracy check (is the product in the bag what was verified?)
- Scan barcode/NDC of the stock bottle against the label; check drug, strength, form,
  quantity, and manufacturer if substitution rules apply.
- Visually inspect tablets/capsules against an image or description (imprint code).
- Label: right patient, directions match the verified sig, auxiliary labels, expiry/BUD.
- Liquids: reconstituted correctly, right volume, oral syringe provided for pediatric doses.
- Bag check: right patient's items only; nothing from the previous patient left behind.

## Gotchas
- **High-alert/LASA pairs** deserve a forced pause: tall-man lettering, separate shelf locations, scan-every-time.
- Your eye reads what it expects: check from the stock container to the label, not label to stock.
- Interruptions during a check → restart that check from the top.
- Pediatric liquids are the commonest 10-fold error source; recalculate dose in mg/kg
  and in mL independently, using a current pediatric reference.
- Who may perform the final check (pharmacist vs accredited technician) is jurisdiction-specific.

## Verify
- [ ] Three passes performed separately; ambiguous orders clarified with the prescriber.
- [ ] Clinical checklist (indication, dose, renal, allergy, interactions, duplication, population) completed.
- [ ] Product barcode-scanned and visually matched; label matches verified directions.
- [ ] Interventions documented; patient flagged for counselling where new/changed.
