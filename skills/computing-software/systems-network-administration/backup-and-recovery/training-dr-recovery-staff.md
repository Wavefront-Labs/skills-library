---
id: computing-software.systems-network-administration.backup-and-recovery.training-dr-recovery-staff
name: training-dr-recovery-staff
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [dr-training, recovery-team, cross-training, contingency-plan, nist-sp-800-34, business-continuity]
level: practitioner
status: docs-checked
description: "Train DR and recovery staff: role-based curricula, plan orientation, hands-on restore labs, cross-training, refreshers and training records."
sources:
  - https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final
  - https://csrc.nist.gov/pubs/sp/800/84/final
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Training recovery staff

**Goal:** enough people can perform each recovery role, confidently, at 3 a.m., without the plan's author.

## What the guides say
- NIST SP 800-84 defines training as informing participants of their roles and responsibilities within a particular IT plan and teaching the skills related to those roles, preparing them for exercises, tests and real emergencies. It can be instructor-led (classroom, interactive online) or self-study.
- SP 800-34 Rev. 1 (section 3.5.2): training should focus on familiarising staff with ISCP roles and teaching the skills needed. It should be provided at least annually, and people newly appointed to ISCP roles should be trained shortly after. The goal is that staff can execute their recovery roles without the plan document itself, in case plan copies are unavailable for the first few hours.
- Topics the guide lists: purpose of the plan, cross-team coordination and communication, reporting procedures, security requirements, team-specific processes (activation and notification, recovery, reconstitution) and individual responsibilities.
- Training sessions typically precede exercises and tests (SP 800-84), so people know their roles before the plan is exercised.
- Teams should be big enough to stay viable if members are unavailable, with alternates designated; members should know the goals and procedures of other teams. If staff are unavailable, personnel from another region or contractors may be coordinated and trained as an alternate team (SP 800-34, chapter 3 discussion of recovery teams).

## Who needs what (practice, tailor to your plan)
| Audience | Content |
|---|---|
| All plan role holders | Plan orientation: activation, notification, roles, where the plan lives, communication channels |
| Recovery team members | Hands-on procedures for their systems: restores, failovers, rebuilds, verification |
| Coordinators / leaders | Decision making, status tracking, escalation, stakeholder communication |
| Service desk | What to tell users during a disaster, how to escalate |
| Executives | Activation authority, decision points, external communication |

## Methods (practice)
- Orientation sessions on joining a role and on a schedule you set.
- Hands-on restore drills in a lab or isolated environment, rotating the engineer who performs each.
- Shadowing during real restores and exercises.
- Tabletop and functional exercises as applied training.

## Cross-training (practice)
Map each critical recovery task to more than one trained person across shifts and locations. Track coverage in a skills matrix; any task with one trained person is a risk item.

## Records and evaluation
- Keep a training log: person, role, module, date, method, assessor. Auditors ask for evidence.
- SP 800-84: participants typically complete an evaluation or critique form, feedback is analysed and documented in a training analysis report, and future sessions are modified as needed.

## Refresh triggers
SP 800-84 says events should follow organisational changes, plan updates or new TT&E guidance. Also refresh on new systems or tools, staff turnover and exercise findings showing confusion.

## Gotchas
- Training only on documentation, never hands-on, fails under stress.
- Relying on vendors for recovery is a single point of failure in a regional event; keep in-house capability.

## Verify
Skills matrix shows more than one trained person per critical task, and drill performance by newly trained staff meets RTO.

## Checked

2026-11-09. Checked against NIST SP 800-34 Rev. 1 (chapter 3 team and TT&E sections) and NIST SP 800-84 (sections 2 and 3), using the PDFs behind the csrc.nist.gov pages. Targeted reads, not the whole documents. Confirmed: training definition, annual minimum and new-role training, topic list, alternate teams, training analysis report, training before exercises. Removed: "monthly or quarterly" drills, "at least two (ideally three)" trained people (now "more than one", labelled practice), and the claim that NIST expects a particular log format. Tables labelled practice.

Method: documentation only; no commands were run.
