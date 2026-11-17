---
id: health-medicine.pharmacy.medication-safety.high-alert-and-lasa-medication-safeguards
name: high-alert-and-lasa-medication-safeguards
category: health-medicine
field: pharmacy
product: medication-safety
tags: [medication-safety, pharmacy, high-alert-medications, ismp, lasa, look-alike-sound-alike, tall-man-lettering, hierarchy-of-intervention-effectiveness, forcing-functions, independent-double-check, smart-pumps, dose-error-reduction-software, concentrated-potassium-chloride, insulin, opioids, anticoagulants, methotrexate, neuromuscular-blockers, never-events, medication-error, root-cause-analysis, incident-reporting, just-culture, swiss-cheese-model]
level: practitioner
status: draft
description: "Design safeguards for high-alert and look-alike/sound-alike drugs using the hierarchy of controls: forcing functions, standardisation, tall-man, smart pumps, double checks, and error reporting."
sources: ["ISMP List of High-Alert Medications (acute, community)", "ISMP Targeted Medication Safety Best Practices for Hospitals", "WHO Medication Without Harm", "Joint Commission NPSG"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# High-alert and LASA medication safeguards

> General professional reference for pharmacy and medication-safety leads. Check the current ISMP lists and national alerts; examples here are illustrative.

**Goal:** some drugs don't cause errors more often — they cause *more harm* when an
error happens. Put the strongest available control on each failure mode instead of
relying on "be careful" memos and staff vigilance.

## 1. Know the usual suspects
**High-alert (ISMP-style list):** insulin, opioids (especially IV, hydromorphone/morphine
confusion, fentanyl patches in opioid-naive), anticoagulants (heparin, warfarin, DOACs,
LMWH), **concentrated electrolytes** (KCl, hypertonic saline), neuromuscular blockers,
oral **methotrexate** (daily vs weekly), chemotherapy, IV sedation, epidural/intrathecal
drugs, pediatric liquids, magnesium sulphate.
**LASA pairs:** hydroxyzine/hydralazine, oxycodone/OxyContin, Humalog/Humulin,
vinBLAStine/vinCRIStine, DOPamine/DOBUTamine, carboplatin/cisplatin, clonazePAM/cloNIDine.

## 2. Apply the hierarchy of interventions (strongest first)
1. **Forcing functions & constraints** — remove concentrated KCl from ward stock;
   oral syringes that can't connect to IV lines (ENFit); vinca alkaloids only in minibags
   (never syringes) to prevent intrathecal administration; weekly-only methotrexate order sentences.
2. **Automation & computerisation** — barcode scanning at dispensing and bedside, smart
   infusion pumps with **dose-error reduction software** (hard limits) and EHR interoperability,
   CPOE maximum-dose alerts tuned to fire rarely but meaningfully.
3. **Standardisation & simplification** — standard concentrations (one heparin infusion,
   one insulin infusion), protocols, pre-mixed products, restricted formulary, weight in kg only.
4. **Redundancies** — **independent double checks** (two people calculate separately,
   not one watching the other) for a small, chosen set; too many double checks become rubber stamps.
5. **Reminders & checklists, labels, tall-man lettering, separate storage.**
6. **Rules, policies, education** — weakest; necessary but never sufficient alone.
Layer several levels for each high-risk process.

## 3. LASA-specific controls
Tall-man lettering on shelves, labels and EHR picklists; separate physical locations;
indication on prescriptions; minimum 3–5 characters to search drug names in CPOE;
review new products' packaging before stocking; scan every product.

## 4. Learning from errors and near misses
- **Report** errors and near misses (local system, national programmes such as ISMP MERP
  in the US). Near misses are free lessons.
- **Just culture:** separate human error (console), at-risk behaviour (coach, fix
  the incentive) and reckless behaviour (sanction).
- Serious events: **root cause analysis** or RCA² — map the process, ask "why" at each
  failed barrier, and produce actions ranked by strength; "re-educate staff" alone is a weak action.
- Feed findings back and measure: pump-library compliance, override rates, barcode scan rates.

## Gotchas
- Alert fatigue: override rates >90% mean the alert is noise — redesign, don't add another.
- Workarounds (scanning a barcode taped to the counter) signal a broken process; investigate why.
- Pediatric areas: single standard concentrations and weight-based limits matter most here; verify any pediatric limits against current references.

## Verify
- [ ] Organisation's high-alert list reviewed against current ISMP list; each item has named safeguards.
- [ ] At least one control from levels 1–3 exists for each high-alert process (not only policy/education).
- [ ] LASA pairs in stock identified with tall-man, separation and scanning.
- [ ] Smart-pump drug library current, with hard limits, and compliance monitored.
- [ ] Error reports trended and RCA actions rated by strength.
