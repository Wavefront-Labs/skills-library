---
id: health-medicine.public-health.community-health-assessment.needs-assessment-indicators-and-priority-setting
name: needs-assessment-indicators-and-priority-setting
category: health-medicine
field: public-health
product: community-health-assessment
tags: [public-health, community-health-assessment, health-needs-assessment, hna, jsna, joint-strategic-needs-assessment, chna, community-health-needs-assessment, chip, mapp, health-indicators, fingertips, county-health-rankings, life-expectancy, healthy-life-expectancy, dalys, avoidable-mortality, deprivation, imd, health-inequalities, social-determinants, small-area-estimation, asset-mapping, stakeholder-consultation, priority-setting, hanlon-method, pearl, multi-criteria-decision-analysis]
level: practitioner
status: gated
description: "Community health assessment: scoping, indicator selection and interpretation, inequality analysis, community voice and asset mapping, and transparent priority setting (Hanlon/MCDA)."
sources: ["https://www.irs.gov/charities-non-profits/community-health-needs-assessment-for-charitable-hospital-organizations-section-501r3", "https://www.ecfr.gov/current/title-26/section-1.501(r)-3"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Needs assessment, indicators and priority setting

> General professional reference. Statutory requirements (e.g. JSNA duties in England,
> CHNA requirements for US non-profit hospitals) and data sources vary by country.

**Goal:** produce an honest picture of a population's health needs, who carries
them, and what the community and services can do — ending in priorities a board can
defend.

## 1. Scope it first
- Population (geography, group, setting), the question (whole-population profile vs
  topic-specific HNA, e.g. mental health of young people), decision it informs,
  timeline, and governance (who signs it off).
- Choose a framework: **MAPP** (US local public health systems) (gated: unconfirmed, source is paywalled or blocked), JSNA guidance (England), or the
  NICE health needs assessment guide (gated: unconfirmed, source is paywalled or blocked). Steering group with community members, not just
  officers.

## 2. Assemble indicators
Cover the outcome–determinant chain:
| Domain | Examples |
|---|---|
| Demography | age structure, ethnicity, migration, projections |
| Outcomes | life expectancy, healthy life expectancy, infant mortality, avoidable/premature mortality, DALYs |
| Morbidity | disease prevalence (registers, surveys, modelled estimates) |
| Behaviours | smoking, physical activity, alcohol, diet |
| Wider determinants | deprivation (IMD/ADI), housing, employment, education, air quality, crime |
| Services | access, uptake (screening, immunisation), outcomes, gaps |
- Sources: national profiles (e.g. Fingertips, County Health Rankings), vital
  statistics, registers, surveys, primary care data, service data.
- For each indicator record: definition, source, period, numerator/denominator, CI,
  comparator, trend.

## 3. Interpret carefully
- **Compare** with region/nation and statistical neighbours; use **age-standardised**
  rates (see
  `health-medicine.public-health.applied-epidemiology.study-design-measures-of-association-and-bias-appraisal`).
- Show **CIs**; with small areas use funnel plots rather than league tables, and
  pooled years.
- **Trend** and **inequality gradient** (by deprivation quintile, ethnicity, sex,
  disability) matter more than a single snapshot; slope index of inequality where
  possible.
- Watch for data gaps: groups invisible in routine data (homeless, Gypsy/Traveller,
  undocumented migrants, LGBTQ+ populations) need targeted primary data.

## 4. Community voice and assets
- Qualitative input: surveys, focus groups, interviews, community conversations;
  report what people said in their words alongside numbers.
- **Asset mapping**: organisations, spaces, networks, skills that can be built on.
- Stakeholder consultation with services, voluntary sector, elected members.

## 5. Priority setting — make it explicit
- Agree criteria **before** scoring: size of problem, severity, inequality, trend,
  effectiveness and feasibility of interventions, cost, community concern, alignment
  with strategy.
- Methods: **Hanlon** (basic priority rating, then a PEARL
  feasibility screen — propriety, economics, acceptability, resources, legality) (gated: unconfirmed, source is paywalled or blocked),
  simple weighted scoring, or formal **MCDA**; nominal group technique for
  consensus.
- Document scores and dissent; sensitivity-check weights.

## 6. Outputs and follow-through
- Short executive summary with top priorities, then topic chapters and a data annex.
- Feed into a **community health improvement plan** with owners, actions and
  indicators; refresh on a cycle (e.g. a US charitable hospital facility must have conducted a CHNA in the current or one of the two preceding taxable years, 26 CFR 1.501(r)-3(a)).

## Gotchas
- Data dump with no "so what".
- Priorities that simply mirror existing services.
- Ranking areas without CIs, stigmatising neighbourhoods on noisy data.
- Small-number disclosure: suppress per rules.

## Verify
- [ ] Scope and decision-maker defined.
- [ ] Each indicator has source, period, CI and comparator.
- [ ] Inequality analysis by at least deprivation and one protected characteristic.
- [ ] Community input included and reported.
- [ ] Priority criteria agreed up front and scoring documented.

## Checked

- Date checked: 2026-10-25. Jurisdiction: United States (CHNA rule); England (JSNA mentioned generally).
- Sources read: IRS CHNA page and 26 CFR 1.501(r)-3 on eCFR.
- Confirmed: The three-year CHNA cycle and the implementation-strategy adoption timing (15th day of the fifth month after year end).
- Corrected or removed: The "every 3 years" wording was replaced by the regulation text (current or either of the two preceding taxable years).
- Gated: MAPP, the NICE HNA guide and the Hanlon/PEARL description. The NACCHO page returned 403, the gov.uk JSNA page returned 404 and NICE returned 403.

Method: documentation only; no commands were run.
