---
id: health-medicine.pathology-and-laboratory-medicine.transfusion-medicine-laboratory.antibody-identification-crossmatch-and-reaction-workup
name: antibody-identification-crossmatch-and-reaction-workup
category: health-medicine
field: pathology-and-laboratory-medicine
product: transfusion-medicine-laboratory
tags: [transfusion-medicine-laboratory, blood-bank, blood-transfusion-laboratory, pathology-and-laboratory-medicine, immunohaematology, abo-grouping, rhd-typing, group-and-screen, type-and-screen, antibody-screen, antibody-identification, antibody-panel, rule-out, dat, direct-antiglobulin-test, iat, crossmatch, electronic-crossmatch, antigen-negative-blood, component-selection, irradiated, cmv-negative, massive-haemorrhage-protocol, transfusion-reaction, haemolytic-transfusion-reaction, trali, taco, wrong-blood-in-tube, haemovigilance, shot]
level: practitioner
status: draft
description: "Blood bank essentials: group and screen, systematic antibody identification, crossmatch choice, special-requirement components, massive-haemorrhage support and transfusion-reaction investigation."
sources:
  - "AABB Technical Manual, 21st ed. (2023) and AABB Standards for Blood Banks and Transfusion Services"
  - "British Society for Haematology. Guidelines for pre-transfusion compatibility procedures in blood transfusion laboratories (2012 and updates)"
  - "BSH guidelines on the investigation and management of acute transfusion reactions (2023)"
  - "Serious Hazards of Transfusion (SHOT) Annual Reports, UK haemovigilance scheme"
  - "CDC National Healthcare Safety Network Hemovigilance Module surveillance protocol (case definitions)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Antibody identification, crossmatch and transfusion-reaction workup

*General professional reference. Procedures, sample-validity rules and special-requirement criteria follow your national standards (e.g. AABB, BSH) and laboratory SOPs; component-dosing decisions belong with the clinical team and local transfusion guidelines.*

**Goal:** issue compatible blood safely and quickly, identify every clinically
significant antibody, and investigate reactions so the next transfusion is safe. Most
serious transfusion harm still comes from **identification errors**, not serology.

## 1. Sample and identity
- Positive patient identification at sample collection; hand-labelled at the bedside
  with required identifiers. Mismatch = reject; never relabel.
- Many systems require **two separate samples** (or a historical group) before issuing
  group-specific red cells, to catch wrong-blood-in-tube (WBIT) errors.
- Sample validity: commonly 72 hours if transfused or pregnant in the last 3 months
  (local rules vary), because new antibodies can form.

## 2. Group and screen
- **ABO** forward (cells) and reverse (plasma) groups must agree; discrepancies
  (weak subgroups, cold agglutinins, recent transfusion or stem-cell transplant,
  infants) are resolved before group-specific issue — give group O red cells meanwhile if urgent.
- **RhD** typing; weak/partial D handling per policy (matters for women of childbearing potential).
- **Antibody screen** by indirect antiglobulin test against two or three screening cells.

## 3. Antibody identification (systematic)
1. Run an extended panel (IAT ± enzyme), autocontrol/DAT.
2. **Rule out** antigens using cells that are non-reactive, preferably homozygous for
   the antigen (dosage: Kidd, Duffy, MNS, Rh).
3. Match the reaction pattern to remaining candidate antibodies.
4. Confirm: **rule of three** (commonly ≥ 3 antigen-positive reactive and ≥ 3 antigen-negative
   non-reactive cells for ~95% confidence) and **phenotype the patient** (should lack the antigen).
5. Consider multiple antibodies, high-incidence antibodies, warm autoantibodies (adsorption
   studies), and drug-related antibodies (e.g. anti-CD38 therapy interferes with IAT —
   DTT-treated cells; note the K antigen is destroyed by DTT).
- **Kidd antibodies** fall to undetectable and cause delayed haemolysis: record every
  antibody permanently and check history on every sample.
- Clinically significant antibodies (active at 37 °C/IAT) need **antigen-negative, IAT-crossmatched** units.

## 4. Crossmatch
- **Electronic (computer) crossmatch** allowed when the screen is negative, no antibody
  history, two concordant groups and a validated LIS.
- **Immediate-spin** confirms ABO compatibility; **IAT crossmatch** when antibodies are present.

## 5. Component selection
Group-compatible red cells, plasma and platelets; special requirements: **irradiated**
(transfusion-associated GvHD risk — e.g. certain transplant patients, purine-analogue therapy,
intrauterine/neonatal exchange, HLA-matched or directed donations), **CMV-safe**, HLA-matched
platelets for refractory patients, washed components for severe allergic reactions or IgA deficiency with antibodies.
Flags must live in the LIS so they are enforced automatically.

## 6. Massive haemorrhage support
Fixed-ratio packs per protocol, emergency group O units (O RhD-negative for females of
childbearing potential where stock allows), switch to group-specific as soon as group
known, near-patient tests (viscoelastic, fibrinogen) to guide; keep the communication
line open and track units issued vs returned.

## 7. Transfusion reaction investigation
Clinical team stops the transfusion, keeps the line, checks identity at the bedside,
and sends the bag and post-transfusion samples. Laboratory:
- **Clerical check** first (bag, labels, patient ID) — WBIT/wrong-unit is the most dangerous cause.
- Repeat ABO/RhD pre and post, **DAT** on post sample, haemolysis markers (visual plasma
  check, bilirubin, LDH, haptoglobin), antibody screen on both samples.
- Culture the bag if fever/sepsis suspected (bacterial contamination, more common in platelets).
- Differential: acute haemolytic, febrile non-haemolytic, allergic/anaphylactic, **TRALI**
  (within 6 h, hypoxaemia, bilateral infiltrates, no circulatory overload), **TACO**
  (overload, raised BNP may help), septic, delayed haemolytic (days later).
- Report to haemovigilance (e.g. SHOT, NHSN) and blood supplier per requirements.

## Gotchas
- A historical antibody not on the current screen is still clinically significant.
- Anti-CD38 (daratumumab) panreactivity mimics a pan-agglutinin — know the patient's drugs.
- Emergency group O release is safe for ABO, but not antigen-negative for known antibodies.

## Verify
- [ ] Sample identity and validity confirmed; two-sample rule met.
- [ ] ABO/RhD concordant; discrepancies resolved.
- [ ] Antibodies identified with rule-outs, rule of three and patient phenotype.
- [ ] Antigen-negative, crossmatched units for significant antibodies; special requirements flagged in LIS.
- [ ] Reactions investigated with clerical check, DAT and haemolysis screen; reported to haemovigilance.
