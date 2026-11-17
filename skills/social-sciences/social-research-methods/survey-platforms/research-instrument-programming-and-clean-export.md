---
id: social-sciences.social-research-methods.survey-platforms.research-instrument-programming-and-clean-export
name: research-instrument-programming-and-clean-export
category: social-sciences
field: social-research-methods
product: survey-platforms
tags: [survey-platforms, qualtrics, redcap, limesurvey, survey-programming, survey-flow, branching-logic, display-logic, skip-logic, randomisation, randomizer, embedded-data, piping, quotas, attention-checks, bot-detection, recaptcha, data-dictionary, longitudinal-surveys, panel-waves, survey-experiments, vignette-experiments, conjoint, test-responses, data-export, spss-export, prolific, mturk, irb-versioning]
level: practitioner
status: draft
description: "Program a research survey in Qualtrics, REDCap or LimeSurvey: logic, recorded randomisation for experiments, quotas, quality checks, testing, and an export that keeps codes and labels."
sources: ["Qualtrics Support documentation (Survey Flow, Randomizer, Quotas)", "REDCap documentation and training videos (Vanderbilt)", "LimeSurvey Manual (manual.limesurvey.org)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Survey platforms for research — program, test, export cleanly

**Goal:** the fielded instrument matches the approved questionnaire exactly, every
experimental assignment is recorded, and the export can be analysed without
reverse-engineering codes.

Commercial market-research fielding (panel quotas, incidence, invoicing) is covered in
sales-marketing.market-research-consumer-insights.survey-platforms.programming-logic-quotas-and-panel-fielding.

## 1. Pick the platform by data and governance
| Need | Usually |
|---|---|
| Identifiable health or sensitive data, longitudinal follow-ups, institution-hosted | **REDCap** (free to member institutions, hosted locally; audit trail) |
| Complex experiments, rich design, institutional licence | **Qualtrics** |
| Open source, self-hostable, multilingual, budget-limited | **LimeSurvey** |
Confirm with your ethics approval where data are stored (country, server) before choosing.

## 2. Program from a frozen spec
Number every item in the source questionnaire and use the **same names** as variable names
(Qualtrics: question "export tag"; REDCap: field name in the data dictionary; LimeSurvey:
question code). Set **recode values** explicitly (1 = Strongly disagree … 5 = Strongly agree)
— Qualtrics assigns codes in creation order, so editing choices can leave gaps or reversed
codes.
- **REDCap:** build in the **Data Dictionary** CSV (field name, form, type, choices
  `1, Yes | 0, No`, branching logic `[consent] = '1'`, validation) and upload — faster and
  reviewable compared with the online designer.
- **LimeSurvey:** question groups, expression manager for conditions
  (`{q1.NAOK == "A1"}`); can import/export `.lss` structure files for versioning.

## 3. Logic and randomisation
- Use display/skip/branching logic for routing; avoid hiding questions with CSS.
- **Experiments:** in Qualtrics, put conditions in a Survey Flow **Randomizer** with
  "Evenly Present Elements", and set an **Embedded Data** field in each branch
  (`condition = A`) so assignment is in the data, not inferred later. Randomised choice or
  block order: export "display order" variables. REDCap has no built-in randomizer for
  surveys beyond its trial randomisation module (allocation tables uploaded in advance) —
  check your instance's configuration.
- **Conjoint/vignette:** generate profiles with a tool (e.g. a JavaScript or pre-generated
  design) and store each displayed attribute level as embedded data.
- **Piping** previous answers into question text — test with empty answers.

## 4. Quotas and sample sources
Quotas on screening variables close cells once full; decide whether over-quota respondents
are screened out with a message and a redirect code (panels such as Prolific require a
completion/screen-out URL or code). Pass panel IDs in via URL parameters into embedded data;
never ask participants to type them.

## 5. Data quality built in
- Attention or instructed-response items (1–2, pre-registered exclusion rules).
- Bot/fraud checks: CAPTCHA, duplicate detection (Qualtrics has fraud-detection options in
  some licences), honeypot hidden questions, open-text review.
- Record timing (page timers) to flag speeders — set the threshold before seeing outcomes.
- Avoid forced responses on sensitive items; ethics committees often require "prefer not to say".

## 6. Testing before launch
1. Click through every path (each logic branch, each experimental condition) on desktop
   and phone.
2. Generate test responses (Qualtrics "Generate Test Responses"; REDCap test records) and
   **analyse them**: check every variable appears, codes are right, randomisation is balanced.
3. Delete test data or mark it; keep the platform version matching the ethics-approved
   documents and log any amendment.

## 7. Export
Export with numeric values *and* labels (SPSS `.sav` keeps both; REDCap offers SPSS/Stata/R
scripts with the CSV). Keep the raw export untouched; clean in scripts
(social-sciences.social-research-methods.statistical-software.reproducible-analysis-in-spss-r-and-stata).

## Gotchas
- Editing a live survey can break export columns or recodes mid-fieldwork; duplicate and
  version instead.
- Default "anonymous link" settings may still record IP addresses and location — switch
  off if consent promised anonymity.
- Back button and "save and continue later" interact badly with randomisation; test them.

## Verify
- [ ] Variable names and codes match the approved questionnaire.
- [ ] Each experimental assignment and display order is a column in the export.
- [ ] All paths tested on two devices; test responses analysed and removed.
- [ ] Data quality checks and exclusion rules defined before launch.
- [ ] Anonymity settings match the consent text.

*Draft: menu names and fraud features vary by licence and version; confirm in your instance.*
