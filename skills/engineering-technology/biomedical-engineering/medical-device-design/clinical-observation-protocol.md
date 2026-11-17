---
id: engineering-technology.biomedical-engineering.medical-device-design.clinical-observation-protocol
name: clinical-observation-protocol
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [clinical-observation, needs-finding, clinical-immersion, ethnography, observation, biodesign]
level: practitioner
status: draft
description: "Run a structured clinical immersion: get access and consent, observe procedures without leading, capture observations as raw notes and turn them into need candidates."
sources: ["Zenios et al., Biodesign: The Process of Innovating Medical Technologies (observation and problem identification chapters)", "Site clinical-observer and privacy policy (hospital specific)", "https://www.iso.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Clinical observation protocol

**Goal:** come out of a clinical immersion with 100+ raw observations tied to a real workflow, not a list of solutions someone already liked.

Practice guidance. Hospital access rules, patient privacy law (for example HIPAA in the US, GDPR in the EU) and local ethics policy decide what you may do; confirm them with the site before you start.

## Before you go
1. Get written permission from the department lead and the hospital's observer or vendor-access office. Many sites require occupational health clearance, vaccination records and a badge.
2. Agree what you may see. Observers normally never touch patients or equipment, never record audio or video without a documented agreement, and never write patient identifiers in notes.
3. Pick the clinical area by a hypothesis about where unmet need lives (high error rate, long cases, repeated workarounds), not by device idea.
4. Prepare a notebook template: time, location, role, action, what surprised you, workaround seen, quote (anonymised).

## While observing
- Watch complete episodes (patient arrival to hand-off), not highlights. Note idle time, repeated actions, improvised tools (tape, towels, extra hands) - these are need signals.
- Ask open, neutral questions at quiet moments: "walk me through what you just did", "what happens when this goes wrong". Do not pitch.
- Record one observation per line, factual and without solution language.
- Use more than one site or clinician before generalising; practice varies.

## After
- Same day: rewrite notes, remove any identifier, tag each observation by theme (safety, time, cost, ergonomics, outcome).
- Turn recurring observations into need candidates for the need-statement step (see `engineering-technology.biomedical-engineering.medical-device-design.need-statement-writing`).

## Gotchas
- Observer effect: clinicians may do things by the book while watched; stay long enough that they stop performing.
- Confirmation bias: log disconfirming observations too.
- Never leave with protected health information on a personal phone.

## Verify
- [ ] Permission and privacy terms documented.
- [ ] 100+ observations, none containing identifiers or solutions.
- [ ] Each candidate need traces to at least two independent observations.
