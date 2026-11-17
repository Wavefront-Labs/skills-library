---
id: computing-software.cybersecurity-defensive.application-security.security-champions-programme
name: security-champions-programme
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [secure-sdlc, security-champions, appsec-programme, developer-enablement, owasp-security-champions-guide, embedded-security]
level: practitioner
status: draft
description: "Run a security champions programme: recruit one engineer per team, define time allocation and duties, train them, give them a community and measure outcomes."
sources: ["OWASP Security Champions Guide", "OWASP SAMM v2 - Education and Guidance practice", "BSIMM - Satellite (security champions) activity data"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Security champions programme

**Goal:** a named, trained engineer in every delivery team who handles first-line security
questions, so the central AppSec team scales without becoming a ticket queue.

## Design
- **Who:** volunteers nominated with their manager's agreement; ideally one per team (BSIMM calls this the satellite).
- **Time:** written allocation, typically 10-20% of time. Without manager sign-off the role dies within two quarters.
- **Duties:** threat-model new features with AppSec support, triage SAST/SCA findings for their repos,
  review security-relevant PRs, be the contact during incidents, relay new standards to the team.
- **Not duties:** being accountable for the team's security alone, or doing pen tests.

## Running it
1. Kick-off: charter (one page), mailing list/chat channel, a tracker of champions by team.
2. Training path: secure coding for the team's stack, the company secure coding standard,
   threat modelling (STRIDE workshop), reading SAST output, how to escalate.
3. Monthly community call: a recent incident or finding, a new tool, a short CTF or lab.
4. Office hours from the AppSec team; champions get a fast lane.
5. Recognition: mention in performance reviews, conference budget, badges. Make it career-positive.

## Metrics
- Coverage: % of teams with an active champion (attended a call in last 60 days).
- Mean time to triage security findings in champion teams vs others.
- Threat models produced per quarter; security defects found pre-release vs post-release.

## Gotchas
- Choosing the most junior engineer because they have spare time; champions need credibility.
- Turnover: keep a deputy per team and re-check the roster quarterly.
- Measuring attendance only; measure findings fixed and design reviews done.

## Verify
- [ ] Every product team appears in the roster with a champion or an open action.
- [ ] Time allocation is written into each champion's objectives.
- [ ] Programme metrics reviewed with engineering leadership each quarter.
