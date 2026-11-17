---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.sre-and-devops-relationship
name: sre-and-devops-relationship
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre, sre-engagement, sre-vs-devops, devops, culture]
level: intro
status: docs-checked
description: "Explain how SRE relates to DevOps: shared principles, SRE as a concrete implementation (class SRE implements interface DevOps), and where the two differ in emphasis."
sources: ["https://sre.google/workbook/how-sre-relates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SRE and DevOps relationship

**Goal:** explain clearly to an organisation what SRE adds to an existing DevOps culture, using the SRE Workbook chapter
"How SRE Relates to DevOps" (title line: "class SRE implements interface DevOps").

## DevOps key ideas (Workbook)
DevOps is a loose set of practices, guidelines and culture designed to break down silos in IT development, operations,
networking and security. Its key ideas: no more silos; accidents are normal (they come from missing safeguards, so
focus on speeding recovery); change should be gradual (small and frequent); tooling and culture are interrelated
(culture matters more); measurement is crucial.

## SRE principles (Workbook)
Operations is a software problem; manage by SLOs; work to minimise toil; the wisdom of production; automate this year's
job away (a 50% limit on toil that the Workbook says is better thought of as a guarantee of engineering time); move
fast by reducing the cost of failure; share ownership with developers; use the same tooling regardless of job title.

## Commonality
Both accept that change is necessary; put collaboration front and centre; favour small, continual, automatically
tested changes; stress tooling and measurement (SLOs for SRE); and practise blameless postmortems. Both are holistic,
and better velocity should be the outcome.

## Differences
- DevOps is a wider philosophy and culture, more context-sensitive, and relatively silent on how to run operations in
  detail. SRE is a job role and set of practices with narrowly defined, service-oriented responsibilities and an
  opinionated framework (for example error budgets).
- SRE is relatively silent on siloization and information barriers. It would support CI and CD for the improved
  operational practice rather than the business case: SRE believes the same things for slightly different reasons.
- The Workbook notes product development teams own their service by default; SRE is neither available nor warranted
  for the bulk of services, though SRE principles still inform how services are managed.

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "How SRE Relates to DevOps". Corrected: the skill's mapping
table of DevOps principles to SRE practices is not in the chapter (it lists its own DevOps ideas and SRE principles
separately), so it was replaced with those lists. Removed: the organisational patterns section, the DORA and
handback claims, and the Google Cloud blog, SRE Book introduction and DORA sources (not read this batch).
Method: documentation only; no commands were run.
