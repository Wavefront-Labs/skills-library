---
id: social-sciences.communication-studies.interpersonal-organisational-communication-research.interaction-coding-diary-studies-and-communication-audits
name: interaction-coding-diary-studies-and-communication-audits
category: social-sciences
field: communication-studies
product: interpersonal-organisational-communication-research
tags: [interpersonal-organisational-communication-research, interpersonal-communication, organisational-communication, interaction-coding, behavioural-observation, observational-coding, sequential-analysis, lag-sequential-analysis, dyadic-data, apim, actor-partner-interdependence-model, diary-study, daily-diary, experience-sampling, esm, ema, multilevel-modelling, within-person, communication-network, sociometric-survey, ona, organisational-network-analysis, communication-audit, ica-audit, focus-groups, employee-survey, noldus-observer, datavyu, boris]
level: practitioner
status: draft
description: "Researching communication in relationships and workplaces: behavioural interaction coding, daily diary/ESM designs with multilevel models, network surveys and communication audits."
sources: ["Bakeman & Quera, Sequential Analysis and Observational Methods for the Behavioral Sciences (2011)", "Kenny, Kashy & Cook, Dyadic Data Analysis (2006)", "Bolger & Laurenceau, Intensive Longitudinal Methods (2013)", "Downs & Adrian, Assessing Organizational Communication (2004)", "Monge & Contractor, Theories of Communication Networks (2003)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interaction coding, diary studies and communication audits

**Goal:** capture how people communicate in couples, families, teams and organisations
— moment-to-moment behaviour, day-to-day patterns, and organisation-wide flows.

## 1. Behavioural interaction coding
- **Elicit interaction:** lab conflict-discussion or problem-solving tasks (e.g.
  10 minutes on a disagreement topic), recorded meetings, or naturalistic recordings.
- **Coding system:** use an established one where it fits (couple, parent–child and
  group-interaction schemes exist) or develop one like a content codebook — see
  social-sciences.communication-studies.content-analysis.codebook-coder-training-and-intercoder-reliability.
- **Unit:** event-based (each turn/utterance), interval-based (every 10–30 s), or
  global ratings of the whole interaction. Event coding supports sequence analysis;
  global ratings are cheaper and often as predictive.
- Software: BORIS (free), Datavyu (free), Noldus Observer XT (commercial) — timestamped
  coding linked to video.
- **Sequential analysis:** does partner B's withdrawal follow A's criticism more than
  chance? Lag-sequential analysis with transitional probabilities and adjusted
  residuals or Yule's Q (Bakeman & Quera).
- Reliability: κ per code and for unitising (agreement on where units start).

## 2. Dyadic data
Partners' scores are interdependent — never analyse them as independent cases.
Use the **Actor–Partner Interdependence Model (APIM)**: your outcome predicted by your
own and your partner's predictors, estimated via multilevel models or SEM; decide
whether members are **distinguishable** (e.g. by role) or not.

## 3. Diary and experience-sampling studies
- **Daily diary:** one short survey per evening for 1–3 weeks. **ESM/EMA:** several
  prompts per day (random or signal-contingent) on phones.
- Keep surveys to a few minutes; 7–14 days is a common daily-diary length; expect
  compliance to drop over time — monitor it live and remind.
- Analyse with **multilevel models** (days nested in persons): separate within-person
  effects (on days when I communicate more with my manager, am I less stressed?) from
  between-person differences by **person-mean centring** predictors.
- Gotcha: lagged within-person effects need consistent spacing; time trends need
  controlling.

## 4. Organisational communication networks
- **Sociometric survey:** roster of staff; "whom do you go to for advice / work
  information?" with frequency. Response rates must be high (missing nodes distort
  network measures); full roster recall beats free recall.
- Measures: centrality (degree, betweenness — brokers), density, silos between units.
- Digital trace alternatives (email/Slack metadata) require strict privacy agreements
  and should exclude content.

## 5. Communication audits
A structured diagnosis of an organisation's communication: interviews and focus
groups with leaders and staff, a survey (e.g. the ICA Audit Survey or Downs–Hazen
Communication Satisfaction Questionnaire), network analysis, review of channels and
documents, and observation of meetings. Deliver a report linking findings to
specific recommendations.
- Confidentiality is critical: report only aggregated results, set minimum group
  sizes (e.g. no breakdowns under 5–10 people), and agree upfront that management
  won't see identifiable data.

## Verify
- [ ] Coding unit, system and per-code reliability reported for interaction data.
- [ ] Dyadic interdependence modelled (APIM or equivalent).
- [ ] Diary compliance reported; within- and between-person effects separated.
- [ ] Network survey response rate high enough and roster-based.
- [ ] Audit confidentiality rules and minimum reporting sizes agreed in writing.
