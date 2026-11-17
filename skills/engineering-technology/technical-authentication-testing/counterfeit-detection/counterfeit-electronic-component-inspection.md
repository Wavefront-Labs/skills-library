---
id: engineering-technology.technical-authentication-testing.counterfeit-detection.counterfeit-electronic-component-inspection
name: counterfeit-electronic-component-inspection
category: engineering-technology
field: technical-authentication-testing
product: counterfeit-detection
tags: [counterfeit-detection, counterfeit-electronic-components, suspect-counterfeit, sae-as6081, sae-as5553, sae-as6171, idea-std-1010, external-visual-inspection, marking-permanency, resistance-to-solvents, dynasolve, acetone-test, blacktopping, resurfacing, remarking, x-ray-inspection, xrf, lead-finish, decapsulation, die-marking, golden-sample, gidep, erai, obsolete-parts, broker-parts, eee-parts]
level: practitioner
status: draft
description: "Screen broker/open-market ICs for counterfeits per SAE AS6081/AS6171 and IDEA-STD-1010: visual, marking/blacktop solvent tests, X-ray, XRF, decap die check, and GIDEP/ERAI reporting."
sources: ["SAE AS5553 Counterfeit Electrical, Electronic, and Electromechanical (EEE) Parts; Avoidance, Detection, Mitigation, and Disposition", "SAE AS6081 Fraudulent/Counterfeit Electronic Parts: Avoidance, Detection, Mitigation, and Disposition - Distributors", "SAE AS6171 Test Methods Standard; General Requirements, Suspect/Counterfeit EEE Parts (and slash sheets)", "IDEA-STD-1010 Acceptability of Electronic Components Distributed in the Open Market", "MIL-STD-883 Method 2015 Resistance to Solvents", "DFARS 252.246-7007 and 252.246-7008"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Counterfeit electronic component inspection — authenticate open-market parts before they hit the board

**Goal:** decide, with documented evidence, whether a lot of electronic components bought outside the authorized (franchised) channel is authentic, suspect, or confirmed counterfeit.

## 1. Plan the test level by risk

The first control is sourcing: buy from the OCM or authorized distributors (SAE AS5553 for OEMs, AS6081 for distributors, AS6496 for authorized distribution). When you cannot, AS6171 sets a risk-based test selection: part criticality (e.g., flight-safety vs. commercial), supplier history, part type (complex ICs carry more risk than passives), and obsolescence. Higher risk = more tests and larger samples. Record lot/date codes, quantity and the supplier's C of C and traceability back to the OCM.

Get a **golden sample** (known-authentic part from the same OCM, ideally same date code range) or at minimum the OCM datasheet, package drawing and marking specification. Without a reference, many findings are inconclusive.

## 2. Packaging and documentation

- Moisture barrier bag, humidity indicator card, desiccant, MSL label, ESD bag, reel labels: fonts, barcodes (decode them; do part number, quantity and date code agree with the label?), OCM logo quality.
- Mixed date codes or lot codes within one reel, or a date code later than the part's EOL announcement, are red flags.

## 3. External visual inspection (EVI)

Under 10-40x stereo microscope, sample per AS6171 / IDEA-STD-1010 (often 100% of a small lot, or a defined sample of a large one):
- Marking: font, logo, alignment, laser vs. ink, pin-1 indicator, consistency across the sample vs. golden sample.
- Body: sanding marks or texture differing between top and sides, mould cavity/ejector pin marks filled or inconsistent, ghost markings.
- Leads/balls: re-tinning, scratches, bent and re-straightened leads, oxidation, solder on leads of "new" parts, non-coplanarity, BGA ball size/shape inconsistency (reballing).

## 4. Marking permanency and resurfacing tests (destructive to the sample)

- **Resistance to solvents** (adapted from MIL-STD-883 Method 2015): swab the marking with acetone, then a 3:1 mineral spirits/isopropyl alcohol mix. Ink marking that smears is suspect (laser marking will not, so this test is weak against laser remarks).
- **Blacktop / resurfacing test:** apply a heated aggressive solvent such as Dynasolve 750 (or 1-methyl-2-pyrrolidinone) to the top surface per the test procedure in use. A coating that softens, peels, or reveals underlying old marking or sanding means the part was resurfaced. Check the solvent's compatibility with the genuine mould compound first using the golden sample. Use a fume hood and the SDS controls.
- **Scrape test:** a scalpel scrape at the edge shows a coating layer of different colour/texture.

## 5. X-ray (non-destructive, sample or 100%)

Compare die size, die attach, bond wire count/routing and lead frame shape against the golden sample. Mixed die sizes within a lot, missing or broken bond wires, or no die at all are decisive. Keep dose low for sensitive memory parts.

## 6. XRF

Measure lead finish composition: an RoHS/matte-Sn part showing Sn-Pb (or vice versa) contradicts the OCM datasheet, indicating re-tinning or mislabelled parts. Note tin-lead re-tinning of military parts may be legitimate if documented by the buyer.

## 7. Decapsulation and die verification

Chemical (fuming nitric/sulfuric acid, done by trained staff in a proper acid hood) or laser decap of a small sample. Inspect die markings: OCM logo, mask set/part ID, copyright year. A die from a different manufacturer or a lower-grade/different part is confirmed counterfeit.

## 8. Electrical tests

Curve trace (pin-to-pin I-V signature vs. golden sample) is cheap and catches dead or different dies. Full functional / parametric testing at temperature is needed for grade fraud (commercial sold as military).

## 9. Disposition and reporting

Quarantine suspect parts; never return them to the supplier for refund in a way that lets them re-enter the market. Classify: authentic / suspect / confirmed counterfeit with evidence package (photos, X-ray images, XRF data). US defence contractors must report to GIDEP (DFARS 252.246-7007/-7008; check current clause text and deadlines); industry databases such as ERAI accept reports too.

## Gotchas

- Absence of evidence is not authentication: passing EVI and X-ray only lowers risk.
- OCMs legitimately change fabs, die shrinks and marking styles; a mismatch against an old golden sample needs OCM confirmation.
- Laser-remarked parts with no blacktop pass solvent tests; rely on X-ray, decap and electrical.
- One lot can mix authentic and fake parts; sample across every reel/tube.

## Verify

- [ ] Supplier paperwork, lot/date codes and traceability are recorded.
- [ ] Golden sample or OCM reference data was used for every comparison.
- [ ] EVI, solvent/blacktop, X-ray and XRF results are photographed and filed.
- [ ] Decap die marking matches OCM and part number on sampled units.
- [ ] Suspect material is quarantined and reported (GIDEP/ERAI) where required.
