---
id: computing-software.cybersecurity-defensive.application-security.bsimm-assessment
name: bsimm-assessment
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [bsimm, software-security-initiative, appsec-maturity, samm, benchmarking]
level: practitioner
status: draft
description: "Use BSIMM to benchmark a software security initiative: the four domains and twelve practices, activity levels, scorecards, and turning gaps into a roadmap."
sources: ["https://www.bsimm.com/framework.html", "https://www.blackduck.com/services/bsimm.html", "https://owaspsamm.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BSIMM assessment

The Building Security In Maturity Model is **descriptive**: it records which activities real software security
initiatives (SSIs) perform, from yearly studies of 100+ firms. Compare yourself to peers, rather than to an
ideal (OWASP SAMM is the prescriptive, open alternative).

## Structure
Four domains, twelve practices (3 each), around 125 activities each assigned level 1-3 (level 1 = commonly
observed, level 3 = rare):
- **Governance**: Strategy and Metrics (SM), Compliance and Policy (CP), Training (T).
- **Intelligence**: Attack Models (AM), Security Features and Design (SFD), Standards and Requirements (SR).
- **SSDL Touchpoints**: Architecture Analysis (AA), Code Review (CR), Security Testing (ST).
- **Deployment**: Penetration Testing (PT), Software Environment (SE), Configuration Management and
  Vulnerability Management (CMVM).
Activities have IDs like `CR1.4` (use automated code review tools) or `SM1.1` (publish process).

## Running a self-assessment
1. Identify the SSI scope (whole company or a business unit) and its software security group (SSG) and
   champions ("satellite").
2. Interview SSG, engineering leads, champions; collect artefacts. An activity counts only if it is actually
   done routinely, with evidence, not planned.
3. Mark each activity observed/not observed; build the **scorecard** per practice.
4. Compare against the published BSIMM data: overall and industry vertical (financial, ISV, healthcare, etc.),
   using the "spider chart" of practice scores and the list of most common activities.
5. Gaps worth closing first: level-1 activities that most peers do and you do not.

## From gaps to roadmap
- Pick 3-6 activities per year tied to your risk (e.g. AA1.1 security feature review if design flaws dominate).
- Assign owners, define evidence of done, re-assess annually.
- Official assessments are performed by the BSIMM vendor; self-assessment is fine for internal planning.

## Gotchas
- High scores do not equal secure software; BSIMM measures activities, not outcomes. Pair with metrics such
  as defect escape rate.
- Don't chase level-3 activities before level-1 basics are routine.
- Activity definitions change between BSIMM versions; note the version used.

## Verify
Scorecard cites evidence per observed activity, and the roadmap lists chosen activity IDs with owners and dates.
