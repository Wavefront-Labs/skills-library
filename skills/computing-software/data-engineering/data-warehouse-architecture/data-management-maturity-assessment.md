---
id: computing-software.data-engineering.data-warehouse-architecture.data-management-maturity-assessment
name: data-management-maturity-assessment
category: computing-software
field: data-engineering
product: data-warehouse-architecture
tags: [data-warehouse-architecture, data-maturity-assessment, dcam, dmm, capability-maturity, gap-analysis, data-strategy-roadmap]
level: practitioner
status: draft
description: "Run a data management maturity assessment with DCAM, DAMA-DMBOK or CMMI DMM: scope, evidence-based scoring, stakeholder interviews, gap analysis and a prioritised roadmap."
sources:
  - https://edmcouncil.org/frameworks/dcam/
  - https://www.dama.org/cpages/body-of-knowledge
  - https://cmmiinstitute.com/dmm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Data management maturity assessment

## Choose a framework
| Framework | Notes |
|---|---|
| EDM Council DCAM | capability-based, popular in financial services; detailed scoring guides; licensed |
| DAMA-DMBOK knowledge areas | 11 areas (governance, architecture, modelling, storage, security, integration, documents, reference/master data, warehousing/BI, metadata, quality) - free structure, build your own scale |
| CMMI DMM (Data Management Maturity) | 5 levels, process-oriented |
| Vendor/analyst models (Gartner, etc.) | quick, less rigorous |
Use a 1-5 scale with written criteria per level so different assessors score alike: 1 ad hoc, 2 developing/project-level, 3 defined and repeatable, 4 managed and measured, 5 optimised.

## Plan
- Scope: whole enterprise or priority domains; which capabilities.
- Sponsor and purpose: regulatory response, data strategy input, platform investment case. Purpose shapes depth.
- Timeline: 6-10 weeks typical.

## Gather evidence (not opinions)
- Interviews/workshops per domain: owners, stewards, engineers, analysts, consumers.
- Artefacts: policies, glossary/catalog coverage, DQ dashboards, incident logs, access review records, lineage, architecture docs.
- Quantitative indicators: % critical data elements with owners, DQ rule coverage, time to provision data access, % pipelines with tests, catalog adoption.
Score each capability with evidence references; "we plan to" counts as level 1-2.

## Analyse
- Current vs target per capability (target set by business need; not everything needs level 4).
- Heat map by domain x capability.
- Root causes, dependencies (e.g. quality monitoring depends on ownership and metadata).

## Roadmap
- 3 horizons: quick wins (0-3 months), foundations (3-12), scale (12-24).
- Each initiative: capability gap closed, owner, cost, measurable outcome, dependency.
- Favour initiatives tied to business outcomes (regulatory report accuracy, faster onboarding of a data product) over abstract maturity points.

## Repeat
Reassess annually with the same criteria; report movement with evidence, not just scores.

## Verify
- [ ] Every score references evidence; criteria per level documented.
- [ ] Roadmap items each map to a capability gap and a business outcome with an owner.
