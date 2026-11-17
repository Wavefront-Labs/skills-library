---
id: health-medicine.oncology.systemic-therapy.systemic-anticancer-therapy-toxicity-management
name: systemic-anticancer-therapy-toxicity-management
category: health-medicine
field: oncology
product: systemic-therapy
tags: [sact, chemotherapy, immunotherapy, targeted-therapy, checkpoint-inhibitor, irae, immune-related-adverse-events, ctcae, toxicity-grading, dose-modification, dose-delay, dose-reduction, neutropenia, febrile-neutropenia, g-csf, peripheral-neuropathy, mucositis, colitis, pneumonitis, hepatitis, endocrinopathy, recist, irecist, response-assessment, oncology-pharmacy, ukons-triage]
level: advanced
status: draft
description: "Grade and manage toxicity from chemotherapy, targeted agents and checkpoint inhibitors using CTCAE, apply dose holds/reductions, and assess response with RECIST."
sources: ["NCI Common Terminology Criteria for Adverse Events (CTCAE, current version)", "ESMO and ASCO clinical practice guidelines on management of immune-related adverse events", "RECIST 1.1 and iRECIST response criteria publications", "DeVita, Hellman, and Rosenberg's Cancer: Principles and Practice of Oncology (textbook)", "UKONS Oncology/Haematology 24-Hour Triage Tool"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

# Systemic anticancer therapy toxicity management

**Goal:** recognise, grade and act on treatment toxicity early enough to keep the patient
safe and on effective therapy, and judge whether the treatment is working.

## 1. Before each cycle: the pre-treatment check
- Confirm **regimen, intent and cycle number** against the protocol; dose by current
  weight/BSA (or AUC for carboplatin) with verified calculations and a second check.
- Review bloods against the protocol's thresholds (typically neutrophils, platelets,
  renal and liver function; regimen-specific thresholds vary, so use the local protocol).
- Ask structured symptom questions since last cycle and **grade each toxicity**.

## 2. Grade with CTCAE
NCI CTCAE grades most adverse events on a common scale:

| Grade | General meaning |
|---|---|
| 1 | Mild; asymptomatic or mild symptoms; intervention not indicated |
| 2 | Moderate; minimal/local intervention; limits instrumental ADLs |
| 3 | Severe or medically significant; hospitalisation may be indicated; limits self-care |
| 4 | Life-threatening; urgent intervention |
| 5 | Death related to the adverse event |

Each event has its own defined criteria (for example diarrhoea by stool frequency over
baseline); look them up rather than estimating.

## 3. Act on the grade
**Cytotoxics and targeted agents (general pattern, protocol overrides):**
- Grade 1: continue, supportive care.
- Grade 2: supportive care; hold or continue per drug-specific guidance.
- Grade 3–4: hold until recovery to grade 1 or baseline, then **dose-reduce** per
  protocol levels; consider G-CSF prophylaxis after febrile neutropenia if intent warrants.
- Cumulative toxicities (oxaliplatin/taxane neuropathy, anthracycline cardiotoxicity,
  bleomycin lung) need tracking across cycles and lifetime-dose limits.

**Checkpoint inhibitors (anti-PD-1/PD-L1, anti-CTLA-4):** immune-related adverse
events (irAEs) can affect any organ, appear months into or after treatment, and are
managed differently:
- Grade 1: usually continue with close monitoring (exceptions exist, e.g. some
  neurological or cardiac events).
- Grade 2: hold; corticosteroids commonly started per guideline.
- Grade 3–4: hold or permanently discontinue; high-dose corticosteroids; involve organ
  specialist; steroid-refractory cases may need further immunosuppression (for example
  infliximab for colitis, avoided in hepatitis). Steroid doses and second-line agents:
  per current ESMO/ASCO guidance and local protocol.
- **Endocrinopathies** (thyroiditis, hypophysitis, adrenal insufficiency, diabetes) are
  usually managed with hormone replacement and often do not require stopping treatment.
- **Myocarditis** is rare but can be fatal: troponin and ECG with any cardiac symptom.

## 4. Triage between cycles
Use a structured telephone triage tool (for example the UKONS 24-hour triage tool) so
any patient with fever, diarrhoea, breathlessness or other red flags is graded and seen
on time. Any febrile patient on chemotherapy is treated as **neutropenic sepsis until
proven otherwise** (see the oncologic-emergencies skill).

## 5. Response assessment
- **RECIST 1.1:** measure up to 5 target lesions (max 2 per organ) at baseline.
  Complete response = disappearance; partial response = at least 30% decrease in sum of
  diameters; progressive disease = at least 20% increase (and at least 5 mm absolute)
  or new lesions; stable disease otherwise.
- Immunotherapy can cause **pseudoprogression**; iRECIST requires confirmation of
  progression on repeat imaging if the patient is clinically stable.
- Lymphoma uses Lugano/Deauville PET criteria, not RECIST.

## Gotchas
- Diarrhoea on immunotherapy is colitis until proven otherwise; loperamide alone can mask it.
- Steroids for irAEs need slow tapers; early stopping causes flares. Consider PJP
  prophylaxis and glucose monitoring with prolonged steroids.
- Drug interactions with oral targeted agents (CYP3A4 inducers/inhibitors, acid
  suppression) are common; check each new prescription.
- Grade the toxicity against baseline, not against normal.

## Verify
- [ ] Regimen, dose calculation and pre-treatment bloods checked against protocol.
- [ ] Every toxicity graded with CTCAE and action documented (continue/hold/reduce/stop).
- [ ] irAEs managed per current guideline with organ specialist where grade 3–4.
- [ ] Response assessed with the correct criteria (RECIST 1.1, iRECIST, Lugano).
- [ ] Patient has a 24-hour contact number and knows the red-flag symptoms.
