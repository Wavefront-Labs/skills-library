---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.incident-command-roles-and-communications
name: incident-command-roles-and-communications
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [incident-management, incident-commander, incident-roles, operations-lead-role, communications-lead-role, planning-lead-role, declaring-incidents, incident-declaration-criteria, incident-state-document, live-incident-doc, incident-handoff, follow-the-sun-handoff, incident-communications, stakeholder-updates, status-page-updates]
level: practitioner
status: docs-checked
description: "Run an incident with ICS-style roles (IC, ops, comms, planning): when to declare, the live incident state document, clean handoffs, and stakeholder updates."
sources: ["https://sre.google/sre-book/managing-incidents/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Incident command, roles and communications

## Declare early
The SRE Book's guideline: declaring early and finding a simple fix is better than spinning up the framework
hours into a growing problem. Set clear declaration conditions; the book's team treats the event as an
incident if **any** is true:
- You need to involve a second team in fixing the problem.
- The outage is visible to customers.
- The issue is unsolved after an hour of concentrated analysis.

## Roles
The framework is based on the Incident Command System. Everyone must know their role and not stray onto
someone else's turf; clear separation gives people more autonomy.
| Role | Does |
|---|---|
| **Incident commander** | holds the high-level state; structures the response, assigning responsibilities by need and priority; de facto holds every position not delegated; removes roadblocks for Ops |
| **Operations lead** | works with the IC applying operational tools; the operations team is the only group modifying the system during an incident |
| **Communications** | public face of the response: periodic updates to the response team and stakeholders (usually email); may also keep the incident document current |
| **Planning** | supports Ops with longer-term issues: filing bugs, arranging handoffs, tracking how the system has diverged from the norm so it can be reverted afterwards |
A role holder who is overloaded asks the planning lead for more staff and delegates (possibly via subincidents).
Give responders a recognised command post (a war room, or a chat channel/email thread) so people know where to
reach the IC.

## Live incident state document
The IC's most important responsibility is a living incident document, ideally editable by several people at
once. A messy-but-functional doc is fine; use a template and keep the most important information at the top.
Do not host it on the system you are trying to fix. Keep it for the postmortem.

## Handoff
Hand the IC post off clearly at the end of the working day. Brief the new IC until fully apprised, then the
outgoing IC states explicitly "You're now the incident commander, okay?" and does not leave until receiving
firm acknowledgment. Tell everyone else working the incident who is now in charge.

## Practice
Incident-management skill atrophies without use: apply the framework to other cross-team or cross-timezone
changes, include it in disaster-recovery tests, and role-play past on-call issues.

## Checked
2026-11-01. Confirmed against the SRE Book chapter Managing Incidents: declaration criteria, the four roles and
their duties, the live incident document, the explicit handoff wording, practice advice. Removed: update
cadences, status-page state names, separate-channel rule, the 10-minute IC target, "IC does not debug", which
that chapter does not state.
Method: documentation only; no commands were run.
