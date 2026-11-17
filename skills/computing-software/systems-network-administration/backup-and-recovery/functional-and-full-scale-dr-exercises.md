---
id: computing-software.systems-network-administration.backup-and-recovery.functional-and-full-scale-dr-exercises
name: functional-and-full-scale-dr-exercises
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [functional-exercise, full-scale-exercise, dr-exercises, dr-test, failover-test, nist-sp-800-84, hseep]
level: advanced
status: docs-checked
description: "Plan and run functional and full-scale DR exercises: objectives and scope, safety criteria, exercise staff, executing recovery steps and failback."
sources:
  - https://csrc.nist.gov/pubs/sp/800/84/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Functional and full-scale exercises

**Goal:** prove people can execute recovery procedures on real systems, not just discuss them.

## Types (NIST SP 800-84, section 5)
- **Functional exercise**: personnel validate operational readiness by performing their duties in a simulated operational environment. It exercises specific team members, procedures and assets in one or more functional aspects of a plan (for example communications, emergency notifications, IT equipment setup). Staff execute roles as they would in an emergency, but in a simulated manner.
- **Full-scale exercise**: SP 800-84 treats it as the far end of functional exercises: a comprehensive exercise of an entire IT plan, addressing all plan elements. Whether deployments and mobilisations are simulated or actually happen depends on the scope. For a full-scale exercise both senior-level and operational-level personnel should participate.

## Planning
1. Ensure staff are trained, and ideally tabletop exercises have been held, before a functional exercise (SP 800-84 says this is usually best).
2. **Topic and scope**: the full plan or one phase (activation, operation, reconstitution) or function. Initial functional exercises often concentrate on operational-level roles.
3. **Objectives**: validate plan content, participants' roles and responsibilities, and the interdependencies documented in the plan, and give hands-on practice. Document specific objectives and state them clearly to participants. SP 800-84 notes SP 800-53 requires federal agencies to exercise or test contingency plans at least annually.
4. **Staff**: an exercise director, controllers (monitor and control activity, run the control cell), data collectors (record actions against evaluation criteria) and simulators (stand in for non-participating parties). Staff should know the plan and objectives and meet beforehand.
5. **Documentation**: briefings, scenario, master scenario events list (MSEL), message injects with a tracking form, controller/data collector/simulator books, evaluation criteria and the after action report outline. Tell participants about any exercise artificialities in the briefing.
6. Logistics start around three months ahead per the guide's checklist; design typically starts three to six months in advance. Get management approval for the exercise.
7. Safety controls are practice, not from SP 800-84: no-go criteria before start (production health, staffing), abort criteria (data at risk, customer impact), rollback plan and an approved change record. The guide does say the exercise director must end the exercise immediately if a real emergency occurs.

## Execution
- A functional exercise typically runs in real or near-real time, often started by a phone call alerting people that the plan is activated, then the notification process in the plan.
- Controllers introduce the scenario and injects from a control cell and keep to the MSEL timeline; data collectors observe and record; simulators play the outside parties.
- Evaluators note timings, issues, procedure gaps and dependencies discovered; record deviations from documented procedures rather than fixing them on the fly (practice).

## Failback (practice)
Plan failback as carefully as failover; data written at the DR site must replicate back. SP 800-84 does not cover this, but the reconstitution phase of the plan being exercised does (see the SP 800-34 skills).

## After
- Hot wash right after play: the director leads a debrief and collects notes and forms.
- After action report: scope, objectives and scenario, observations by staff and participants, recommendations for the plan, participant list, survey results. The plan coordinator assigns action items and updates the plan, and may brief managers.

## Gotchas
- Fixing procedures on the fly hides gaps; record deviations instead.
- Exercising only the easy systems produces false confidence; rotate scope.

## Verify
Measured recovery times and completion rates per objective are recorded against targets and compared with the previous exercise.

## Checked

2026-11-09. Checked against NIST SP 800-84 (PDF behind the csrc.nist.gov page), sections 2, 3 and 5 (functional exercises), plus the executive summary. Targeted reads, not the whole 97 pages. Confirmed: exercise definitions, full-scale as comprehensive exercise of the entire plan, objectives, staff roles, documentation set, conduct, hot wash and after action report. Removed: the FEMA HSEEP source and HSEEP attribution (not read), the "weekend" production-move example, the "safety officer" role (not in the guide), and the claim that the guide covers failback. Safety controls and failback are labelled as practice.

Method: documentation only; no commands were run.
