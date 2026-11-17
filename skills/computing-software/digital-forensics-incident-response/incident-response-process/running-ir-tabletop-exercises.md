---
id: computing-software.digital-forensics-incident-response.incident-response-process.running-ir-tabletop-exercises
name: running-ir-tabletop-exercises
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [tabletop-exercise, ir-preparation, incident-readiness, exercise-design, dfir]
level: practitioner
status: draft
description: "Design and facilitate incident response tabletop exercises: objectives, scenario and injects, roles, facilitation, scoring and the after-action report."
sources: ["https://csrc.nist.gov/pubs/sp/800/84/final", "https://www.cisa.gov/resources-tools/services/cisa-tabletop-exercise-packages"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running IR tabletop exercises

**Goal:** expose gaps in the plan, decisions and communications before a real incident does.
NIST SP 800-84 covers test, training and exercise programs; CISA publishes free CTEP packages.

## Design (2-4 weeks before)
1. **Objectives** (3-5, testable): "Validate who authorises isolating the ERP", "Test OOB
   comms", "Exercise GDPR 72-hour decision".
2. **Audience**: technical tabletop (IR/IT) vs executive tabletop (decisions, comms, legal).
   Do not mix in one session.
3. **Scenario** grounded in your threat profile: ransomware via VPN credential, BEC wire
   fraud, cloud access key leak, insider exfiltration.
4. **Injects**: 8-12 timed messages that escalate and force decisions. Example sequence:
   EDR alert, then help desk reports, then ransom note, then journalist call, then leak-site
   post, then backup found encrypted.
5. Ground rules: no-fault, use real documents, "if it's not written down, you can't use it".

## Facilitation
- Facilitator presents injects and asks "what do you do now, who decides, how do you know?"
- Scribe records decisions, times, and every "we don't know" verbatim.
- Hold back hints; let silence work. Push on specifics: names, numbers, tools.
- 2-3 hours maximum; executives 90 minutes.

## After-action report (within 2 weeks)
- Per objective: met / partially / not met, with evidence.
- Findings as actionable items with owner and due date (plan change, tool access,
  training, contract).
- Track items to closure; re-test them in the next exercise.

## Gotchas
- Scenarios that are too easy or "magic" (the attacker always wins) teach nothing.
- Exec tabletop without legal and comms in the room misses the hardest decisions.

## Verify
Count findings closed from the previous exercise; a program where the same gaps recur is
not improving.
