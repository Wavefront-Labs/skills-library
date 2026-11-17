---
id: law-government.mediation-arbitration-and-adr.online-dispute-resolution.designing-an-odr-process-and-running-asynchronous-mediation
name: designing-an-odr-process-and-running-asynchronous-mediation
category: law-government
field: mediation-arbitration-and-adr
product: online-dispute-resolution
tags: [mediation-arbitration-and-adr, online-dispute-resolution, odr, e-adr, asynchronous-mediation, text-based-mediation, video-mediation, video-hearing, zoom-mediation, breakout-rooms, platform-dispute-resolution, consumer-disputes, small-claims, online-court, civil-resolution-tribunal, diagnosis-phase, automated-negotiation, blind-bidding, digital-signature, accessibility, digital-divide, data-protection, ombuds, fourth-party]
level: practitioner
status: draft
description: "Design and run online dispute resolution: staged diagnosis-negotiation-mediation-decision flow, asynchronous text mediation technique, video hearing control, accessibility and data safeguards."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing an ODR process and running asynchronous mediation

**Goal:** resolve high-volume or long-distance disputes online with a process people can
use without a lawyer, that settles most cases early and stays fair for the rest.

## 1. Process design: the staged funnel
Most successful ODR systems (platform marketplaces, consumer schemes, online tribunals
such as British Columbia's Civil Resolution Tribunal) use escalating stages:
1. **Diagnosis / self-help** — guided questions classify the problem, explain rights
   and likely outcomes, and generate templates. Many disputes end here.
2. **Assisted negotiation** — the parties exchange structured messages or offers on
   the platform; optional **blind bidding** (settles automatically if offers come
   within an agreed range).
3. **Facilitation / mediation** — a human neutral joins, usually asynchronously.
4. **Decision** — adjudication or arbitration on the documents, with a hearing only
   when credibility is central.
For each stage define: entry criteria, time limits, what the user sees, the
default if a party goes silent, and the data captured.

Design checklist:
- **Plain-language** interface, mobile-first, tested with real users (reading age,
  language options, screen readers — check WCAG conformance).
- **Assisted digital** route (phone, paper, in-person help) for people who can't go online.
- Clear statement of **who the neutral is** and that the platform operator is not a
  party-side advocate — critical when a marketplace runs disputes about its own sellers.
- Data protection: lawful basis, retention, access controls, where data is hosted.
- Enforcement: how outcomes are implemented (refund via platform, consent order,
  arbitral award, chargeback).
- Metrics: resolution rate per stage, time to resolution, user satisfaction by party
  type, outcome distributions (check for systematic bias).

## 2. Asynchronous (text) mediation technique
- Open with a welcome post: role, neutrality, timetable, response expectations
  (e.g. "reply within 48 hours"), confidentiality, and that private messages to the
  mediator are available.
- Use **private channels** like caucuses; label clearly which messages the other
  side sees — the most damaging ODR error is a private note posted in the joint thread.
- Summarise each party's position in neutral language; people re-read text, so word
  carefully and avoid anything that reads as judgment.
- Ask one or two focused questions per post; long posts get skimmed.
- Track deadlines; send reminders; define what silence means in advance.
- Draft settlement terms on the platform for both to accept explicitly (click-to-agree
  or e-signature), with a payment/action date.

## 3. Synchronous video sessions
- Test tech beforehand; send a link per party; have a phone fallback.
- Use the waiting room and **breakout rooms** for caucus; confirm who can hear you
  before speaking confidentially.
- Check who else is in the party's room (ask for a camera pan if it matters), and agree
  no recording.
- Shorter sessions with breaks; screen fatigue is real.

## Gotchas
- Automated or AI triage must not quietly decide merits; disclose where automation is
  used and offer human review. Rules on automated decision-making **vary by
  jurisdiction** (e.g. GDPR Art. 22 in the EU).
- Repeat players (platforms, retailers) learn the system faster than one-time users;
  monitor outcomes for that imbalance.
- Electronic signatures and online awards: check form and enforceability locally.

## Verify
- [ ] Each stage has entry criteria, deadlines and a default for non-response.
- [ ] Non-digital access route exists and has been tested.
- [ ] Private and joint channels visibly distinct; mediator double-checks before posting.
- [ ] Settlement terms explicitly accepted by both parties on the record.
- [ ] Outcome metrics reviewed by party type for bias.
