---
id: computing-software.digital-forensics-incident-response.incident-response-process.choosing-a-csirt-model
name: choosing-a-csirt-model
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [csirt-model, csirt, ir-team, soc, nist-sp-800-61, dfir]
level: practitioner
status: draft
description: "Choose and staff a CSIRT model (central, distributed, coordinating, outsourced or hybrid) with on-call design and the skill mix an organisation actually needs."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://www.first.org/standards/frameworks/csirts/csirt_services_framework_v2.1"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a CSIRT model

**Goal:** an IR capability sized to the organisation, with clear coverage hours and an
escalation path that works on a Sunday.

## Models (NIST SP 800-61r2 2.4.1; FIRST CSIRT Services Framework)
| Model | Fits | Watch for |
|---|---|---|
| Central team | Single-country company, one IT org | Single point of failure if team is small |
| Distributed teams | Multinational, autonomous business units | Inconsistent process; needs a coordinating layer |
| Coordinating team | Holding company, government sector, PSIRT-style | Has authority to advise, not to act |
| Fully outsourced (MDR + retainer) | Small org, no 24x7 staff | Who can authorise containment at 2am? |
| Hybrid (in-house lead + MDR + retainer) | Most mid-size orgs | Hand-off points must be written down |

## Sizing questions
1. Required coverage: 24x7 monitoring needs about 5-6 FTE per seat; 24x7 *on-call* response
   needs at least 4 people in rotation to stay humane (one week in four).
2. Which services (FIRST framework): information security event management, incident
   management, vulnerability management, situational awareness, knowledge transfer.
3. Where forensics lives: in-house disk/memory skills, or retainer only?
4. Regulatory drivers (DORA, NIS2, PCI, HIPAA) that require tested capability.

## Skill mix for a core team of 4-6
Incident handler/lead, host forensics, network forensics, cloud/identity, malware triage,
and someone who writes well (reports and exec updates are half the job).

## On-call design
- Primary and secondary each week; documented paging thresholds tied to the severity matrix.
- Compensation and next-day relief written into policy, otherwise rotations decay.
- On-call runbook: how to get into the EDR, the bridge, the case system from a personal phone.

## Verify
Simulate a SEV1 page at an awkward hour; measure time to a qualified human on the bridge and
whether they could reach every tool they needed.
