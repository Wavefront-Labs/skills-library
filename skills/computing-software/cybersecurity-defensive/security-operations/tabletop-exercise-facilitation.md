---
id: computing-software.cybersecurity-defensive.security-operations.tabletop-exercise-facilitation
name: tabletop-exercise-facilitation
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [incident-response, tabletop-exercise, ir-testing, scenario-design, after-action-report, cisa-ttx, exercise-facilitation]
level: practitioner
status: draft
description: "Design and run incident response tabletop exercises: objectives, realistic scenarios with injects, facilitation, capturing gaps and turning them into tracked actions."
sources: ["https://www.cisa.gov/resources-tools/services/cisa-tabletop-exercise-packages", "https://csrc.nist.gov/pubs/sp/800/84/final", "https://www.ncsc.gov.uk/information/exercise-in-a-box"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tabletop exercises

**Goal:** test the IR plan, decisions and communication with the real people, find gaps
cheaply, and fix them (NIST SP 800-84 test, training and exercise guidance).

## Plan (2-4 weeks ahead)
- **Objectives** (3-5, testable): "Exec team decides on ransom stance within the plan's
  authority model"; "SOC escalates to IC within 30 minutes"; "Legal determines notification
  obligations from the facts given".
- **Audience:** technical (SOC, IT, IR) or executive (CEO, CFO, legal, comms) or both
  in separate sessions. 8-15 participants.
- **Scenario:** realistic for your threat profile (ransomware via VPN appliance exploit, BEC
  payment fraud, cloud tenant compromise, third-party SaaS breach). CISA CTEP and NCSC
  Exercise in a Box provide ready scenarios.
- **Injects:** timed developments that force decisions: media enquiry, ransom note with
  deadline, backups found encrypted, regulator call, key person unreachable, attacker emails
  staff.
- Roles: facilitator, scribe/observers (one per group), optional "white cell" playing
  external parties.

## Run (2-3 hours)
1. Ground rules: no-fault, decisions are hypothetical but answer as you would really act,
   use the actual plan and contact lists.
2. Present the scenario in phases; after each inject ask: What do you know? Who needs to know?
   What do you decide? Who has authority?
3. Push on specifics: "Show me the number you would call", "Where is the plan if the wiki
   is encrypted?"
4. Keep time; park deep technical tangents.

## Hot wash and after-action report
- Immediately: what went well, what did not, surprises.
- AAR within two weeks: objectives met/partially/not; findings with evidence; each gap
  becomes an action with owner and due date in the tracker.
- Common findings: unclear decision authority, out-of-band comms missing, outdated contacts,
  no insurer engagement steps, backup recovery times unknown.

## Gotchas
- Scenarios that are too easy or too exotic teach nothing; base on recent real incidents.
- Executives skipping the session; schedule with their assistants months ahead.
- Actions not tracked means the same gaps next year.

## Verify
At the next exercise, check last time's actions are closed and the related failure does not repeat.
