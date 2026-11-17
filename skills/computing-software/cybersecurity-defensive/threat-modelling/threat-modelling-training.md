---
id: computing-software.cybersecurity-defensive.threat-modelling.threat-modelling-training
name: threat-modelling-training
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [threat-modelling-training, developer-training, four-question-framework, security-education, threat-modelling]
level: practitioner
status: draft
description: "Teach developers to threat model: the four-question frame, a hands-on exercise on their own system, games, coached first models, and checking that skills stuck."
sources: ["https://www.threatmodelingmanifesto.org/", "https://shostack.org/resources/threat-modeling", "https://owasp.org/www-project-threat-dragon/", "https://github.com/adamshostack/eop"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Training developers to threat model

Goal: delivery teams produce useful models without a security engineer in the room for every change. Lectures
do not achieve this; practice on real systems with coaching does.

## Curriculum (about half a day, then coaching)
1. **Why and the four questions** (Shostack / Threat Modeling Manifesto, 20 min): What are we working on? What
   can go wrong? What are we going to do about it? Did we do a good enough job?
2. **Diagramming** (30 min): draw a DFD of a small sample app with processes, stores, external entities, flows
   and trust boundaries. Emphasise that a whiteboard sketch is enough.
3. **Finding threats** (60 min): STRIDE per element on the sample; then play Elevation of Privilege or OWASP
   Cornucopia for 30 minutes to make it social.
4. **Mitigations and tracking** (30 min): write two threats as backlog tickets with acceptance criteria.
5. **Own system** (60-90 min): each team diagrams something they are building now and finds at least five
   threats, with an experienced facilitator rotating between teams.

## Follow-up that makes it stick
- Coach the team's first two or three real models, then step back to reviewing.
- Provide templates: diagram stencil, threat table, ticket template, and a checklist of triggers for when to
  model.
- Security champions become local facilitators (pair with the champions programme).
- Tools: OWASP Threat Dragon or draw.io stencils; avoid heavyweight tools in the first course.

## Assessing effectiveness
- Before/after: give teams a small design and count relevant threats found (quality, not quantity).
- Review the next real models the team produces against a rubric: boundaries drawn, flows labelled, threats
  specific to the design, mitigations tracked.
- Track whether trained teams' models get updated on design change.

## Gotchas
- Generic sample apps bore senior engineers; use an anonymised internal design.
- Teaching every methodology confuses; pick one (STRIDE per element) and mention others as optional.
- Do not grade teams on threat counts.

## Verify
Within a quarter, trained teams have produced at least one model each without a security engineer authoring
it, and reviews of those models pass the rubric.
