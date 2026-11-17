---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.simple-prr-engagement-model
name: simple-prr-engagement-model
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [prr-engagement, simple-prr-model, production-readiness-review, sre-onboarding, sre-engagement]
level: practitioner
status: docs-checked
description: "Run the SRE Book's simple PRR engagement to onboard an existing service: engagement, analysis, improvements and refactoring, training, and onboarding."
sources: ["https://sre.google/sre-book/evolving-sre-engagement-model/", "https://sre.google/workbook/engagement-model/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The simple PRR engagement model

SRE Book "The Evolving SRE Engagement Model": the simple PRR model applies when a development team asks
SRE to take over production management of an existing service. Phases:

## 1. Engagement
- SRE leadership decides which SRE team is a good fit; usually one to three SREs are selected or
  self-nominate to run the PRR.
- They open discussion with the development team: SLO/SLA, disruptive design changes needed for
  reliability, and planning and training schedules. Outcome: common agreement on process and goals.

## 2. Analysis
- SRE reviewers learn the service and gauge its maturity with a service-specific PRR checklist (see
  `prr-checklist-and-questionnaire`), based on domain expertise and the Production Guide.
- They also review recent incidents, postmortems and follow-ups to gauge emergency-response demands.
- Output: recommended improvements.

## 3. Improvements and refactoring
- Improvements are prioritised by importance for reliability, negotiated with the dev team, and agreed
  as a plan; both teams help refactor or add features.
- This phase varies most in duration and effort.

## 4. Training
- The SRE reviewers train the whole team, usually with the dev team: design overviews, deep dives on
  request flows, the production setup, and hands-on exercises (see `on-call-learning-paths`).

## 5. Onboarding
- Progressive transfer of responsibility and ownership: parts of operations, the change management
  process, access rights. The dev team stays available to back up and advise for a period.

## Continuous improvement
After onboarding, the service stays healthy through ongoing reviews, error budgets and the production
meeting. If reliability degrades persistently, the engagement can be revisited or ended
(see `ending-sre-engagement-and-handback`).

## Exit criteria template (your own, not from the Book)
| Phase | Exit criteria |
|---|---|
| Engagement | SLO draft agreed; timeline; named leads on both sides |
| Analysis | gap list prioritised and accepted by dev lead |
| Improvements | agreed high-priority gaps closed |
| Training | each SRE on the rotation completed the walkthroughs and exercises |
| Onboarding | SRE primary on-call within pager load targets for an agreed period |

## Gotchas
- Accepting the pager before improvements are done creates an overloaded team with no leverage.
- The PRR model is late in the lifecycle; for new services prefer early engagement.

## Verify
- [ ] Each phase has documented exit criteria met before moving on.

## Checked
2026-11-01. Confirmed in SRE Book The Evolving SRE Engagement Model: the Simple PRR phases (Engagement, Analysis, Improvements and Refactoring, Training, Onboarding, Continuous Improvement) and their contents. Removed the secondary-then-primary on-call sequence, dev-on-call shadowing and Wheel of Misfortune in training, and the numeric exit criteria, none of which the chapter states. The Workbook engagement-model page was fetched but not checked line by line.
Method: documentation only; no commands were run.
