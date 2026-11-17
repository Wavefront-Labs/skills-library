---
id: computing-software.digital-privacy-hygiene.privacy-configuration.threat-model-assets-and-likelihood
name: threat-model-assets-and-likelihood
category: computing-software
field: digital-privacy-hygiene
product: privacy-configuration
tags: [digital-privacy-hygiene, privacy-configuration, threat-model-assets, risk-likelihood-assessment, threat-model, security-plan, adversary-analysis, eff-ssd, security-scenario]
level: intro
status: docs-checked
description: "Write a one-page personal threat model from EFF's questions: what you protect, from whom, consequences, likelihood, effort you will spend, and allies."
sources:
  - "https://ssd.eff.org/module/your-security-plan"
  - "https://www.privacyguides.org/en/basics/threat-modeling/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Threat model: assets and likelihood

**Goal:** stop doing random security advice; spend effort where your real risks are.

## The questions
EFF's "Your Security Plan" (Surveillance Self-Defense) lists six questions; Privacy Guides' "Threat Modeling"
uses the first five.
1. **What do I want to protect?** (assets) - data you keep, where it is kept, who has access to it and what stops
   others from accessing it. Assets are usually information (emails, contacts, messages, location, documents); the
   devices themselves can be assets.
2. **Who do I want to protect it from?** (adversaries) - EFF's examples: your boss, law enforcement, a former
   partner, business competition, your government, a hacker on a public network, and trusted people who are careless
   with their own security.
3. **How bad are the consequences if I fail?** - consider what the adversary might do with the data and how capable
   they are.
4. **How likely is it that I will need to protect it?** - risk is the likelihood that a particular threat against a
   particular asset will occur; separate what might happen from how probable it is. Assessing risk is personal and
   subjective.
5. **How much trouble am I willing to go through?** - there is no perfect option; balance convenience, cost and
   privacy, and note financial, technical and social constraints.
6. **Who are my allies?** (EFF only) - people whose security overlaps with yours; agree shared practices, and
   remember an "insider threat" can sit inside a trusted circle.

Write down which threats you will take seriously and which are too rare, too harmless or too hard to combat. Both
guides note the list of adversaries may be something to destroy once the plan is done.

## Scoring grid (this skill's own aid, not from EFF or Privacy Guides)
For each asset-adversary pair: Likelihood (1-3) x Impact (1-3). Work on the highest scores first.
Example:
| Asset | Adversary | L | I | Score | Action |
|---|---|---|---|---|---|
| Email | Credential-stuffing criminal | 3 | 3 | 9 | Unique password + passkey |
| Location | Ex-partner | 2 | 3 | 6 | Review location sharing |
| Browsing | Ad networks | 3 | 1 | 3 | Blocker |

## Review
EFF: a security plan changes as your situation changes; create it, then mark your calendar to review it. Typical
triggers: new job, move, relationship change, becoming public-facing, risky travel.

## Verify
- [ ] One-page model written with top 5 scored risks and actions.

## Checked
Checked 2026-11-08 against the full text of both cited pages (EFF "Your Security Plan"; Privacy Guides "Threat
Modeling"). Fixed: EFF lists six questions (adds allies), not five; question wording and examples now follow the
pages. Removed: the unsupported claims about the likelihood of opportunistic crime and state targeting, the list of
SSD scenarios, and the Safety Check example. The scoring grid is labelled as this skill's own aid.
Method: documentation only; no commands were run.
