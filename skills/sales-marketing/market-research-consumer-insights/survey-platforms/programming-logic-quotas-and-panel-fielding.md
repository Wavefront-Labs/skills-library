---
id: sales-marketing.market-research-consumer-insights.survey-platforms.programming-logic-quotas-and-panel-fielding
name: programming-logic-quotas-and-panel-fielding
category: sales-marketing
field: market-research-consumer-insights
product: survey-platforms
tags: [survey-platforms, qualtrics, surveymonkey, google-forms, alchemer, typeform, survey-programming, survey-flow, display-logic, skip-logic, branch-logic, randomizer, embedded-data, url-parameters, quotas, panel-sourcing, panel-marketplace, cint, dynata, prolific, redirects, terminate, overquota, soft-launch, data-export, spss-sav, csv]
level: practitioner
status: draft
description: "Program and field a survey on Qualtrics, SurveyMonkey or Google Forms: logic, randomisation, quotas, panel redirects with respondent IDs, soft launch, and clean exports for analysis."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Programming, logic, quotas and panel fielding

**Goal:** turn a questionnaire into a live survey that routes correctly, fills
the right quotas, pays the panel only for good completes, and exports clean.
Menu names reflect **Qualtrics**, **SurveyMonkey** and **Google Forms** as
commonly configured; **status draft:** UIs change and paid-plan features vary —
check the current help pages for your licence tier.

## 1. Pick the platform for the job
- **Google Forms** — free, fast, internal or customer lists. Section branching
  only ("Go to section based on answer"); no quotas, weak randomisation. Fine for
  simple feedback, not for panel studies.
- **SurveyMonkey** — easy, skip/display logic, randomisation and quotas on higher
  plans; its own Audience panel.
- **Qualtrics** (or Alchemer, Decipher/Forsta for agencies) — full survey flow,
  embedded data, quotas, complex piping and randomisers; standard for panel work.

## 2. Program it (Qualtrics terms; others similar)
- **Blocks** for each questionnaire section; **Survey flow** orders blocks, sets
  **Embedded data**, **Randomizer** elements (e.g. show 1 of 3 concepts, evenly
  present), **Branch** elements, and **End of survey** elements.
- **Display logic** on questions (show if…); **skip logic** to jump; prefer
  branches in survey flow for anything structural — easier to audit.
- **Choice randomisation** within lists (anchor "Other"/"None" at the bottom).
- **Piping** previous answers ("You said you use ${q://QID5/ChoiceGroup/SelectedChoices}").
- **Validation**: force response where needed, numeric ranges, sum checks.
- Name questions meaningfully (Q_AGE, Q_PI_CONCEPT) — export column names come from these.
- Recode values so scales export as numbers in the intended order (Recode values
  option per question).

## 3. Quotas
- Define quotas for the screener variables (e.g. age × gender, region, user type),
  set targets 5–10% above need on hard cells, and the action when full: end
  survey with **overquota** redirect.
- Use **embedded data** for quota groups computed from several answers.
- Monitor fill daily; tell the panel which cells are lagging.

## 4. Panel sourcing and redirects
- Panels/marketplaces (Cint, Dynata, Prolific, PureSpectrum, etc.) send respondents
  to your link with an ID parameter, e.g. `...?rid=[%RID%]` — the exact placeholder
  is set by the panel.
- Capture it: add `rid` as **embedded data at the top of survey flow** (same name
  as the URL parameter).
- Three end redirects back to the panel, each carrying the ID:
  **complete**, **terminate** (screened out), **overquota**, e.g.
  `https://panel.example/complete?rid=${e://Field/rid}`. Some panels add a
  security hash — follow their spec.
- Agree incidence rate (IR) and length of interview (LOI) up front; price depends on both.

## 5. Test and soft launch
- Generate test responses (Qualtrics: *Tools › Generate test responses*) to check
  routing and quotas, then **delete test data** before launch.
- Click through every path on a phone.
- **Soft launch** ~10% of sample; check LOI, IR, drop-off point, open-end quality,
  quota fill. Fix, then full launch.

## 6. Export for analysis
- CSV with **numeric values** (not choice text) plus a separate labels file, or
  **SPSS .sav** which carries value labels. Qualtrics: *Data & Analysis › Export &
  Import › Export data*.
- Export *after* applying exclusion filters you've documented (speeders,
  attention-check fails); keep the raw full export too.
- Check row count = completes reported by the panel; reconcile IDs before paying.

## Gotchas
- Editing a live survey's questions can shift export columns or recodes; copy the survey for big changes.
- Mobile rendering of matrix questions is poor — use mobile-friendly layouts.
- Personal data in embedded fields falls under privacy law; collect only what you need.
- Forgetting the overquota redirect = paying for people you didn't want.

## Verify
- [ ] Every path tested on desktop and mobile; test data deleted.
- [ ] Quotas set with overquota action; fill monitored daily.
- [ ] Respondent ID captured and appended to all three redirects.
- [ ] Soft launch checked LOI, IR, drop-off and data quality.
- [ ] Export uses numeric codes/labels; counts reconciled with the panel.
