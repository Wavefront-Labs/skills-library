---
id: computing-software.digital-forensics-incident-response.incident-response-process.out-of-band-incident-communications
name: out-of-band-incident-communications
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [out-of-band-communications, incident-communications, secure-communications, signal, dfir]
level: practitioner
status: draft
description: "Run incident communications out of band when email, chat or identity may be compromised: channel choice, setup, verification and operational security."
sources: ["https://csrc.nist.gov/pubs/sp/800/61/r3/final", "https://www.cisa.gov/stopransomware/ransomware-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Out-of-band incident communications

**Goal:** the attacker cannot read the response team's plans. In AD-joined or M365/Google
compromises, assume email, Teams/Slack, and anything authenticated by the corporate IdP is
readable by the adversary (CISA ransomware guide explicitly advises out-of-band comms).

## Channel choice
| Need | Option | Notes |
|---|---|---|
| Chat for core team | Signal / Wire / a separate tenant (pre-provisioned "break-glass" M365 or Slack workspace) | Not federated with corporate IdP; MFA on personal devices |
| Voice bridge | Conference line not tied to corporate SSO, or phone tree | Rotate PIN per incident |
| Documents | Separate tenant or encrypted shared drive set up in advance | Not the corporate SharePoint/Drive |
| Exec updates | Phone call, then written summary in the OOB channel | |

Set this up **before** an incident: accounts, device list, and a printed contact sheet in the
jump kit.

## Operational rules
- Decide at declaration whether comms go OOB (any domain admin, IdP or mail compromise = yes).
- Verify identities when someone joins (call back on a known number) since the attacker may
  already know names from the compromised mailbox.
- No IOC, plan or containment timing in corporate email or tickets until the environment is
  cleared; attackers watch for "we found you" mail and accelerate (ransomware deployment).
- Use code names for the incident; avoid naming hosts in subject lines.
- Disappearing messages off for the incident group: you need the record. Export the chat into
  the case file at close.
- Legal hold applies to OOB channels too.

## Gotchas
- People default back to Teams when the OOB app is clumsy; rehearse it in tabletops.
- Personal phones compromised or lost: keep membership tight and remove leavers promptly.

## Verify
At each tabletop, run the first hour entirely OOB. Anyone who cannot join within 15 minutes
is a gap to fix.
