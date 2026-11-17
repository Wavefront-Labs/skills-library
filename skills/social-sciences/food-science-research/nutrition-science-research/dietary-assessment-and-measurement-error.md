---
id: social-sciences.food-science-research.nutrition-science-research.dietary-assessment-and-measurement-error
name: dietary-assessment-and-measurement-error
category: social-sciences
field: food-science-research
product: nutrition-science-research
tags: [nutrition-science-research, nutritional-epidemiology, dietary-assessment, food-frequency-questionnaire, ffq, 24-hour-recall, 24hr-recall, ampm, asa24, intake24, food-record, weighed-food-record, measurement-error, misreporting, under-reporting, doubly-labelled-water, recovery-biomarkers, urinary-nitrogen, energy-adjustment, residual-method, nci-method, usual-intake, regression-calibration, validation-study, goldberg-cutoff, food-composition-database]
level: advanced
status: draft
description: "Choose and run dietary assessment for nutrition research (FFQ, 24-h recall, food records), then handle measurement error: under-reporting, energy adjustment, usual-intake models and calibration."
sources:
  - "Willett, Nutritional Epidemiology (3rd ed., 2013)"
  - "NCI Dietary Assessment Primer (epi.grants.cancer.gov/dietary-assessment)"
  - "Subar et al. (2015), Addressing current criticism regarding the value of self-report dietary data, J. Nutrition"
  - "Kipnis et al. (2003), OPEN biomarker study, American J. Epidemiology"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dietary assessment and measurement error

**Goal:** measure what people eat well enough to answer a research question about diet
and health — and analyse the data knowing that every self-report method is wrong in
predictable ways. (Clinical dietetic assessment of individual patients belongs to
health-medicine.)

## 1. Match the instrument to the question
| Instrument | Captures | Strength | Weakness |
|---|---|---|---|
| **24-hour recall** (interviewer: USDA AMPM; self-administered: ASA24, Intake24) | Detailed intake for one day | Least biased self-report; open-ended | Large day-to-day variation; needs ≥ 2 non-consecutive days for usual intake |
| **Food record / diary** (estimated or weighed) | Intake as eaten, 3–7 days | No memory reliance | Reactivity — people eat differently (and simpler) when recording; burden |
| **Food-frequency questionnaire (FFQ)** | Habitual intake over months/a year | Cheap at scale; ranks individuals | Poor absolute intake; fixed food list must suit the population |
| **Screeners** | One food group (e.g. fruit & veg) | Very short | Narrow |
| **Biomarkers** | Objective exposure | No self-report bias | Few true recovery markers; cost |

Rules of thumb: **population means/distributions** → repeated 24-h recalls; **ranking
individuals in a large cohort** → FFQ (ideally calibrated against recalls/biomarkers);
**controlled feeding trials** → weighed provision plus compliance biomarkers.

## 2. Field practice
- Use or adapt an FFQ validated **in your population**; a US FFQ in another food culture
  misses staple foods and portion norms.
- Recall days should cover weekdays and weekend days, unannounced where possible.
- Portion-size aids (photo atlases, household measures) matter more than people think.
- Code against an appropriate, current **food composition database** (e.g. FNDDS/FoodData
  Central in the US, national tables elsewhere) and document the version.

## 3. The measurement-error problem
- **Energy under-reporting** is systematic, larger in people with higher BMI, and
  differs by food (snacks and sweets under-reported more). Recovery-biomarker studies
  (doubly labelled water for energy, urinary nitrogen for protein, urinary
  potassium/sodium) show FFQs under-report energy substantially; recalls less so.
- Random error **attenuates** diet–disease associations toward the null (and can
  distort them in multivariable models).

## 4. Analysis tools
- **Energy adjustment**: residual method or nutrient density, so you study diet
  composition rather than total amount eaten. Choose and justify one.
- **Identifying implausible reporters**: Goldberg cut-off (EI:BMR) or predicted-energy
  methods; report sensitivity analyses with and without them rather than silently dropping.
- **Usual intake**: from ≥ 2 recalls on at least a subsample, use the NCI method (SAS
  macros) or MSM/SPADE to remove within-person variation when estimating the
  distribution or the share below a requirement.
- **Regression calibration**: in a calibration substudy, regress the reference measure
  (recall/biomarker) on the FFQ and use it to de-attenuate associations.

## Gotchas
- Never estimate prevalence of inadequate intake from a single 24-h recall — the
  distribution is too wide.
- Supplements are often missed; ask separately.
- Changing database versions mid-study changes nutrient values silently.
- Uncertain: specific under-reporting magnitudes vary by population and instrument; cite
  biomarker studies close to yours.

## Verify
- [ ] Instrument choice matches the estimand (mean, distribution or ranking).
- [ ] FFQ validated in the study population, or calibration substudy planned.
- [ ] ≥ 2 non-consecutive recalls on at least a subsample for usual-intake modelling.
- [ ] Energy adjustment method stated; misreporting sensitivity analysis done.
- [ ] Food composition database and version documented.
