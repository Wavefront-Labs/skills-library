---
id: computing-software.cybersecurity-defensive.security-operations.insider-threat-incident-response
name: insider-threat-incident-response
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [insider-incident-response, insider-threat, incident-response, evidence-preservation, legal-hold, hr-coordination]
level: advanced
status: draft
description: "Handle confirmed insider threat incidents: legal and HR-led process, evidence preservation, covert vs overt actions, access removal timing, and recovery of data."
sources: ["https://insights.sei.cmu.edu/library/common-sense-guide-to-mitigating-insider-threats-seventh-edition/", "https://www.cisa.gov/resources-tools/resources/insider-threat-mitigation-guide", "https://csrc.nist.gov/pubs/sp/800/61/r3/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Insider threat incident handling

## Governance
- Case lead is usually the insider risk/HR/legal function; security supplies evidence and technical
  actions. Agree decision rights at the start.
- Legal privilege: run the investigation under counsel direction where possible; label documents.

## Sequence
1. **Preserve covertly**: litigation hold on mailbox and OneDrive/Google Drive, export cloud audit
   logs, image or triage-collect the endpoint (remote, during normal use), snapshot relevant file
   shares, preserve badge and VPN logs. Do this before the subject knows.
2. **Scope**: what data left, to where (personal email, USB, cloud storage, printers), when,
   co-conspirators. Use DLP, proxy/CASB, endpoint USB events, print logs.
3. **Decide timing** with HR/legal: immediate access removal if active harm (sabotage, ongoing
   exfiltration), otherwise coordinate with the HR meeting.
4. **Overt actions** (at or just before the meeting): disable accounts, revoke sessions and tokens,
   remove VPN/MFA devices, collect devices, rotate shared credentials they knew, revoke
   physical access.
5. **Recover data**: legal letters for return/deletion, cloud provider requests, attestations;
   for USB devices, forensic examination of returned media.
6. **Report**: factual, no speculation about motive; regulators/customers if personal data
   breach thresholds are met.

## Sabotage cases
Check for logic bombs, scheduled tasks, cron jobs, backdoor accounts, changed passwords on
service accounts, deleted backups; review admin changes by the subject over the preceding months.

## Gotchas
- Interviews are HR/legal-led; security staff do not confront subjects.
- Chain of custody matters if the case goes to court or tribunal.
- Treat co-workers' data in the evidence carefully (privacy).

## Verify
Evidence inventory with hashes and custody log, documented decisions with timestamps and
approvers, all access removed and validated, and lessons learned fed into controls.
