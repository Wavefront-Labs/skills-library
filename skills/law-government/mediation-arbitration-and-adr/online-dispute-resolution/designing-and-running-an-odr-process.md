---
id: law-government.mediation-arbitration-and-adr.online-dispute-resolution.designing-and-running-an-odr-process
name: designing-and-running-an-odr-process
category: law-government
field: mediation-arbitration-and-adr
product: online-dispute-resolution
tags: [online-dispute-resolution, mediation-arbitration-and-adr, odr, e-adr, online-mediation, asynchronous-mediation, platform-dispute-resolution, marketplace-disputes, ecommerce-disputes, consumer-adr, chargeback, online-court, civil-resolution-tribunal, uncitral-technical-notes-on-odr, process-design, triage, guided-negotiation, solution-explorer, escalation-ladder, video-hearing, virtual-hearing, zoom-mediation, digital-exclusion, accessibility, data-protection, gdpr, cybersecurity, algorithmic-fairness, small-claims]
level: practitioner
status: draft
description: "Designing and running online dispute resolution: triage and guided negotiation, asynchronous mediation, online determination, video hearings, accessibility and data protection."
sources: ["UNCITRAL Technical Notes on Online Dispute Resolution (2016)", "Civil Resolution Tribunal (British Columbia) public process materials", "Katsh & Rabinovich-Einy, Digital Justice (2017)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing and running an ODR process

**Goal:** resolve high volumes of low-to-mid value disputes (marketplace, consumer,
small claims, tenancy, neighbour) online, fast and fairly, with human neutrals used
where they add most value. Models: UNCITRAL's three-stage ODR design, marketplace
resolution centres, and public online tribunals such as British Columbia's Civil
Resolution Tribunal. Consumer ADR and online-court rules differ by jurisdiction (and
change — e.g. the EU's central ODR platform was wound down in 2025); check what your
scheme must comply with.

## 1. Design the escalation ladder
| Stage | What happens | Typical clock |
|---|---|---|
| 0. Diagnosis / self-help | Guided questions explain rights and options; many disputes end here | Immediate |
| 1. Guided negotiation | Structured offers (refund, replacement, partial credit) exchanged on-platform | 7–14 days |
| 2. Facilitation (mediation) | A human facilitator joins the thread asynchronously; video if needed | 14–30 days |
| 3. Determination | Adjudicator decides on written submissions (hearing exceptional) | 14–30 days after close of evidence |
| 4. Enforcement / appeal | Platform remedies (refund, chargeback), court order, limited review | Per scheme |
Set every clock in the rules and send automatic reminders; default rules decide what
happens if a party goes silent (e.g. the claim proceeds to determination).

## 2. Intake and triage
- Structured forms capture the claim type, amount, key facts and documents in a
  consistent format (photos, receipts, message history).
- Triage rules route out what ODR shouldn't handle: safety issues, fraud, domestic
  abuse, vulnerable users, claims above the scheme limit.
- Ask about access needs at intake: language, disability, no-device or low-bandwidth
  users; offer phone or paper alternatives.

## 3. Running asynchronous mediation
1. Introduce yourself in the shared thread; explain stages, deadlines, confidentiality.
2. Use **private channels** with each party (the online caucus) for interests and offers.
3. Summarise frequently in neutral language; written tone escalates conflict faster
   than speech.
4. Propose concrete options with deadlines; capture agreement in a structured
   settlement form both parties click to accept — the platform generates the record.
5. Move to a short video session when text is going in circles.

## 4. Online determination and video hearings
- Decide on the documents where credibility isn't central; give each party notice of
  the other's evidence and a chance to respond.
- Video hearings: test links in advance; identity check; one speaker at a time; mute
  rules; screen-sharing for exhibits; a phone fallback; record if the rules require.
- Written decisions in plain language with short reasons and next steps.

## 5. Governance
- Data protection: minimum necessary data, retention schedule, lawful basis (GDPR
  where applicable), encryption, access logs.
- Algorithmic tools (outcome predictors, auto-suggested settlements): disclose use,
  audit for bias, keep a human decision-maker for determinations.
- Neutrality: platform-funded neutrals need visible independence safeguards.
- Publish metrics: resolution rate per stage, time to resolution, user satisfaction,
  outcomes split by party type.

## Gotchas
- Designing for the confident user; the digitally excluded drop out silently.
- Deadlines too tight for people with jobs and caring duties.
- Settlement wording that the platform cannot actually execute.
- Over-automation: users disengage if they never meet a human.

## Verify
- [ ] Every stage has rules, a clock and a default outcome.
- [ ] Triage screens out unsuitable disputes and vulnerable users.
- [ ] Non-digital and accessibility routes exist.
- [ ] Settlement and decision outputs are executable and enforceable.
- [ ] Data-protection and algorithm-governance documented; metrics published.
