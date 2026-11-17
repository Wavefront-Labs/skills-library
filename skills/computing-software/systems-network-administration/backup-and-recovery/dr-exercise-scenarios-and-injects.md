---
id: computing-software.systems-network-administration.backup-and-recovery.dr-exercise-scenarios-and-injects
name: dr-exercise-scenarios-and-injects
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [exercise-injects, msel, tabletop-exercise, dr-exercise, tabletop, functional-exercise]
level: practitioner
status: docs-checked
description: "Write DR exercise scenarios with a master scenario events list (MSEL) and message injects as NIST SP 800-84 defines them, plus exercise staff roles."
sources:
  - https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-84.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DR exercise scenarios and injects

NIST SP 800-84 builds a functional exercise from objectives, a scenario, a **Master Scenario Events List (MSEL)** and **message injects** played by controllers.

## Objectives first
Functional exercise objectives validate the plan's content, participants' roles and responsibilities, and the documented interdependencies, and give participants hands-on practice executing their functions. Write specific objectives and tell participants what they are. Injects exist to serve these.

## Scenario
- It adds realism by giving participants situations that inspire responses toward the objectives, and must not stray outside the exercise scope.
- It may explore worst cases, but it is often more useful to use topical issues the organisation is likely to meet; SP 800-84's example for an organisation prone to natural disasters is a significant power outage caused by a hurricane.
- A short, concise scenario works better than a detailed one, because participants otherwise critique the scenario. A trusted agent who knows the plan can help with the scenario, MSEL and injects.

## MSEL
A chronologically sequenced outline of the simulated events and key event descriptions that participants respond to. It also lists expected actions and the objectives the events serve. It regulates simulated events by coordinating participants' actions and defining the event schedule. Plan it so key events lead to the objectives and all participants stay active. It is for exercise development and management only, not for players.

## Message injects
- A pre-scripted message given to participants during play (also called an implementer or event inject), in the form of e-mail, letter, memo, phone call or radio script.
- SP 800-84's example: the vehicle carrying backup tapes to the restoration site is in a traffic jam and will arrive three hours late.
- Each inject records the time injected, who it goes to, who it comes from, how it is delivered, and the text. One MSEL entry can have several injects.
- Use enough injects to keep participants busy but not overwhelmed; the number varies with duration.
- A **message inject tracking form** lists inject numbers, scheduled and actual times, a summary and comments for the person injecting.

## Roles (functional exercise)
- **Exercise director**: responsible for staffing, development, conduct and logistics; announces the end, and ends the exercise at once if a real emergency occurs.
- **Controllers**: monitor and run exercise activity from a control cell, introducing the scenario and injects and keeping to the MSEL and tracking form.
- **Data collectors**: observe and record player actions against the evaluation criteria.
- **Simulators**: play non-participating internal and external parties and keep responses consistent with the MSEL.

## Scaling
SP 800-84 expects training, then tabletop exercises, before a functional exercise; a comprehensive functional exercise of the whole plan is a full-scale exercise.

## Verify
The after action report rates each objective from data collectors' records and lists recommendations for the plan.

## Checked

2026-11-09. Read NIST SP 800-84 sections 5.2 to 5.5 (functional exercises: objectives, staff, scenario, MSEL, message injects, tracking form, conduct). Removed: FEMA HSEEP source (not read), the sample MSEL table and example times, the list of "good injects", the safety officer role, the 30-minute and 4-hour example objectives, and the "year by year" scaling advice (not stated).

Method: documentation only; no commands were run.
