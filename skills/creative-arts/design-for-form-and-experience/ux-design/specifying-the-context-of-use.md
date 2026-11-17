---
id: creative-arts.design-for-form-and-experience.ux-design.specifying-the-context-of-use
name: specifying-the-context-of-use
category: creative-arts
field: design-for-form-and-experience
product: ux-design
tags: [human-centred-design, iso-9241-210, context-of-use, iso-25063, user-characteristics, environment-analysis, ux-research, ux-design]
level: practitioner
status: draft
description: "Write an ISO 9241-210 context-of-use description: users and stakeholder groups, goals and tasks, technical, physical and social environment, and how it feeds requirements."
sources:
  - "ISO 9241-210:2019 Ergonomics of human-system interaction - Human-centred design for interactive systems, clause 7.2 (iso.org/standard/77520.html)"
  - "ISO/IEC 25063:2014 Common Industry Format for context of use description"
  - "Usability.gov / NN/g field study guidance"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Context of use description

**Goal:** a shared, evidence-based description of who will use the system, for what, and in what
conditions; the first design activity in ISO 9241-210 and the input to user requirements.

## What it contains (ISO 9241-210 7.2, ISO/IEC 25063 structure)
1. **Users and other stakeholders:** each user group (primary, secondary, indirect) and
   stakeholders affected without using it.
2. **User characteristics per group:** knowledge and skills, experience with similar systems,
   language, physical and sensory abilities, attitudes, frequency of use, training available.
3. **Goals and tasks:** what each group wants to achieve, the main tasks, frequency, duration,
   criticality, dependencies, and where errors would be dangerous or costly.
4. **Environment:**
   - Technical: devices, browsers, connectivity, other systems used alongside.
   - Physical: location, light, noise, temperature, standing/moving, gloves, one-handed use.
   - Social and organisational: interruptions, time pressure, policies, who else is present,
     privacy.
5. **Sources and confidence:** which facts come from field research, analytics, or assumption.

## How to produce it
1. Draft from existing knowledge with stakeholders (a 90 minute workshop); mark everything as
   assumed.
2. Validate with field visits, interviews and analytics (see contextual inquiry and interview skills).
3. Write it as a table per user group, 2-4 pages total; attach photos of real environments.
4. Review with the team and update when research contradicts it.

## How it is used
- Derive user requirements (each requirement traces to a context fact).
- Set test conditions: usability tests should reproduce the critical context (outdoors, on a
  phone, interrupted).

## Gotchas
- Describing the ideal user instead of the real range of users.
- Skipping the environment section; that is where mobile and field products fail.
- Writing once and never updating.

## Verify
Each user group has evidence beyond assumption for its top tasks and environment; every high-
priority requirement links to at least one context-of-use fact.
