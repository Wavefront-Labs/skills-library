---
id: computing-software.digital-forensics-incident-response.incident-response-process.pre-authorising-responder-authority-to-act
name: pre-authorising-responder-authority-to-act
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [ir-authority-to-act, incident-response-plan, containment-authority, delegation-of-authority, ir-policy, dfir]
level: practitioner
status: draft
description: "Pre-authorise responders in policy to isolate, disconnect, disable accounts and seize systems: delegation table, limits, business override and after-action logging."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://csrc.nist.gov/pubs/sp/800/61/r2/final", "https://www.cisa.gov/sites/default/files/publications/Federal_Government_Cybersecurity_Incident_and_Vulnerability_Response_Playbooks_508C.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pre-authorising responders' authority to act

The worst time to find out who may pull a production server off the network is 02:00 during ransomware staging. SP 800-61r2 (2.3.2) says the IR policy should state the team's authority to confiscate or disconnect equipment and monitor activity; 800-61r3 folds this under GV.RR and RS.MI.

## Delegation-of-authority table (put in the signed IR policy)
| Action | Who may act alone | Conditions | Must notify within |
|---|---|---|---|
| EDR-isolate a workstation | Any on-call analyst | Confirmed malicious activity | 1 h, system owner |
| Isolate a server / block a subnet | IR lead | Active compromise or spread | 30 min, service owner + duty manager |
| Disable a user or service account | IR lead | Credential compromise suspected | 1 h, account owner's manager / app owner |
| Seize a device physically | IR lead + HR or Legal for employee devices | Chain of custody started | Same day |
| Shut down a business-critical service | Incident commander with exec sponsor (CISO/CIO) | Life, safety or wide-scale data loss | Immediately, exec bridge |
| Monitor employee communications | Legal sign-off required | Jurisdictional rules | Before monitoring starts |

## Writing it
1. List the actions from your playbooks; each one either appears in the table or is "requires approval from X".
2. Name roles, not people; tie each to the on-call rota.
3. Include a business-override path: the service owner can ask the commander to reverse an action, but the responder does not wait for permission to act inside their row.
4. Get it signed by the executive who owns business risk (CEO/COO or delegated), not just the CISO.
5. Require each use to be logged in the incident decision log with time, rationale and who was told.

## Gotchas
- Outsourced or cloud systems: the authority has to be in the contract (MSP, MSSP, SaaS) or your responders cannot act.
- Employee-owned devices and monitoring need Legal and works-council review in many jurisdictions.
- Exercise it: a tabletop where the analyst hesitates to isolate the CFO's laptop reveals whether the policy is believed.

## Verify
Pick three containment actions from recent incidents and confirm each was inside a table row, logged, and notified within the stated window.
