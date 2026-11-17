---
id: computing-software.qa-testing-engineering.exploratory-testing.crowdsourced-testing-programmes
name: crowdsourced-testing-programmes
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [crowdtesting, crowdsourced-testing, experience-based-testing, device-coverage, localization-testing]
level: practitioner
status: draft
description: "Plan and run crowdsourced testing: when to use it, scoping and briefs, tester selection, confidentiality, payout models and validating results."
sources:
  - https://www.ministryoftesting.com/
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Crowdsourced testing programmes

**Goal:** use external testers at scale for device/locale coverage and fresh eyes, without drowning in low-quality reports.

## Good fits
- Real-world device, OS, carrier and network diversity beyond your lab.
- Localisation and in-country checks (payments, addresses, language quality).
- Usability feedback from target demographics.
- Pre-launch exploratory sweeps, payment flows in many countries.
Poor fits: deep domain logic, unreleased confidential features without strong NDA controls, regression testing better automated.

## Setting up a cycle
1. **Brief:** product overview, in-scope features and builds, out-of-scope list, known issues, test accounts, what a good report looks like, severity definitions.
2. **Selection:** filter testers by device, location, language, rating; invite more than needed.
3. **Mode:** exploratory with charters, scripted test cases for coverage, or usability tasks with recordings.
4. **Payout:** per approved bug (by severity), per executed test case, or hourly; per-bug models drive volume of trivial reports, so weight by severity and reject duplicates.
5. **Duration:** 24-72 h cycles are typical.

## Managing results
- Vendor or in-house triage validates reports (reproduce, dedupe) before they reach developers.
- Require video or screenshots, device details and build number.
- Feed accepted defects into your tracker with a crowd tag to measure value.

## Risks and controls
- Confidentiality: NDAs, watermarked builds, limited access windows.
- Test data: dedicated test accounts and payment sandboxes; no production customer data.
- Production testing by crowd needs agreement with operations and fraud teams.

## Gotchas
- Unclear scope produces reports on out-of-scope areas you still have to process.
- Measuring by bug count rewards noise; measure accepted, unique, severe defects per cost.

## Verify
Each cycle has a brief, a triage outcome summary (accepted/duplicate/rejected by severity), and cost per accepted defect.
