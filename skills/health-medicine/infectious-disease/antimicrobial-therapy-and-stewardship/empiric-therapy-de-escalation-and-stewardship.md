---
id: health-medicine.infectious-disease.antimicrobial-therapy-and-stewardship.empiric-therapy-de-escalation-and-stewardship
name: empiric-therapy-de-escalation-and-stewardship
category: health-medicine
field: infectious-disease
product: antimicrobial-therapy-and-stewardship
tags: [antimicrobial-therapy-and-stewardship, infectious-disease, antimicrobial-stewardship, antibiotic-stewardship, empiric-therapy, directed-therapy, de-escalation, antibiogram, susceptibility, mic, breakpoints, eucast, clsi, esbl, mrsa, cre, carbapenemase, ampc, iv-to-oral-switch, antibiotic-time-out, duration-of-therapy, therapeutic-drug-monitoring, vancomycin, aminoglycosides, penicillin-allergy, start-smart-then-focus]
level: practitioner
status: draft
description: "Choose empiric antimicrobials from source, host and local antibiogram, read susceptibility reports, then de-escalate, switch IV to oral and stop on time via a 48-72 h review."
sources:
  - "Barlam TF et al. Implementing an Antibiotic Stewardship Program: IDSA/SHEA guidelines. Clin Infect Dis 2016"
  - "UK Health Security Agency. Start Smart - Then Focus: antimicrobial stewardship toolkit for inpatient care"
  - "CDC. Core Elements of Hospital Antibiotic Stewardship Programs (2019 and later updates)"
  - "EUCAST Expert Rules and Clinical Breakpoint Tables; CLSI M100 Performance Standards for Antimicrobial Susceptibility Testing"
  - "IDSA Guidance on the Treatment of Antimicrobial-Resistant Gram-Negative Infections (updated periodically)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Empiric therapy, de-escalation and stewardship

*General clinical/professional reference, not a substitute for independent clinical judgement. Drug choices, doses and durations must be checked against your current local formulary, antibiogram and guidelines.*

**Goal:** give the right drug early enough to save the patient, then narrow, switch and
stop it as soon as the evidence allows. Stewardship is not withholding antibiotics; it is
making every dose count.

## 1. Choosing empiric therapy — four inputs
1. **Likely source** — pneumonia, urinary, intra-abdominal, skin/soft tissue, CNS, line.
   The source defines the probable organisms; "broad cover for everything" is not a plan.
2. **Host and exposure risk** — prior resistant organisms (check the micro history for
   MRSA, ESBL, CRE, *Pseudomonas*), antibiotics in the last 90 days, healthcare contact,
   neutropenia, travel to high-resistance regions.
3. **Severity** — septic shock justifies broader initial cover and combination therapy;
   a stable patient can often wait hours for better data.
4. **Local antibiogram** — the hospital's (and ideally unit's) susceptibility rates. A
   drug with < ~80-90% local activity against the likely organism is a poor empiric
   choice for a sick patient (threshold is a common rule of thumb, not a standard).

Then the drug-level checks: allergy (clarify the actual reaction — most reported penicillin
allergies are not true IgE allergy; delabelling pathways exist), renal/hepatic function,
interactions (rifampicin, azoles, linezolid with serotonergic drugs), pregnancy, penetration
to the site (CNS, bone, prostate), and **source control** — no antibiotic drains an abscess.

## 2. Reading a susceptibility report
- S / I / R follow EUCAST or CLSI breakpoints; know which your lab uses. Under EUCAST,
  "I" means *susceptible, increased exposure* (use the high dose), not "intermediate, avoid".
- MIC values are not comparable across different drugs; a lower number does not mean a better drug.
- Suppressed (cascade) reporting is deliberate: the lab may hide broad agents when a narrow
  one works. Ask the lab rather than assuming resistance.
- Resistance phenotypes that change management: ESBL (avoid relying on piperacillin-tazobactam
  for serious infection per trial data; carbapenem typically preferred — verify current guidance),
  AmpC inducers (*Enterobacter*, *Klebsiella aerogenes*, *Citrobacter freundii* — third-generation
  cephalosporins can fail on therapy), carbapenemase type (KPC vs metallo — drives choice of
  newer agents), MRSA, VRE. Involve ID/microbiology for any carbapenemase producer.

## 3. The 48-72 hour antibiotic time-out
Every course gets a documented review with one of five decisions:
**stop** (no infection), **continue**, **narrow/de-escalate**, **IV-to-oral switch**, or **OPAT**.
- De-escalate to the narrowest agent active against the identified organism; stop anti-MRSA
  or anti-pseudomonal cover when cultures that would have found them are negative (e.g.
  MRSA nasal PCR negative has high negative predictive value for MRSA pneumonia).
- IV-to-oral when: clinically improving, afebrile, gut working, a highly bioavailable
  oral option exists (fluoroquinolones, linezolid, metronidazole, doxycycline, TMP-SMX), and
  the infection does not mandate IV (e.g. *S. aureus* bacteraemia, endocarditis, meningitis
  — though oral step-down evidence is growing; follow current guidance).
- Write a **stop date** at the start. Many modern trials support shorter courses
  (e.g. uncomplicated pneumonia, pyelonephritis, intra-abdominal infection with source
  control); check the current evidence for the specific syndrome.

## 4. Therapeutic drug monitoring
Vancomycin (AUC-guided dosing is now preferred over trough-only in many guidelines),
aminoglycosides, and some azoles (voriconazole, posaconazole) need levels. Dose and target
ranges vary by guideline and lab — use the local protocol and pharmacist.

## 5. Running a stewardship programme (the system view)
Core elements: leadership commitment, a physician + pharmacist lead, actions
(prospective audit and feedback, restricted agents needing approval, syndrome-specific
guidelines), tracking (days of therapy per 1,000 patient-days, *C. difficile* rates,
resistance trends), reporting back to prescribers, and education. Prospective audit with
feedback ("handshake stewardship") tends to be better received than pure restriction.

## Red flags — call ID / microbiology
Carbapenemase producer, *S. aureus* or *Candida* bacteraemia, any organism resistant to
all first-line agents, treatment failure despite "susceptible" result (think source, dose,
penetration, wrong bug), serious beta-lactam allergy limiting options.

## Gotchas
- A positive culture from a colonised site (sputum in a ventilated patient, catheter urine) is not proof of infection.
- Double anaerobic cover (metronidazole plus piperacillin-tazobactam or a carbapenem) is usually redundant.
- Nobody owns the stop date unless someone writes it down.

## Verify
- [ ] Empiric choice names source, host risk, severity and antibiogram rationale.
- [ ] Cultures sent before the first dose where feasible; source control considered.
- [ ] Allergy history clarified, not just copied.
- [ ] 48-72 h review documented with one of the five decisions.
- [ ] Stop date or review date written; TDM ordered where required.
- [ ] Doses checked against current local formulary and renal function.
