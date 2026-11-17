---
id: social-sciences.psychology.replication-open-science.registered-reports-and-osf-replication-workflow
name: registered-reports-and-osf-replication-workflow
category: social-sciences
field: psychology
product: replication-open-science
tags: [replication-open-science, open-science, psychology, replication, direct-replication, conceptual-replication, registered-report, stage-1, stage-2, in-principle-acceptance, preregistration, osf, open-science-framework, open-data, open-materials, reproducibility, many-labs, psychological-science-accelerator, qrps, p-hacking, harking, equivalence-testing, tost, small-telescopes, top-guidelines, codebook, fair-data]
level: practitioner
status: draft
description: "Run a replication or Registered Report: Stage 1 protocol, OSF project structure, data and code sharing, multi-lab coordination and how to judge whether it replicated."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Registered Reports and an OSF replication workflow

**Goal:** produce a study whose conclusions don't depend on decisions made after
seeing the data, with materials and data that let someone else reproduce it.

## 1. Choose the kind of replication
- **Direct (close) replication:** same materials, procedure and analysis, new sample.
  Tests whether the original finding holds. Contact the original authors for materials
  and ask them to review the protocol — reduces "you did it wrong" disputes later.
- **Conceptual replication:** different operationalisation of the same hypothesis.
  Tests generality — but a failure is ambiguous (was it the theory or the new method?).
- Document every unavoidable deviation (language, population, era) before collecting data.

## 2. Sample size for a replication
Original effects are usually inflated. Options:
- Power for a fraction of the original effect, or for a SESOI.
- **Small-telescopes approach** (Simonsohn 2015): roughly 2.5× the original n gives
  ~80% power to detect an effect the original study had only 33% power to find.
- Plan **equivalence tests (TOST)** so a null can be informative, not just "non-significant".

## 3. Registered Report pathway
1. **Stage 1:** submit introduction, methods, analysis plan, power analysis and pilot
   data to a journal offering RRs (the Center for Open Science keeps a list of
   participating journals).
2. Peer review on the question and method. **In-principle acceptance (IPA)** means the
   journal commits to publish regardless of results if you follow the protocol.
3. Register the accepted Stage 1 protocol (OSF Registries) — usually required.
4. Collect and analyse exactly as planned. Exploratory analyses are allowed in a
   clearly separated section.
5. **Stage 2:** submit results; review checks adherence and that conclusions follow.
Timelines: Stage 1 review can take months — build it into grants and theses.

## 4. OSF project structure
```
Project/
  Materials/        stimuli, task code, questionnaires (or links + licences)
  Preregistration/  frozen registration (linked, not editable)
  Data/             raw (de-identified) + processed + codebook
  Analysis/         scripts, R/Python environment file (renv.lock, requirements.txt)
  Manuscript/       preprint
```
- Make a **codebook** for every variable (name, label, values, missing codes).
- Choose a licence (CC-BY for materials/data, MIT/GPL for code are common).
- De-identify before upload: remove names, dates of birth, free-text that identifies,
  and check combinations of quasi-identifiers. Consent forms must permit sharing.
- Version the analysis with git; link a GitHub repo to OSF, or archive a release on Zenodo.

## 5. Multi-lab studies
Psychological Science Accelerator and Many Labs-style projects: a central protocol,
translated materials with back-translation, a shared data template, site-level
ethics approval, and an analysis plan with site as a random effect. Heterogeneity
across sites is itself a result — report it.

## 6. Judging "did it replicate?"
No single criterion. Report several: significance in the same direction; whether the
original estimate is inside the replication's CI; the replication effect size and CI;
equivalence test against the SESOI; and a meta-analytic combination. Avoid declaring
failure from a non-significant, underpowered result.

## 7. Avoid QRPs in your own work
Optional stopping, selective outcome reporting, flexible exclusions, HARKing
(hypothesising after results are known), and rounding p-values down. Preregistration
and full reporting (all conditions, all measures, all exclusions) address most.

## Gotchas
- Preregistrations that are vague ("we will analyse with appropriate methods") constrain nothing.
- "Data available on request" often means not available — deposit it.
- Uncertain: RR policies vary by journal; check the specific author guidelines.

## Verify
- [ ] Replication type stated and deviations from the original documented in advance.
- [ ] Sample size justified for a realistic (not original) effect.
- [ ] Protocol registered and time-stamped before data collection.
- [ ] Data, codebook, materials and code deposited with licences.
- [ ] Replication judged on several criteria including effect size and CI.
